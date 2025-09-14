🤖 پُل Telegram Botپُل (Pol) is a Telegram bot designed to act as a secure intermediary between Telegram users and their Google Drive accounts. It allows users to upload files to their Google Drive, manage default upload folders, and optionally shorten the generated Google Drive links using Short.io.✨ Features•Google Drive Integration: Securely connect your Google Drive account using OAuth 2.0.•File Uploads: Upload documents, photos, and other files directly from Telegram to your designated Google Drive folder.•Customizable Upload Folder: Set a specific Google Drive folder for your uploads. The bot can create the folder if it doesn't exist.•Short.io Link Shortening: Automatically shorten Google Drive links using your custom Short.io domain and API key.•Admin Panel: Dedicated commands for administrators to manage users, add/remove other admins, and send broadcast messages.•User Management: Each user's settings (Google Drive refresh token, folder ID, Short.io domain, API key) are securely stored.•Error Handling & Logging: Robust error handling and comprehensive logging for monitoring and debugging.🚀 Getting StartedFollow these steps to set up and run your own پُل bot.1. Prerequisites•Python 3.9+•A Telegram Bot Token from @BotFather•Google Cloud Project with Google Drive API enabled and OAuth 2.0 Client ID (Desktop app type) credentials.•Go to Google Cloud Console•Create a new project or select an existing one.•Navigate to "APIs & Services" > "Library" and enable "Google Drive API".•Navigate to "APIs & Services" > "Credentials".•Click "CREATE CREDENTIALS" > "OAuth client ID".•Select "Desktop app" as the Application type.•Note down your Client ID and Client Secret.•(Optional) A Short.io account and API Key for link shortening.•Go to Short.io•Navigate to "Integrations" > "API Keys" to generate one.2. Installation1.Clone the repository:Copygit clone https://github.com/your_username/pol_telegram_bot.git # Replace with actual repo URL
cd pol_telegram_bot
2.Create a virtual environment (recommended):Copypython3 -m venv venv
source venv/bin/activate  # On Windows: `venv\Scripts\activate`
3.Install dependencies:pip install -r requirements.txt3. Configuration1.Create a .env file:
Copy the .env.example file to .env and fill in your credentials:cp .env.example .env2.Edit .env:
Open the newly created .env file and populate the following variables:Copy# Telegram Bot Token (from BotFather)
TELEGRAM_BOT_TOKEN="YOUR_TELEGRAM_BOT_TOKEN"

# Google Cloud Project Credentials (from Google Cloud Console -> APIs & Services -> Credentials)
# Create an OAuth 2.0 Client ID (Desktop app type)
GOOGLE_CLIENT_ID="YOUR_GOOGLE_CLIENT_ID"
GOOGLE_CLIENT_SECRET="YOUR_GOOGLE_CLIENT_SECRET"

# Short.io API Key (from Short.io dashboard -> Integrations -> API Keys)
SHORTIO_API_KEY="YOUR_SHORTIO_API_KEY"

# Database URL (SQLite example, can be PostgreSQL, MySQL, etc.)
# For SQLite, it will create a file named پل_bot.db in the project root
DATABASE_URL="sqlite:///./پل_bot.db"

# Admin User IDs (comma-separated Telegram user IDs)
# Example: ADMIN_IDS="123456789,987654321"
ADMIN_IDS="YOUR_TELEGRAM_ADMIN_ID_1,YOUR_TELEGRAM_ADMIN_ID_2"
Important: For ADMIN_IDS, make sure to include your own Telegram User ID so you can manage the bot.4. Running the Botpython main.pyThe bot should now be running and polling for updates. You can interact with it on Telegram.📚 UsageUser Commands•/start: Greet the bot and get a welcome message.•/help: Display a list of available commands and their descriptions.•/connect_drive: Initiate the Google Drive connection process. You will receive an authorization URL; click it, grant permissions, and paste the resulting code back to the bot.•/setfolder: Set your default Google Drive folder for uploads. The bot will create the folder if it doesn't exist.•/setdomain: Set your custom Short.io domain (e.g., my.short.io).•/setapikey: Set your Short.io API Key.•File Upload: Simply send any file to the bot, and it will be uploaded to your configured Google Drive folder. If Short.io is configured, a shortened link will also be provided.Admin Commands (Requires ADMIN_IDS to be set in .env)•/addadmin <user_id>: Add a new user as an administrator.•/removeadmin <user_id>: Remove an administrator.•/listusers: List all registered users and their admin status.•/broadcast <message>: Send a message to all users of the bot.🛠️ DevelopmentProject StructureCopyپل_bot/
├── config/
│   └── settings.py         # Configuration management
├── database/
│   ├── db_manager.py       # Database connection and CRUD operations
│   └── models.py           # SQLAlchemy models for User
├── handlers/
│   ├── admin_handlers.py   # Admin-specific command handlers
│   ├── user_handlers.py    # User-specific command handlers and conversation flows
│   └── common_handlers.py  # General commands like /start, /help, and error handling
├── services/
│   ├── google_drive_service.py # Google Drive API interactions
│   └── shortio_service.py      # Short.io API interactions
├── utils/
│   ├── google_auth_flow.py # Google OAuth 2.0 flow management
│   ├── decorators.py       # Custom decorators (e.g., admin_only, authenticated_user)
│   └── logger.py           # Centralized logging setup
├── main.py                 # Bot entry point, handler registration
├── requirements.txt        # Python dependencies
├── .env.example            # Example environment variables
└── README.md               # Project documentation
DatabaseThe bot uses SQLAlchemy with SQLite by default. The database file (پل_bot.db) will be created in the project root. You can configure a different database by changing the DATABASE_URL in your .env file.LoggingLogging is configured to output to the console by default. You can modify utils/logger.py to customize logging behavior (e.g., log to a file).🤝 ContributingContributions are welcome! Please feel free to fork the repository, make your changes, and submit a pull request.📄 LicenseThis project is licensed under the MIT License - see the LICENSE file for details. (Note: A LICENSE file is not included in this output, but should be added to a real project.)📞 SupportFor any questions or issues, please open an issue on the GitHub repository or contact the developer.
