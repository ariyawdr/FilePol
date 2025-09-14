🤖 ربات تلگرام پُل (Pol Bot)

<div dir="rtl">

پلی امن و سریع بین تلگرام و حساب گوگل درایو شما.

پُل (Pol) یک ربات تلگرام است که به عنوان یک واسط امن بین کاربران تلگرام و حساب گوگل درایو آن‌ها عمل می‌کند. این ربات به کاربران اجازه می‌دهد فایل‌های خود را مستقیماً از تلگرام در گوگل درایو آپلود کنند، پوشه پیش‌فرض آپلود را مدیریت کرده و در صورت تمایل، لینک‌های گوگل درایو را با استفاده از سرویس Short.io کوتاه کنند.

</div>

English Version

<div dir="rtl">

✨ ویژگی‌ها

    اتصال به گوگل درایو: اتصال امن به حساب گوگل درایو با استفاده از پروتکل OAuth 2.0.

    آپلود فایل: آپلود مستقیم اسناد، تصاویر، ویدئوها و سایر فایل‌ها از تلگرام به پوشه مشخص‌شده در گوگل درایو.

    پوشه آپلود سفارشی: امکان تعیین یک پوشه دلخواه در گوگل درایو برای آپلودها. اگر پوشه وجود نداشته باشد، ربات آن را ایجاد می‌کند.

    کوتاه‌سازی لینک با Short.io: کوتاه کردن خودکار لینک‌های گوگل درایو با استفاده از دامنه و کلید API شخصی شما در Short.io.

    پنل مدیریت: دستورات ویژه برای مدیران جهت مدیریت کاربران، افزودن/حذف مدیران دیگر و ارسال پیام همگانی.

    مدیریت کاربران: ذخیره‌سازی امن تنظیمات هر کاربر (توکن گوگل درایو، شناسه پوشه، دامنه و کلید API مربوط به Short.io).

    مدیریت خطا و لاگ‌برداری: سیستم جامع مدیریت خطا و ثبت لاگ‌ها برای نظارت و اشکال‌زدایی آسان.

🚀 راه‌اندازی و نصب

برای راه‌اندازی و اجرای ربات پُل، مراحل زیر را دنبال کنید.

۱. پیش‌نیازها

    پایتون +3.9

    توکن ربات تلگرام که از @BotFather دریافت می‌کنید.

    یک پروژه در Google Cloud با API گوگل درایو فعال و اطلاعات OAuth 2.0 Client ID.

        به کنسول Google Cloud بروید.

        یک پروژه جدید بسازید یا یک پروژه موجود را انتخاب کنید.

        به بخش APIs & Services > Library رفته و Google Drive API را فعال کنید.

        به بخش APIs & Services > Credentials بروید.

        روی CREATE CREDENTIALS و سپس OAuth client ID کلیک کنید.

        نوع برنامه را Desktop app انتخاب کنید.

        Client ID و Client Secret خود را یادداشت کنید.

    (اختیاری) یک حساب Short.io و کلید API برای کوتاه‌سازی لینک.

        به Short.io بروید.

        از بخش Integrations > API Keys یک کلید جدید بسازید.

۲. نصب

۱. مخزن پروژه را کلون کنید:
Bash

git clone https://github.com/your_username/pol_telegram_bot.git # URL مخزن خود را جایگزین کنید
cd pol_telegram_bot

۲. یک محیط مجازی ایجاد کنید (توصیه می‌شود):
Bash

python3 -m venv venv
source venv/bin/activate  # در ویندوز: venv\Scripts\activate

۳. وابستگی‌ها را نصب کنید:
Bash

pip install -r requirements.txt

۳. پیکربندی

۱. فایل .env را ایجاد کنید:
فایل .env.example را به .env کپی کرده و اطلاعات خود را در آن وارد کنید.
Bash

cp .env.example .env

۲. فایل .env را ویرایش کنید:
مقادیر زیر را با اطلاعات خود در فایل .env پر کنید:
Ini, TOML

# توکن ربات تلگرام (دریافتی از BotFather)
TELEGRAM_BOT_TOKEN="YOUR_TELEGRAM_BOT_TOKEN"

# اطلاعات پروژه Google Cloud
# (از بخش Google Cloud Console -> APIs & Services -> Credentials)
GOOGLE_CLIENT_ID="YOUR_GOOGLE_CLIENT_ID"
GOOGLE_CLIENT_SECRET="YOUR_GOOGLE_CLIENT_SECRET"

# کلید API سرویس Short.io (اختیاری)
SHORTIO_API_KEY="YOUR_SHORTIO_API_KEY"

# آدرس پایگاه داده (مثال با SQLite، قابل تغییر به PostgreSQL و ...)
# در حالت SQLite، فایلی به نام pol_bot.db در ریشه پروژه ایجاد می‌شود
DATABASE_URL="sqlite:///./pol_bot.db"

# شناسه‌های کاربری مدیران (با کاما از هم جدا شوند)
# مثال: ADMIN_IDS="123456789,987654321"
ADMIN_IDS="YOUR_TELEGRAM_ADMIN_ID_1,YOUR_TELEGRAM_ADMIN_ID_2"

مهم: شناسه کاربری تلگرام خود را حتماً در ADMIN_IDS وارد کنید تا بتوانید ربات را مدیریت کنید.

۴. اجرای ربات

Bash

python main.py

ربات اکنون فعال شده و آماده دریافت دستورات در تلگرام است.

📚 راهنمای استفاده

دستورات کاربر

    /start: نمایش پیام خوشامدگویی.

    /help: نمایش لیست دستورات موجود و توضیحات آن‌ها.

    /connect_drive: شروع فرآیند اتصال به حساب گوگل درایو. یک لینک برای شما ارسال می‌شود؛ روی آن کلیک کرده، دسترسی‌های لازم را تایید کنید و کد نهایی را برای ربات ارسال کنید.

    /setfolder: تنظیم پوشه پیش‌فرض برای آپلود فایل‌ها در گوگل درایو.

    /setdomain: تنظیم دامنه شخصی Short.io (مثال: my.short.io).

    /setapikey: تنظیم کلید API سرویس Short.io.

    آپلود فایل: کافیست هر فایلی را برای ربات ارسال کنید تا در پوشه گوگل درایو شما آپلود شود. اگر Short.io پیکربندی شده باشد، لینک کوتاه نیز دریافت خواهید کرد.

دستورات ادمین

    /addadmin <user_id>: افزودن یک کاربر به لیست مدیران.

    /removeadmin <user_id>: حذف یک کاربر از لیست مدیران.

    /listusers: نمایش لیست تمام کاربران ثبت‌شده و وضعیت مدیریت آن‌ها.

    /broadcast <message>: ارسال یک پیام به تمام کاربران ربات.

🛠️ اطلاعات توسعه‌دهندگان

ساختار پروژه

pol_bot/
├── config/
│   └── settings.py         # مدیریت پیکربندی
├── database/
│   ├── db_manager.py       # مدیریت اتصال به پایگاه داده و عملیات CRUD
│   └── models.py           # مدل‌های SQLAlchemy
├── handlers/
│   ├── admin_handlers.py   # مدیریت دستورات ادمین
│   ├── user_handlers.py    # مدیریت دستورات کاربر
│   └── common_handlers.py  # مدیریت دستورات عمومی و خطاها
├── services/
│   ├── google_drive_service.py # تعامل با Google Drive API
│   └── shortio_service.py      # تعامل با Short.io API
├── utils/
│   ├── google_auth_flow.py # مدیریت فرآیند OAuth 2.0 گوگل
│   ├── decorators.py       # دکوریتورهای سفارشی (مانند admin_only)
│   └── logger.py           # تنظیمات مرکزی لاگ‌برداری
├── main.py                 # نقطه شروع ربات
├── requirements.txt        # وابستگی‌های پایتون
├── .env.example            # فایل نمونه متغیرهای محیطی
└── README.md               # مستندات پروژه

پایگاه داده

ربات به طور پیش‌فرض از SQLite با استفاده از SQLAlchemy استفاده می‌کند. شما می‌توانید با تغییر متغیر DATABASE_URL در فایل .env از پایگاه‌داده‌های دیگر نیز استفاده کنید.

لاگ‌برداری

لاگ‌ها به طور پیش‌فرض در کنسول نمایش داده می‌شوند. برای تغییر این رفتار (مثلاً ذخیره در فایل)، می‌توانید فایل utils/logger.py را ویرایش کنید.

🤝 مشارکت

از مشارکت شما استقبال می‌کنیم! لطفاً مخزن را Fork کرده، تغییرات خود را اعمال و یک Pull Request ارسال کنید.

📄 لایسنس

این پروژه تحت لایسنس MIT منتشر شده است. برای جزئیات بیشتر به فایل LICENSE مراجعه کنید.

📞 پشتیبانی

در صورت وجود هرگونه سوال یا مشکل، لطفاً یک Issue در مخزن گیت‌هاب پروژه ثبت کنید.

</div>

🤖 Pol (پُل) Telegram Bot (English)

A secure and fast bridge between your Telegram and Google Drive account.

Pol (پُل) is a Telegram bot designed to act as a secure intermediary between Telegram users and their Google Drive accounts. It allows users to upload files to their Google Drive, manage default upload folders, and optionally shorten the generated Google Drive links using Short.io.

✨ Features

    Google Drive Integration: Securely connect your Google Drive account using OAuth 2.0.

    File Uploads: Upload documents, photos, and other files directly from Telegram to your designated Google Drive folder.

    Customizable Upload Folder: Set a specific Google Drive folder for your uploads. The bot can create the folder if it doesn't exist.

    Short.io Link Shortening: Automatically shorten Google Drive links using your custom Short.io domain and API key.

    Admin Panel: Dedicated commands for administrators to manage users, add/remove other admins, and send broadcast messages.

    User Management: Each user's settings (Google Drive refresh token, folder ID, Short.io domain, API key) are securely stored.

    Error Handling & Logging: Robust error handling and comprehensive logging for monitoring and debugging.

🚀 Getting Started

Follow these steps to set up and run your own Pol bot.

1. Prerequisites

    Python 3.9+

    A Telegram Bot Token from @BotFather.

    A Google Cloud Project with the Google Drive API enabled and OAuth 2.0 Client ID credentials.

        Go to the Google Cloud Console.

        Create a new project or select an existing one.

        Navigate to APIs & Services > Library and enable the Google Drive API.

        Navigate to APIs & Services > Credentials.

        Click CREATE CREDENTIALS > OAuth client ID.

        Select Desktop app as the Application type.

        Note down your Client ID and Client Secret.

    (Optional) A Short.io account and API Key for link shortening.

        Go to Short.io.

        Navigate to Integrations > API Keys to generate one.

2. Installation

    Clone the repository:
    Bash

git clone https://github.com/your_username/pol_telegram_bot.git # Replace with actual repo URL
cd pol_telegram_bot

Create a virtual environment (recommended):
Bash

python3 -m venv venv
source venv/bin/activate  # On Windows: `venv\Scripts\activate`

Install dependencies:
Bash

    pip install -r requirements.txt

3. Configuration

    Create a .env file by copying the example file:
    Bash

cp .env.example .env

Edit the .env file and fill in your credentials:
Ini, TOML

    # Telegram Bot Token (from BotFather)
    TELEGRAM_BOT_TOKEN="YOUR_TELEGRAM_BOT_TOKEN"

    # Google Cloud Project Credentials (from Google Cloud Console -> APIs & Services -> Credentials)
    GOOGLE_CLIENT_ID="YOUR_GOOGLE_CLIENT_ID"
    GOOGLE_CLIENT_SECRET="YOUR_GOOGLE_CLIENT_SECRET"

    # Short.io API Key (from Short.io dashboard -> Integrations -> API Keys)
    SHORTIO_API_KEY="YOUR_SHORTIO_API_KEY"

    # Database URL (SQLite example, can be PostgreSQL, MySQL, etc.)
    # For SQLite, it will create a file named pol_bot.db in the project root
    DATABASE_URL="sqlite:///./pol_bot.db"

    # Admin User IDs (comma-separated Telegram user IDs)
    # Example: ADMIN_IDS="123456789,987654321"
    ADMIN_IDS="YOUR_TELEGRAM_ADMIN_ID_1,YOUR_TELEGRAM_ADMIN_ID_2"

    Important: For ADMIN_IDS, make sure to include your own Telegram User ID so you can manage the bot.

4. Running the Bot

Bash

python main.py

The bot should now be running and polling for updates. You can interact with it on Telegram.

📚 Usage

User Commands

    /start: Greet the bot and get a welcome message.

    /help: Display a list of available commands and their descriptions.

    /connect_drive: Initiate the Google Drive connection process. You will receive an authorization URL; click it, grant permissions, and paste the resulting code back to the bot.

    /setfolder: Set your default Google Drive folder for uploads.

    /setdomain: Set your custom Short.io domain (e.g., my.short.io).

    /setapikey: Set your Short.io API Key.

    File Upload: Simply send any file to the bot, and it will be uploaded to your configured Google Drive folder. If Short.io is configured, a shortened link will also be provided.

Admin Commands

    /addadmin <user_id>: Add a new user as an administrator.

    /removeadmin <user_id>: Remove an administrator.

    /listusers: List all registered users and their admin status.

    /broadcast <message>: Send a message to all users of the bot.

🛠️ For Developers

Project Structure

pol_bot/
├── config/
│   └── settings.py         # Configuration management
├── database/
│   ├── db_manager.py       # Database connection and CRUD operations
│   └── models.py           # SQLAlchemy models for User
├── handlers/
│   ├── admin_handlers.py   # Admin-specific command handlers
│   ├── user_handlers.py    # User-specific command handlers
│   └── common_handlers.py  # General commands like /start, /help
├── services/
│   ├── google_drive_service.py # Google Drive API interactions
│   └── shortio_service.py      # Short.io API interactions
├── utils/
│   ├── google_auth_flow.py # Google OAuth 2.0 flow management
│   ├── decorators.py       # Custom decorators (e.g., admin_only)
│   └── logger.py           # Centralized logging setup
├── main.py                 # Bot entry point
├── requirements.txt        # Python dependencies
├── .env.example            # Example environment variables
└── README.md               # Project documentation

Database

The bot uses SQLAlchemy with SQLite by default. You can configure a different database by changing the DATABASE_URL in your .env file.

Logging

Logging is configured to output to the console by default. You can modify utils/logger.py to customize logging behavior (e.g., log to a file).

🤝 Contributing

Contributions are welcome! Please feel free to fork the repository, make your changes, and submit a pull request.

📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

📞 Support

For any questions or issues, please open an issue on the GitHub repository.
