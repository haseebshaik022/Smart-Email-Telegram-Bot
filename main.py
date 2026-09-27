import asyncio
import json
import os

from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

from apscheduler.schedulers.asyncio import AsyncIOScheduler

from classifier import classify_email
from telegram import send_telegram


SCOPES = ["https://www.googleapis.com/auth/gmail.readonly"]

PROCESSED_FILE = "processed_emails.json"


def get_gmail_service():
    creds = None

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file(
            "token.json",
            SCOPES
        )

    if not creds or not creds.valid:

        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())

        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json",
                SCOPES
            )

            creds = flow.run_local_server(port=0)

        with open("token.json", "w") as token:
            token.write(creds.to_json())

    return build(
        "gmail",
        "v1",
        credentials=creds
    )


def load_processed_emails():

    if not os.path.exists(PROCESSED_FILE):
        return set()

    try:
        with open(PROCESSED_FILE, "r") as file:
            return set(json.load(file))

    except json.JSONDecodeError:
        return set()


def save_processed_emails(processed):

    with open(PROCESSED_FILE, "w") as file:
        json.dump(list(processed), file)


async def check_emails():

    service = get_gmail_service()

    processed = load_processed_emails()

    result = service.users().messages().list(
        userId="me",
        maxResults=10
    ).execute()

    messages = result.get("messages", [])

    print(f"Found {len(messages)} emails")

    for message in messages:

        message_id = message["id"]

        if message_id in processed:
            continue

        msg = service.users().messages().get(
            userId="me",
            id=message_id,
            format="metadata",
            metadataHeaders=[
                "From",
                "Subject",
                "Date"
            ]
        ).execute()

        headers = msg["payload"].get("headers", [])

        sender = ""
        subject = ""
        date = ""

        for header in headers:

            if header["name"] == "From":
                sender = header["value"]

            elif header["name"] == "Subject":
                subject = header["value"]

            elif header["name"] == "Date":
                date = header["value"]

        print("\n-----------------------------")
        print(f"From: {sender}")
        print(f"Subject: {subject}")
        print(f"Date: {date}")

        classification = await classify_email(
            sender,
            subject,
            date
        )

        print(f"AI: {classification}")

        if classification == "IMPORTANT":

            telegram_message = f"""
🔔 IMPORTANT EMAIL

👤 From:
{sender}

📌 Subject:
{subject}

📅 Date:
{date}

⚡ This email was classified as important.
"""

            send_telegram(telegram_message)

            print("📨 Telegram notification sent!")

        else:

            print("⏭️ Not important. Ignoring.")

        processed.add(message_id)

        save_processed_emails(processed)


async def run_bot():

    await check_emails()

    scheduler = AsyncIOScheduler()

    scheduler.add_job(
        check_emails,
        "interval",
        seconds=10
    )

    scheduler.start()

    print("🤖 Email bot is running...")
    print("⏰ Checking Gmail every 1 hour...")

    while True:
        await asyncio.sleep(10)


if __name__ == "__main__":
    asyncio.run(run_bot())