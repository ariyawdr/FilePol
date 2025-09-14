# Project Structure and Code Architecture for 'پُل' Telegram Bot

This document outlines the proposed project structure and code architecture for the 'پُل' Telegram bot, based on the detailed specifications provided by the user. The goal is to create a modular, maintainable, and scalable application.

## 1. Directory Structure

The project will follow a standard Python project structure, separating configuration, core logic, handlers, and utilities into distinct directories and files.

```
پل_bot/
├── config/
│   └── settings.py
├── database/
│   └── db_manager.py
│   └── models.py
├── handlers/
│   ├── admin_handlers.py
│   ├── user_handlers.py
│   └── common_handlers.py
├── services/
│   ├── google_drive_service.py
│   └── shortio_service.py
├── utils/
│   ├── google_auth_flow.py
│   ├── decorators.py
│   └── logger.py
├── main.py
├── requirements.txt
├── .env.example
└── README.md
```

## 2. Module Breakdown and Responsibilities

### `main.py`
-   **Responsibility:** Entry point of the application. Initializes the Telegram bot, loads configurations, sets up the database, registers all handlers, and starts the bot polling.

### `config/settings.py`
-   **Responsibility:** Manages all application configurations, including Telegram bot token, Google API credentials, Short.io API key, database connection string, admin user IDs, etc. Utilizes environment variables for sensitive information.

### `database/db_manager.py`
-   **Responsibility:** Handles all database interactions. Provides methods for connecting to the database, creating tables, and performing CRUD operations for `User` and `Admin` models.

### `database/models.py`
-   **Responsibility:** Defines the database models (e.g., `User`, `Admin`, `GoogleDriveAuth`, `UserSettings`) using an ORM (e.g., SQLAlchemy or Peewee).

### `handlers/admin_handlers.py`
-   **Responsibility:** Contains all Telegram handler functions specific to admin commands (e.g., `/addadmin`, `/removeadmin`, `/listusers`, `/broadcast`). Implements admin authentication checks.

### `handlers/user_handlers.py`
-   **Responsibility:** Contains all Telegram handler functions for regular user commands and interactions (e.g., `/start`, `/help`, `/setup`, `/connect_drive`, `/setfolder`, file uploads).

### `handlers/common_handlers.py`
-   **Responsibility:** Contains general-purpose Telegram handler functions, such as error handlers, unknown command handlers, and possibly inline query handlers.

### `services/google_drive_service.py`
-   **Responsibility:** Encapsulates all logic for interacting with the Google Drive API. Includes methods for:
    -   Initializing the Google Drive client.
    -   Searching for folders by name.
    -   Creating folders if they don't exist.
    -   Uploading files to a specified folder.
    -   Handling Google Drive API errors.

### `services/shortio_service.py`
-   **Responsibility:** Encapsulates all logic for interacting with the Short.io API. Includes methods for:
    -   Shortening URLs.
    -   Handling Short.io API errors.

### `utils/google_auth_flow.py`
-   **Responsibility:** Manages the OAuth 2.0 flow for Google Drive. Provides functions to:
    -   Generate authorization URLs.
    -   Exchange authorization codes for tokens.
    -   Refresh access tokens using refresh tokens.
    -   Store and retrieve credentials securely.

### `utils/decorators.py`
-   **Responsibility:** Contains custom decorators for common tasks, such as:
    -   `@admin_only`: Restricts access to admin commands.
    -   `@authenticated_user`: Ensures the user is connected to Google Drive.
    -   `@log_errors`: Catches and logs errors in handlers.

### `utils/logger.py`
-   **Responsibility:** Configures and provides a centralized logging mechanism for the entire application.

## 3. Key Data Models (Conceptual)

-   **User:** `user_id` (Telegram ID), `is_admin`, `google_drive_refresh_token`, `google_drive_folder_id`, `shortio_domain`, `shortio_api_key`.
-   **Admin:** `admin_id` (Telegram ID).

## 4. Workflow Overview

1.  **Bot Start:** `main.py` initializes the bot, database, and loads configurations.
2.  **User Interaction:** Users send commands or files.
3.  **Handler Dispatch:** `python-telegram-bot` dispatches updates to appropriate handlers.
4.  **Authentication/Authorization:** Decorators or explicit checks verify user/admin status and Google Drive connection.
5.  **Service Calls:** Handlers interact with `google_drive_service.py` and `shortio_service.py` to perform actions.
6.  **Database Operations:** `db_manager.py` is used to store and retrieve user/admin data and settings.
7.  **Response:** Bot sends appropriate messages back to the user.

## 5. Error Handling and Logging

-   Centralized error handling will be implemented using `common_handlers.py` to catch unhandled exceptions.
-   Specific error handling will be done within `services` modules (e.g., `google_drive_service.py`, `shortio_service.py`) to gracefully manage API failures.
-   `utils/logger.py` will ensure all significant events, errors, and warnings are logged to a file or console for debugging and monitoring.

This architecture aims to provide a clear separation of concerns, making the codebase easier to develop, test, and maintain.
