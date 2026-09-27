# 📧 Smart Email Telegram Bot

An AI-powered email monitoring bot that analyzes Gmail emails using their metadata and sends Telegram notifications only for emails classified as important.

The project is built with Python, Gmail API, Groq LLM, Telegram Bot API, and APScheduler.

---

## 🚀 Features

- 📩 Fetches the latest emails from Gmail
- 🔍 Extracts email metadata:
  - Sender
  - Subject
  - Date
- 🤖 Uses an LLM to classify emails as:
  - `IMPORTANT`
  - `NOT_IMPORTANT`
- 📲 Sends Telegram notifications for important emails
- 🚫 Ignores promotions, newsletters, marketing emails, and other unimportant messages
- 🔁 Automatically checks Gmail every 12 hours
- 🧠 Tracks processed Gmail message IDs to prevent duplicate processing
- 🔐 Uses environment variables and OAuth credentials for secure configuration
- ⚡ Uses asynchronous Python with `asyncio`
- ⏰ Uses APScheduler for periodic background execution

---

## 🏗️ Architecture

```text
                    Gmail API
                        │
                        ▼
              Fetch Email Metadata
              ┌──────────────────┐
              │ From             │
              │ Subject          │
              │ Date             │
              └──────────────────┘
                        │
                        ▼
                 AI Classifier
                        │
             ┌──────────┴──────────┐
             ▼                     ▼
        IMPORTANT             NOT_IMPORTANT
             │                     │
             ▼                     ▼
      Telegram Alert              Ignore
             │
             ▼
          User
