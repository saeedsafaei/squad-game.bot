# pip install python-telegram-bot>=20.0

import asyncio
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackQueryHandler, ContextTypes, filters

# 🔴 توکن بات تلگرام
BOT_TOKEN = "8348439329:AAHAgXHamWVOOk26z_rLeRjvkL_PY56_Ovk"

# 📢 شناسه کانال برای ارسال آگهی (مثال: @your_channel یا -1001234567890)
CHANNEL_ID = "https://t.me/shap_SquidGame"  # این را با شناسه کانال خود جایگزین کنید

# 📢 شناسه کانال برای ارسال آگهی (مثال: @your_channel یا -1001234567890)
CHANNEL_ID = "https://t.me/shap_SquidGame"  # این را با شناسه کانال خود جایگزین کنید

# 📸 URL عکس تبلیغاتی - می‌توانید این را با آدرس عکس خودتان جایگزین کنید
AD_IMAGE_URL = "https://images.unsplash.com/photo-1550745165-9bc0b252726f?w=800"  # مثال - جایگزین کنید

# متن تبلیغاتی
AD_TEXT = """
🎮 **خرید و فروش اکانت کالاف دیوتی موبایل**

✨ اکانت‌های با کیفیت و معتبر
💰 قیمت‌های مناسب و رقابتی
🔒 تضمین امنیت و سلامت اکانت
⚡ تحویل فوری پس از خرید

📱 برای خرید یا فروش اکانت، با ما در ارتباط باشید!
"""

# متن توضیحات پروفایل بات (About)
BOT_DESCRIPTION = """🎮 خرید و فروش اکانت کالاف دیوتی موبایل

✨ اکانت‌های با کیفیت و معتبر
💰 قیمت‌های مناسب و رقابتی
🔒 تضمین امنیت و سلامت اکانت
⚡ تحویل فوری پس از خرید

📱 برای خرید یا فروش اکانت، با ما در ارتباط باشید!"""

# متن توضیحات کوتاه (Short Description)
BOT_SHORT_DESCRIPTION = "🎮 خرید و فروش اکانت کالاف دیوتی موبایل | اکانت‌های معتبر و با کیفیت"

# متن خوش‌آمدگویی
WELCOME_TEXT = """
👋 **خوش آمدید!**

به بات خرید و فروش اکانت کالاف دیوتی موبایل خوش آمدید.

لطفاً یکی از گزینه‌های زیر را انتخاب کنید:
"""

def create_main_keyboard():
    """ساخت کیبورد کنترل پنل"""
    keyboard = [
        [KeyboardButton("1️⃣ فروش اکانت"), KeyboardButton("2️⃣ گپ واسطه گری")],
        [KeyboardButton("3️⃣ درباره ما"), KeyboardButton("4️⃣ ارتباط با ما")],
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)

def create_back_keyboard():
    """ساخت کیبورد با دکمه بازگشت به صفحه اصلی"""
    keyboard = [
        [KeyboardButton("🔙 بازگشت به صفحه اصلی")],
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=False)

def create_region_keyboard():
    """ساخت کیبورد شناور برای انتخاب ریجن"""
    keyboard = [
        [InlineKeyboardButton("🇮🇷 ایران", callback_data="region_iran")],
        [InlineKeyboardButton("🇮🇳 هند", callback_data="region_india")],
        [InlineKeyboardButton("🇪🇺 اروپا", callback_data="region_europe")],
    ]
    return InlineKeyboardMarkup(keyboard)

def create_exchange_keyboard():
    """ساخت کیبورد شناور برای سوال معاوضه"""
    keyboard = [
        [InlineKeyboardButton("✅ بله", callback_data="exchange_yes")],
        [InlineKeyboardButton("❌ خیر", callback_data="exchange_no")],
    ]
    return InlineKeyboardMarkup(keyboard)

def create_ad_confirmation_keyboard():
    """ساخت کیبورد شناور برای تایید یا حذف آگهی"""
    keyboard = [
        [InlineKeyboardButton("✅ تایید آگهی", callback_data="ad_confirm")],
        [InlineKeyboardButton("❌ حذف آگهی", callback_data="ad_delete")],
    ]
    return InlineKeyboardMarkup(keyboard)

def create_ad_text(context_data):
    """ساخت متن آگهی از اطلاعات جمع‌آوری شده"""
    # تبدیل region_code به نام فارسی
    region_code = context_data.get('region', '')
    region_display = {
        'iran': '🇮🇷 ایران',
        'india': '🇮🇳 هند',
        'europe': '🇪🇺 اروپا'
    }.get(region_code, 'نامشخص')
    
    # تبدیل wants_exchange به متن فارسی
    wants_exchange = context_data.get('wants_exchange', False)
    exchange_display = "✅ بله" if wants_exchange else "❌ خیر"
    
    ad_text = f"""🎮 **اکانت کالاف دیوتی موبایل**

📍 **ریجن:** {region_display}
🔗 **نوع لینک:** {context_data.get('link_type', 'نامشخص')}
💎 **تعداد CP:** {context_data.get('cp_count', 'نامشخص'):,}
🎮 **وضعیت بتل پس:** {context_data.get('battlepass_status', 'نامشخص')}
💰 **قیمت:** {context_data.get('price_toman', 'نامشخص'):,} تومان
🔄 **معاوضه:** {exchange_display}

📝 **توضیحات:**
{context_data.get('account_description', 'بدون توضیحات')}

👤 **فروشنده:** {context_data.get('seller_id', 'نامشخص')}

━━━━━━━━━━━━━━━━━━━━
#فروش_اکانت #کالاف_دیوتی #اکانت_کالاف"""
    
    return ad_text

async def send_advertisement(update: Update, context: ContextTypes.DEFAULT_TYPE, show_keyboard: bool = False) -> None:
    """ارسال پیام تبلیغاتی با عکس"""
    reply_markup = create_main_keyboard() if show_keyboard else None
    try:
        await update.message.reply_photo(
            photo=AD_IMAGE_URL,
            caption=AD_TEXT,
            parse_mode="Markdown",
            reply_markup=reply_markup
        )
    except Exception as e:
        # اگر عکس لود نشد، فقط متن را ارسال کن
        await update.message.reply_text(AD_TEXT, parse_mode="Markdown", reply_markup=reply_markup)

async def start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """هندلر دستور /start - نمایش تبلیغ و کیبورد"""
    # پاک کردن state قبلی
    context.user_data.pop("state", None)
    context.user_data.pop("media_file_id", None)
    context.user_data.pop("media_type", None)
    context.user_data.pop("region", None)
    context.user_data.pop("link_type", None)
    context.user_data.pop("cp_count", None)
    context.user_data.pop("battlepass_status", None)
    context.user_data.pop("account_description", None)
    context.user_data.pop("price", None)
    
    # ارسال تبلیغ با کیبورد
    await send_advertisement(update, context, show_keyboard=True)
    
    # ارسال پیام خوش‌آمدگویی با کیبورد
    await update.message.reply_text(
        WELCOME_TEXT,
        reply_markup=create_main_keyboard(),
        parse_mode="Markdown"
    )

async def account_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """هندلر دستور /account - نمایش پیام اکانت"""
    await update.message.reply_text("اکانت")

async def cancel_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """هندلر دستور /cancel - لغو عملیات جاری و بازگشت به صفحه اصلی"""
    context.user_data.pop("state", None)
    context.user_data.pop("media_file_id", None)
    context.user_data.pop("media_type", None)
    context.user_data.pop("region", None)
    context.user_data.pop("link_type", None)
    context.user_data.pop("cp_count", None)
    context.user_data.pop("battlepass_status", None)
    context.user_data.pop("account_description", None)
    context.user_data.pop("price", None)
    
    await update.message.reply_text(
        "❌ عملیات لغو شد.\n\n"
        "🏠 **صفحه اصلی**\n\n"
        "لطفاً یکی از گزینه‌های زیر را انتخاب کنید:",
        reply_markup=create_main_keyboard(),
        parse_mode="Markdown"
    )

async def media_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """هندلر دریافت عکس، فیلم یا گیف برای فروش اکانت"""
    user_state = context.user_data.get("state")
    
    if user_state == "waiting_for_media":
        # بررسی اینکه آیا پیام حاوی عکس، فیلم یا گیف است
        if update.message.photo:
            media_type = "عکس"
            file_id = update.message.photo[-1].file_id
        elif update.message.video:
            media_type = "فیلم"
            file_id = update.message.video.file_id
        elif update.message.animation:  # گیف
            media_type = "گیف"
            file_id = update.message.animation.file_id
        elif update.message.document:
            # بررسی اینکه آیا document یک گیف است
            if update.message.document.mime_type and "gif" in update.message.document.mime_type:
                media_type = "گیف"
                file_id = update.message.document.file_id
            else:
                await update.message.reply_text(
                    "⚠️ لطفاً فقط عکس، فیلم یا گیف ارسال کنید.",
                    parse_mode="Markdown"
                )
                return
        else:
            await update.message.reply_text(
                "⚠️ لطفاً یک عکس، فیلم یا گیف ارسال کنید.",
                parse_mode="Markdown"
            )
            return
        
        # دریافت موفقیت‌آمیز
        context.user_data["media_file_id"] = file_id
        context.user_data["media_type"] = media_type
        context.user_data["state"] = "waiting_for_region"
        
        await update.message.reply_text(
            f"✅ {media_type} شما با موفقیت دریافت شد!\n\n"
            "🌍 لطفاً **ریجن اکانت** خود را انتخاب کنید:",
            reply_markup=create_region_keyboard(),
            parse_mode="Markdown"
        )
    else:
        # اگر state مناسب نیست، تبلیغ نمایش بده با کیبورد
        await send_advertisement(update, context, show_keyboard=True)

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """هندلر پیام‌های متنی - پردازش دکمه‌های کنترل پنل"""
    user_state = context.user_data.get("state")
    message_text = update.message.text
    
    # اگر کاربر در حال فروش اکانت است و نوع لینک شدن را وارد می‌کند
    if user_state == "waiting_for_link_type":
        # ذخیره نوع لینک شدن
        context.user_data["link_type"] = message_text
        context.user_data["state"] = "waiting_for_cp"
        
        await update.message.reply_text(
            f"✅ نوع لینک شدن شما: **{message_text}**\n\n"
            "💎 **تعداد CP (Credit Points) اکانت خود را وارد کنید:**",
            reply_markup=create_back_keyboard(),
            parse_mode="Markdown"
        )
    # اگر کاربر در حال فروش اکانت است و تعداد CP را وارد می‌کند
    elif user_state == "waiting_for_cp":
        # بررسی اینکه آیا ورودی عدد است
        try:
            cp_count = int(message_text)
            # ذخیره تعداد CP
            context.user_data["cp_count"] = cp_count
            context.user_data["state"] = "waiting_for_battlepass"
            
            await update.message.reply_text(
                f"✅ تعداد CP شما: **{cp_count:,}**\n\n"
                "🎮 **وضعیت بتل پس اکانت خود را وارد کنید:**\n\n"
                "مثال: فعال، غیرفعال، سطح 50، کامل و ...",
                reply_markup=create_back_keyboard(),
                parse_mode="Markdown"
            )
        except ValueError:
            await update.message.reply_text(
                "⚠️ لطفاً یک عدد معتبر برای تعداد CP وارد کنید.\n\n"
                "مثال: 5000 یا 10000",
                reply_markup=create_back_keyboard(),
                parse_mode="Markdown"
            )
    # اگر کاربر در حال فروش اکانت است و وضعیت بتل پس را وارد می‌کند
    elif user_state == "waiting_for_battlepass":
        # ذخیره وضعیت بتل پس
        context.user_data["battlepass_status"] = message_text
        context.user_data["state"] = "waiting_for_description"
        
        await update.message.reply_text(
            f"✅ وضعیت بتل پس شما: **{message_text}**\n\n"
            "📝 **توضیحات اکانت خود را وارد کنید:**\n\n"
            "می‌توانید اطلاعاتی مانند:\n"
            "• سطح اکانت\n"
            "• آیتم‌های موجود\n"
            "• ویژگی‌های خاص\n"
            "• و هر توضیح دیگری که فکر می‌کنید مهم است",
            reply_markup=create_back_keyboard(),
            parse_mode="Markdown"
        )
    # اگر کاربر در حال فروش اکانت است و توضیحات اکانت را وارد می‌کند
    elif user_state == "waiting_for_description":
        # ذخیره توضیحات اکانت
        context.user_data["account_description"] = message_text
        context.user_data["state"] = "waiting_for_price"
        
        await update.message.reply_text(
            f"✅ توضیحات شما دریافت شد.\n\n"
            "💰 **قیمت پیشنهادی خود را وارد کنید:**\n\n"
            "مثال: 500000 تومان یا 100 دلار",
            reply_markup=create_back_keyboard(),
            parse_mode="Markdown"
        )
    # اگر کاربر در حال فروش اکانت است و قیمت را وارد می‌کند
    elif user_state == "waiting_for_price":
        # ذخیره قیمت
        context.user_data["price"] = message_text
        context.user_data["state"] = "waiting_for_exchange"
        
        await update.message.reply_text(
            f"✅ قیمت پیشنهادی شما: **{message_text}**\n\n"
            "🔄 **آیا مایل به معاوضه اکانت خود با اکانت دیگر هستید؟**",
            reply_markup=create_exchange_keyboard(),
            parse_mode="Markdown"
        )
    # اگر کاربر در حال فروش اکانت است و قیمت به تومان را وارد می‌کند
    elif user_state == "waiting_for_price_toman":
        # بررسی اینکه آیا ورودی عدد است
        try:
            price_toman = int(message_text.replace(',', '').replace('،', ''))
            # ذخیره قیمت به تومان
            context.user_data["price_toman"] = price_toman
            context.user_data["state"] = "waiting_for_seller_id"
            
            await update.message.reply_text(
                f"✅ قیمت شما: **{price_toman:,} تومان**\n\n"
                "👤 **ایدی فروشنده را وارد کنید:**\n\n"
                "مثال: @username یا 123456789",
                reply_markup=create_back_keyboard(),
                parse_mode="Markdown"
            )
        except ValueError:
            await update.message.reply_text(
                "⚠️ لطفاً یک عدد معتبر برای قیمت به تومان وارد کنید.\n\n"
                "مثال: 500000 یا 1000000",
                reply_markup=create_back_keyboard(),
                parse_mode="Markdown"
            )
    # اگر کاربر در حال فروش اکانت است و ایدی فروشنده را وارد می‌کند
    elif user_state == "waiting_for_seller_id":
        # ذخیره ایدی فروشنده
        context.user_data["seller_id"] = message_text
        context.user_data["state"] = "waiting_for_ad_confirmation"
        
        # ساخت متن آگهی
        ad_text = create_ad_text(context.user_data)
        media_file_id = context.user_data.get('media_file_id')
        media_type = context.user_data.get('media_type', 'عکس')
        
        # نمایش آگهی به کاربر
        try:
            if media_type == "عکس" and media_file_id:
                await update.message.reply_photo(
                    photo=media_file_id,
                    caption=ad_text,
                    reply_markup=create_ad_confirmation_keyboard(),
                    parse_mode="Markdown"
                )
            elif media_type == "فیلم" and media_file_id:
                await update.message.reply_video(
                    video=media_file_id,
                    caption=ad_text,
                    reply_markup=create_ad_confirmation_keyboard(),
                    parse_mode="Markdown"
                )
            elif media_type == "گیف" and media_file_id:
                await update.message.reply_animation(
                    animation=media_file_id,
                    caption=ad_text,
                    reply_markup=create_ad_confirmation_keyboard(),
                    parse_mode="Markdown"
                )
            else:
                await update.message.reply_text(
                    ad_text,
                    reply_markup=create_ad_confirmation_keyboard(),
                    parse_mode="Markdown"
                )
        except Exception as e:
            # اگر خطا در ارسال فایل بود، فقط متن را ارسال کن
            await update.message.reply_text(
                ad_text,
                reply_markup=create_ad_confirmation_keyboard(),
                parse_mode="Markdown"
            )
        
        await update.message.reply_text(
            "👆 **پیش‌نمایش آگهی شما**\n\n"
            "لطفاً آگهی را بررسی کنید و یکی از گزینه‌های زیر را انتخاب کنید:",
            reply_markup=create_back_keyboard(),
            parse_mode="Markdown"
        )
    # اگر کاربر در حال فروش اکانت است و اطلاعات می‌فرستد
    elif user_state == "media_received":
        # اینجا می‌توانید اطلاعات را پردازش کنید
        # فعلاً فقط تأیید می‌کنیم
        await update.message.reply_text(
            "✅ اطلاعات شما دریافت شد. به زودی با شما تماس خواهیم گرفت.\n\n"
            "لطفاً یکی از گزینه‌های زیر را انتخاب کنید:",
            reply_markup=create_main_keyboard(),
            parse_mode="Markdown"
        )
        # پاک کردن state
        context.user_data.pop("state", None)
        context.user_data.pop("media_file_id", None)
        context.user_data.pop("media_type", None)
        context.user_data.pop("region", None)
        context.user_data.pop("link_type", None)
        context.user_data.pop("cp_count", None)
        context.user_data.pop("battlepass_status", None)
        context.user_data.pop("account_description", None)
        context.user_data.pop("price", None)
        context.user_data.pop("price_toman", None)
        context.user_data.pop("wants_exchange", None)
        context.user_data.pop("seller_id", None)
    # پردازش دکمه‌های کنترل پنل
    elif message_text == "1️⃣ فروش اکانت":
        # تنظیم state برای دریافت عکس/فیلم/گیف
        context.user_data["state"] = "waiting_for_media"
        
        await update.message.reply_text(
            "💰 **فروش اکانت**\n\n"
            "📸 لطفاً یک **عکس، فیلم یا گیف** از اکانت خود ارسال کنید.\n\n"
            "این فایل می‌تواند شامل:\n"
            "• اسکرین‌شات از اکانت\n"
            "• ویدیو از گیم‌پلی\n"
            "• گیف از آیتم‌های اکانت\n\n"
            "⏳ منتظر دریافت فایل شما هستیم...",
            reply_markup=create_back_keyboard(),
            parse_mode="Markdown"
        )
    elif message_text == "🔙 بازگشت به صفحه اصلی":
        # پاک کردن state و بازگشت به صفحه اصلی
        context.user_data.pop("state", None)
        context.user_data.pop("media_file_id", None)
        context.user_data.pop("media_type", None)
        context.user_data.pop("region", None)
        context.user_data.pop("link_type", None)
        context.user_data.pop("cp_count", None)
        context.user_data.pop("battlepass_status", None)
        context.user_data.pop("account_description", None)
        context.user_data.pop("price", None)
        context.user_data.pop("price_toman", None)
        context.user_data.pop("wants_exchange", None)
        context.user_data.pop("seller_id", None)
        
        await update.message.reply_text(
            "🏠 **صفحه اصلی**\n\n"
            "لطفاً یکی از گزینه‌های زیر را انتخاب کنید:",
            reply_markup=create_main_keyboard(),
            parse_mode="Markdown"
        )
    elif message_text == "2️⃣ گپ واسطه گری":
        await update.message.reply_text(
            "🤝 **گپ واسطه گری**\n\n"
            "برای دسترسی به گپ واسطه‌گری، لطفاً با پشتیبانی در ارتباط باشید.\n\n"
            "گپ واسطه‌گری برای اطمینان از معاملات امن و مطمئن ایجاد شده است.",
            reply_markup=create_main_keyboard(),
            parse_mode="Markdown"
        )
    elif message_text == "3️⃣ درباره ما":
        await update.message.reply_text(
            "ℹ️ **درباره ما**\n\n"
            "🎮 ما یک تیم متخصص در زمینه خرید و فروش اکانت‌های بازی هستیم.\n\n"
            "✨ **خدمات ما:**\n"
            "• خرید و فروش اکانت‌های معتبر\n"
            "• واسطه‌گری در معاملات\n"
            "• تضمین امنیت و سلامت اکانت‌ها\n"
            "• پشتیبانی 24/7\n\n"
            "🔒 تمام معاملات با تضمین کامل انجام می‌شود.",
            reply_markup=create_main_keyboard(),
            parse_mode="Markdown"
        )
    elif message_text == "4️⃣ ارتباط با ما":
        await update.message.reply_text(
            "📞 **ارتباط با ما**\n\n"
            "برای ارتباط با ما می‌توانید:\n\n"
            "• از طریق همین بات پیام بفرستید\n"
            "• با پشتیبانی در ارتباط باشید\n\n"
            "ما در اسرع وقت پاسخگوی شما خواهیم بود.",
            reply_markup=create_main_keyboard(),
            parse_mode="Markdown"
        )
    else:
        # نمایش تبلیغ برای پیام‌های عادی با کیبورد
        await send_advertisement(update, context, show_keyboard=True)

async def region_callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """هندلر انتخاب ریجن از کیبورد شناور"""
    query = update.callback_query
    await query.answer()  # پاسخ به callback query
    
    # تعیین نام ریجن بر اساس callback_data
    if query.data == "region_iran":
        region_name = "🇮🇷 ایران"
        region_code = "iran"
    elif query.data == "region_india":
        region_name = "🇮🇳 هند"
        region_code = "india"
    elif query.data == "region_europe":
        region_name = "🇪🇺 اروپا"
        region_code = "europe"
    else:
        return
    
    # ذخیره ریجن
    context.user_data["region"] = region_code
    context.user_data["state"] = "waiting_for_link_type"
    
    # ویرایش پیام قبلی
    await query.edit_message_text(
        f"✅ ریجن شما: **{region_name}**",
        parse_mode="Markdown"
    )
    
    # ارسال پیام درخواست نوع لینک شدن
    await query.message.reply_text(
        "🔗 **نوع لینک شدن اکانت خود را وارد کنید...**\n\n"
        "مثال: گوگل پلی، اپل آیدی، گیم سنتر و ...",
        reply_markup=create_back_keyboard(),
        parse_mode="Markdown"
    )

async def exchange_callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """هندلر انتخاب معاوضه از کیبورد شناور"""
    query = update.callback_query
    await query.answer()  # پاسخ به callback query
    
    # تعیین پاسخ بر اساس callback_data
    if query.data == "exchange_yes":
        exchange_answer = "بله"
        exchange_value = True
    elif query.data == "exchange_no":
        exchange_answer = "خیر"
        exchange_value = False
    else:
        return
    
    # ذخیره پاسخ معاوضه
    context.user_data["wants_exchange"] = exchange_value
    context.user_data["state"] = "waiting_for_price_toman"
    
    # ویرایش پیام قبلی
    await query.edit_message_text(
        f"✅ پاسخ شما: **{exchange_answer}**",
        parse_mode="Markdown"
    )
    
    # ارسال پیام درخواست قیمت به تومان
    await query.message.reply_text(
        "💰 **قیمت اکانت را به تومان وارد کنید:**\n\n"
        "مثال: 500000 یا 1000000",
        reply_markup=create_back_keyboard(),
        parse_mode="Markdown"
    )

async def ad_confirmation_callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """هندلر تایید یا حذف آگهی"""
    query = update.callback_query
    await query.answer()  # پاسخ به callback query
    
    if query.data == "ad_confirm":
        # تایید آگهی و ارسال به کانال
        try:
            # ساخت متن آگهی
            ad_text = create_ad_text(context.user_data)
            media_file_id = context.user_data.get('media_file_id')
            media_type = context.user_data.get('media_type', 'عکس')
            
            bot = context.bot
            
            # ارسال آگهی به کانال
            if media_type == "عکس" and media_file_id:
                sent_message = await bot.send_photo(
                    chat_id=CHANNEL_ID,
                    photo=media_file_id,
                    caption=ad_text,
                    parse_mode="Markdown"
                )
            elif media_type == "فیلم" and media_file_id:
                sent_message = await bot.send_video(
                    chat_id=CHANNEL_ID,
                    video=media_file_id,
                    caption=ad_text,
                    parse_mode="Markdown"
                )
            elif media_type == "گیف" and media_file_id:
                sent_message = await bot.send_animation(
                    chat_id=CHANNEL_ID,
                    animation=media_file_id,
                    caption=ad_text,
                    parse_mode="Markdown"
                )
            else:
                sent_message = await bot.send_message(
                    chat_id=CHANNEL_ID,
                    text=ad_text,
                    parse_mode="Markdown"
                )
            
            # ویرایش پیام قبلی
            await query.edit_message_text(
                "✅ **آگهی شما با موفقیت در کانال منتشر شد!**\n\n"
                "به زودی با شما تماس خواهیم گرفت.",
                parse_mode="Markdown"
            )
            
            # پاک کردن state و بازگشت به صفحه اصلی
            context.user_data.pop("state", None)
            context.user_data.pop("media_file_id", None)
            context.user_data.pop("media_type", None)
            context.user_data.pop("region", None)
            context.user_data.pop("link_type", None)
            context.user_data.pop("cp_count", None)
            context.user_data.pop("battlepass_status", None)
            context.user_data.pop("account_description", None)
            context.user_data.pop("price", None)
            context.user_data.pop("price_toman", None)
            context.user_data.pop("wants_exchange", None)
            context.user_data.pop("seller_id", None)
            
            # ارسال پیام بازگشت به صفحه اصلی
            await query.message.reply_text(
                "🏠 **صفحه اصلی**\n\n"
                "لطفاً یکی از گزینه‌های زیر را انتخاب کنید:",
                reply_markup=create_main_keyboard(),
                parse_mode="Markdown"
            )
            
        except Exception as e:
            await query.edit_message_text(
                f"❌ **خطا در ارسال آگهی به کانال:**\n\n"
                f"خطا: {str(e)}\n\n"
                "لطفاً دوباره تلاش کنید یا با پشتیبانی تماس بگیرید.",
                parse_mode="Markdown"
            )
    
    elif query.data == "ad_delete":
        # حذف آگهی
        await query.edit_message_text(
            "❌ **آگهی حذف شد.**\n\n"
            "اگر می‌خواهید دوباره آگهی بسازید، دستور /start را ارسال کنید.",
            parse_mode="Markdown"
        )
        
        # پاک کردن state و بازگشت به صفحه اصلی
        context.user_data.pop("state", None)
        context.user_data.pop("media_file_id", None)
        context.user_data.pop("media_type", None)
        context.user_data.pop("region", None)
        context.user_data.pop("link_type", None)
        context.user_data.pop("cp_count", None)
        context.user_data.pop("battlepass_status", None)
        context.user_data.pop("account_description", None)
        context.user_data.pop("price", None)
        context.user_data.pop("price_toman", None)
        context.user_data.pop("wants_exchange", None)
        context.user_data.pop("seller_id", None)
        
        # ارسال پیام بازگشت به صفحه اصلی
        await query.message.reply_text(
            "🏠 **صفحه اصلی**\n\n"
            "لطفاً یکی از گزینه‌های زیر را انتخاب کنید:",
            reply_markup=create_main_keyboard(),
            parse_mode="Markdown"
        )

async def setup_bot_profile(application: Application) -> None:
    """تنظیم توضیحات پروفایل بات

    ⚠️ تنظیم عکس پروفایل از طریق BotFather انجام می‌شود
    (در حال حاضر Telegram API متدی برای این کار ارائه نمی‌کند).
    """
    bot = application.bot
    try:
        # تنظیم توضیحات کوتاه (Short Description)
        await bot.set_my_short_description(BOT_SHORT_DESCRIPTION)
        print("✅ توضیحات کوتاه بات تنظیم شد")
        
        # تنظیم توضیحات کامل (About/Description)
        await bot.set_my_description(BOT_DESCRIPTION)
        print("✅ توضیحات کامل بات تنظیم شد")
            
    except Exception as e:
        print(f"⚠️ خطا در تنظیم پروفایل بات: {e}")

async def post_init(application: Application) -> None:
    """تابع اجرا شده بعد از راه‌اندازی بات"""
    await setup_bot_profile(application)

def main() -> None:
    application = Application.builder().token(BOT_TOKEN).post_init(post_init).build()

    # هندلر دستور /start - تبلیغ و کیبورد
    application.add_handler(CommandHandler("start", start_handler))
    
    # هندلر دستور /account - نمایش پیام اکانت
    application.add_handler(CommandHandler("account", account_handler))
    
    # هندلر دستور /cancel - لغو عملیات
    application.add_handler(CommandHandler("cancel", cancel_handler))
    
    # هندلر انتخاب ریجن از کیبورد شناور
    application.add_handler(CallbackQueryHandler(region_callback_handler, pattern="^region_"))
    
    # هندلر انتخاب معاوضه از کیبورد شناور
    application.add_handler(CallbackQueryHandler(exchange_callback_handler, pattern="^exchange_"))
    
    # هندلر تایید یا حذف آگهی
    application.add_handler(CallbackQueryHandler(ad_confirmation_callback_handler, pattern="^ad_"))
    
    # هندلر دریافت عکس، فیلم یا گیف (اولویت بالاتر)
    application.add_handler(MessageHandler(
        filters.PHOTO | filters.VIDEO | filters.ANIMATION | filters.Document.ALL,
        media_handler
    ))
    
    # هندلر پیام‌های متنی (غیر از دستورات) - نمایش تبلیغ
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

    print("Bot is running...")
    application.run_polling()

if __name__ == "__main__":
    main()
