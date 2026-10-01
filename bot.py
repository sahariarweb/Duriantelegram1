import logging
import requests
import asyncio
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton, Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
    ConversationHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
)

# Logging Setup
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# Credentials & Settings
BOT_TOKEN = "8299974008:AAEMPLwWuia2RljJSL6b4qVlMlMygCfDfyU"
PANEL_USERNAME = "Sahariar69x"
PANEL_API_KEY = "ZkVGanQyZjdESzgxeFFsZHZZKzN2QT09"
ALLOWED_TELEGRAM_USER = "sahariar69x"

TELEGRAM_PROJECT_ID = "1" 
BASE_URL = "https://api.durianrcs.com/out/ext_api"

STATE_TARGET_CUY = 1

active_sessions = {}

COUNTRY_FLAGS = {
    "afghanistan": "🇦🇫", "albania": "🇦🇱", "algeria": "🇩🇿", "andorra": "🇦🇩", "angola": "🇦🇴",
    "argentina": "🇦🇷", "armenia": "🇦🇲", "australia": "🇦🇺", "austria": "🇦🇹", "azerbaijan": "🇦🇿",
    "bahrain": "🇧🇭", "bangladesh": "🇧🇩", "belarus": "🇧🇾", "belgium": "🇧🇪", "belize": "🇧🇿",
    "bolivia": "🇧🇴", "bosnia": "🇧🇦", "brazil": "🇧🇷", "bulgaria": "🇧🇬", "cambodia": "🇰🇭",
    "cameroon": "🇨🇲", "canada": "🇨🇦", "chile": "🇨🇱", "china": "🇨🇳", "colombia": "🇨🇴",
    "costa rica": "🇨🇷", "croatia": "🇭🇷", "cuba": "🇨🇺", "cyprus": "🇨🇾", "czech republic": "🇨🇿",
    "denmark": "🇩🇰", "ecuador": "🇪🇨", "egypt": "🇪🇬", "estonia": "🇪🇪", "ethiopia": "🇪🇹",
    "finland": "🇫🇮", "france": "🇫🇷", "georgia": "🇬🇪", "germany": "🇩🇪", "ghana": "🇬🇭",
    "greece": "🇬🇷", "guatemala": "🇬🇹", "honduras": "🇭🇳", "hungary": "🇭🇺", "iceland": "🇮🇸",
    "india": "🇮🇳", "indonesia": "🇮🇩", "iran": "🇮🇷", "iraq": "🇮🇶", "ireland": "🇮🇪",
    "israel": "🇮🇱", "italy": "🇮🇹", "jamaica": "🇯🇲", "japan": "🇯🇵", "jordan": "🇯🇴",
    "kazakhstan": "🇰🇿", "kenya": "🇰🇪", "kuwait": "🇰🇼", "latvia": "🇱🇻", "lebanon": "🇱🇧",
    "libya": "🇱🇾", "lithuania": "🇱🇹", "luxembourg": "🇱🇺", "malaysia": "🇲🇾", "mexico": "🇲🇽",
    "morocco": "🇲🇦", "nepal": "🇳🇵", "netherlands": "🇳🇱", "new zealand": "🇳🇿", "nigeria": "🇳🇬",
    "north korea": "🇰🇵", "norway": "🇳🇴", "oman": "🇴🇲", "pakistan": "🇵🇰", "palestine": "🇵🇸",
    "panama": "🇵🇦", "paraguay": "🇵🇾", "peru": "🇵🇪", "philippines": "🇵🇭", "poland": "🇵🇱",
    "portugal": "🇵🇹", "qatar": "🇶🇦", "romania": "🇷🇴", "russia": "🇷🇺", "saudi arabia": "🇸🇦",
    "serbia": "🇷🇸", "singapore": "🇸🇬", "slovakia": "🇸🇰", "slovenia": "🇸🇮", "somalia": "🇸🇴",
    "south africa": "🇿🇦", "south korea": "🇰🇷", "spain": "🇪🇸", "sri lanka": "🇱🇰", "sudan": "🇸🇩",
    "sweden": "🇸🇪", "switzerland": "🇨🇭", "syria": "🇸🇾", "taiwan": "🇹🇼", "tajikistan": "🇹🇯",
    "thailand": "🇹🇭", "tunisia": "🇹🇳", "turkey": "🇹🇷", "turkmenistan": "🇹🇲", "uganda": "🇺🇬",
    "ukraine": "🇺🇦", "united arab emirates": "🇦🇪", "uae": "🇦🇪", "united kingdom": "🇬🇧", "uk": "🇬🇧",
    "united states": "🇺🇸", "usa": "🇺🇸", "uruguay": "🇺🇾", "uzbekistan": "🇺🇿", "venezuela": "🇻🇪",
    "vietnam": "🇻🇳", "yemen": "🇾🇪", "zambia": "🇿🇲", "zimbabwe": "🇿🇼", "el salvador": "🇸🇻"
}

def get_country_flag(country_name: str) -> str:
    key = country_name.strip().lower()
    return COUNTRY_FLAGS.get(key, "🏳️")

def check_user(update: Update) -> bool:
    user = update.effective_user
    if not user or not user.username:
        return False
    return user.username.lower() == ALLOWED_TELEGRAM_USER.lower()

def get_main_reply_keyboard():
    return ReplyKeyboardMarkup(
        [
            [KeyboardButton("💰 Balance"), KeyboardButton("🎯 Target")],
            [KeyboardButton("📦 Stock Number")]
        ],
        resize_keyboard=True
    )

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not check_user(update):
        return

    user_id = update.effective_user.id
    if user_id in active_sessions:
        active_sessions[user_id]["status"] = "stopped"

    menu_markup = get_main_reply_keyboard()
    text = "👋 Welcome to Telegram OTP Bot!\nPlease choose an option below:"
    
    if update.message:
        await update.message.reply_text(text, reply_markup=menu_markup)
    elif update.callback_query:
        query = update.callback_query
        await query.answer()
        await query.message.reply_text(text, reply_markup=menu_markup)

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not check_user(update): return
    menu_markup = get_main_reply_keyboard()
    await update.message.reply_text(
        "📖 **How to Use:**\n\n"
        "1. Click on `🎯 Target`.\n"
        "2. Send country name(s) (e.g., `Cuba, Ukraine` or `United Kingdom`).\n"
        "3. Control the process anytime using Pause or Stop buttons.",
        parse_mode="Markdown",
        reply_markup=menu_markup
    )

async def balance_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not check_user(update): return
    menu_markup = get_main_reply_keyboard()
    try:
        url = f"{BASE_URL}/getUserInfo?name={PANEL_USERNAME}&ApiKey={PANEL_API_KEY}"
        res = requests.get(url, timeout=15).json()
        if res.get("code") == 200:
            d = res.get("data", {})
            await update.message.reply_text(
                f"👤 **User Information:**\n"
                f"• Username: `{d.get('username')}`\n"
                f"• Balance/Score: `{d.get('score')}`",
                parse_mode="Markdown",
                reply_markup=menu_markup
            )
        else:
            await update.message.reply_text(f"❌ Error: {res.get('msg')}", reply_markup=menu_markup)
    except Exception as e:
        await update.message.reply_text(f"❌ Error: {e}", reply_markup=menu_markup)

async def stock_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not check_user(update): return
    menu_markup = get_main_reply_keyboard()
    try:
        url = f"{BASE_URL}/getStock?name={PANEL_USERNAME}&ApiKey={PANEL_API_KEY}&pid={TELEGRAM_PROJECT_ID}"
        res = requests.get(url, timeout=15).json()
        await update.message.reply_text(
            f"📦 **Stock Information:**\n<code>{res}</code>",
            parse_mode="HTML",
            reply_markup=menu_markup
        )
    except Exception as e:
        await update.message.reply_text(f"❌ Stock Error: {e}", reply_markup=menu_markup)

async def target_prompt(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not check_user(update): return ConversationHandler.END
    menu_markup = get_main_reply_keyboard()
    await update.message.reply_text(
        "🎯 **Target Mode**\n\n"
        "Send country name(s) to start collecting numbers continuously.\n\n"
        "Examples:\n"
        "United Kingdom\n"
        "Syria, Fiji\n"
        "Egypt, United States, Canada",
        parse_mode="Markdown",
        reply_markup=menu_markup
    )
    return STATE_TARGET_CUY

async def target_exec(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not check_user(update):
        return ConversationHandler.END
        
    cuy_input = update.message.text.strip()
    user_id = update.effective_user.id
    menu_markup = get_main_reply_keyboard()
    
    if cuy_input.lower() in ["/cancel", "stop running process", "stop"]:
        if user_id in active_sessions:
            active_sessions[user_id]["status"] = "stopped"
        await update.message.reply_text(f"⏹️ **Target Stopped**", parse_mode="Markdown", reply_markup=menu_markup)
        return ConversationHandler.END

    countries = [c.strip() for c in cuy_input.split(",") if c.strip()]
    flags_str = " ".join([get_country_flag(c) for c in countries])
    display_cuy = ", ".join(countries)

    control_keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("⏸ Pause", callback_data="pause_process"),
            InlineKeyboardButton("⏹️ Stop", callback_data="stop_process")
        ]
    ])

    active_sessions[user_id] = {"status": "running"}

    # কন্টিনিউয়াস লুপ: ব্যবহারকারী স্টপ না করা পর্যন্ত নাম্বার বাই করতেই থাকবে
    while True:
        if user_id not in active_sessions or active_sessions[user_id]["status"] == "stopped":
            break

        status_msg = await update.message.reply_text(
            f"🎯 **Target Running**\n\n"
            f"▶️ {flags_str} {display_cuy}\n\n"
            f"⏳ Searching for a new number...",
            reply_markup=control_keyboard,
            parse_mode="Markdown"
        )

        phone_number = None
        request_count = 0
        got_count = 0

        while not phone_number:
            if user_id not in active_sessions or active_sessions[user_id]["status"] == "stopped":
                break

            while user_id in active_sessions and active_sessions[user_id]["status"] == "paused":
                await asyncio.sleep(1)
                if user_id not in active_sessions or active_sessions[user_id]["status"] == "stopped":
                    break

            if user_id not in active_sessions or active_sessions[user_id]["status"] == "stopped":
                break

            try:
                for cuy in countries:
                    api_url = f"{BASE_URL}/getMobile?name={PANEL_USERNAME}&ApiKey={PANEL_API_KEY}&cuy={cuy}&pid={TELEGRAM_PROJECT_ID}&num=1&noblack=0&serial=2&secret_key=&vip="
                    res = requests.get(api_url, timeout=5)
                    request_count += 1
                    data = res.json()
                    
                    if data.get("code") == 200:
                        phone_number = data.get('data')
                        got_count += 1
                        break
                
                await status_msg.edit_text(
                    f"🎯 **Target Running**\n\n"
                    f"▶️ {flags_str} {display_cuy}\n\n"
                    f"📡 Requests: {request_count} | ✅ Got: {got_count} | ⚡ 300/min\n"
                    f"⏳ Active searching...",
                    reply_markup=control_keyboard,
                    parse_mode="Markdown"
                )
            except Exception:
                request_count += 1

            await asyncio.sleep(0.3)

        if user_id not in active_sessions or active_sessions[user_id]["status"] == "stopped":
            break

        release_keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("📋 Copy Number", callback_data=f"copy_{phone_number}")],
            [InlineKeyboardButton("🗑️ Release", callback_data=f"release_{phone_number}")]
        ])

        total_seconds = 300 
        sent_msg = None
        otp_received = False
        otp_code = None

        for remaining in range(total_seconds, -1, -1):
            if user_id not in active_sessions or active_sessions[user_id]["status"] == "stopped":
                break

            while user_id in active_sessions and active_sessions[user_id]["status"] == "paused":
                await asyncio.sleep(1)
                if user_id not in active_sessions or active_sessions[user_id]["status"] == "stopped":
                    break

            minutes = remaining // 60
            seconds = remaining % 60
            timer_str = f"{minutes}:{seconds:02d}"

            try:
                otp_url = f"{BASE_URL}/getMsg?name={PANEL_USERNAME}&ApiKey={PANEL_API_KEY}&pn={phone_number}&pid={TELEGRAM_PROJECT_ID}&serial=2"
                otp_res = requests.get(otp_url, timeout=3).json()
                
                if otp_res.get("code") == 200 and otp_res.get("data"):
                    otp_code = otp_res.get("data")
                    otp_received = True
                    break
            except Exception:
                pass

            message_text = (
                f"Telegram {flags_str} `{phone_number}`\n\n"
                f"⏳ {timer_str}"
            )

            if sent_msg is None:
                try:
                    await status_msg.delete()
                except Exception:
                    pass

                sent_msg = await update.message.reply_text(
                    message_text,
                    reply_markup=release_keyboard,
                    parse_mode="Markdown"
                )
            else:
                try:
                    await sent_msg.edit_text(message_text, reply_markup=release_keyboard, parse_mode="Markdown")
                except Exception:
                    pass

            await asyncio.sleep(1)

        if user_id not in active_sessions or active_sessions[user_id]["status"] == "stopped":
            break

        if otp_received and otp_code:
            updated_text = (
                f"✅ **OTP Received!**\n\n"
                f"📱 Number: ~~{phone_number}~~\n"
                f"🔑 OTP Code: `{otp_code}`"
            )
            otp_keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton("📋 Copy OTP", callback_data=f"copyotp_{otp_code}")]
            ])
            try:
                if sent_msg:
                    await sent_msg.edit_text(updated_text, reply_markup=otp_keyboard, parse_mode="Markdown")
            except Exception:
                pass
        else:
            try:
                expired_text = f"⌛ **Expired:** Time is up! Number `{phone_number}` has been deleted. Moving to next..."
                if sent_msg:
                    await sent_msg.edit_text(expired_text, parse_mode="Markdown")
            except Exception:
                pass
        
        # একটু বিরতি দিয়ে আবার পরের নাম্বার খোঁজা শুরু করবে
        await asyncio.sleep(1)

    return ConversationHandler.END

async def inline_actions(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    data = query.data

    if data.startswith("copy_"):
        await query.answer()
        num = data.split("_")[1]
        await query.answer(f"Number Copied: {num}", show_alert=True)
    elif data.startswith("copyotp_"):
        await query.answer()
        otp = data.split("_")[1]
        await query.answer(f"OTP Copied: {otp}", show_alert=True)
    elif data == "pause_process":
        if user_id in active_sessions:
            active_sessions[user_id]["status"] = "paused"
        
        resume_keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("▶️ Resume", callback_data="resume_process"),
                InlineKeyboardButton("⏹️ Stop", callback_data="stop_process")
            ]
        ])
        try:
            await query.message.edit_reply_markup(reply_markup=resume_keyboard)
        except Exception:
            pass
        await query.answer("⏸️ Process Paused", show_alert=True)

    elif data == "resume_process":
        if user_id in active_sessions:
            active_sessions[user_id]["status"] = "running"
        
        control_keyboard = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("⏸️ Pause", callback_data="pause_process"),
                InlineKeyboardButton("⏹️ Stop", callback_data="stop_process")
            ]
        ])
        try:
            await query.message.edit_reply_markup(reply_markup=control_keyboard)
        except Exception:
            pass
        await query.answer("▶️ Process Resumed", show_alert=True)

    elif data == "stop_process":
        if user_id in active_sessions:
            active_sessions[user_id]["status"] = "stopped"
        try:
            await query.message.edit_text("⏹️ **Target Stopped**", parse_mode="Markdown")
        except Exception:
            pass
        try:
            await query.answer("Target Stopped Successfully", show_alert=True)
        except Exception:
            pass
        await start(update, context)

    elif data.startswith("release_"):
        await query.answer()
        try:
            await query.message.edit_text("🗑️ Number released successfully.")
        except Exception:
            pass

async def cancel(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id in active_sessions:
        active_sessions[user_id]["status"] = "stopped"
    menu_markup = get_main_reply_keyboard()
    await update.message.reply_text("⏹️ **Target Stopped**", parse_mode="Markdown", reply_markup=menu_markup)
    return ConversationHandler.END

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("cancel", cancel))

    app.add_handler(MessageHandler(filters.Regex("^💰 Balance$"), balance_handler))
    app.add_handler(MessageHandler(filters.Regex("^📦 Stock Number$"), stock_handler))
    app.add_handler(MessageHandler(filters.Regex("^restart the bot$"), start))
    app.add_handler(MessageHandler(filters.Regex("^How to use$"), help_command))
    app.add_handler(MessageHandler(filters.Regex("^stop running process$"), cancel))

    target_conv_handler = ConversationHandler(
        entry_points=[MessageHandler(filters.Regex("^🎯 Target$"), target_prompt)],
        states={
            STATE_TARGET_CUY: [MessageHandler(filters.TEXT & ~filters.COMMAND, target_exec)],
        },
        fallbacks=[CommandHandler("cancel", cancel), MessageHandler(filters.Regex("^stop running process$"), cancel)],
    )

    app.add_handler(target_conv_handler)
    app.add_handler(CallbackQueryHandler(inline_actions, pattern="^(copy_|copyotp_|release_|pause_process|resume_process|stop_process)"))

    print("🤖 Continuous Bot is running...")
    app.run_polling()

