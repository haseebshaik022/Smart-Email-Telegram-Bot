from groq import AsyncGroq
from dotenv import load_dotenv
import os

load_dotenv()

client = AsyncGroq(
    api_key=os.getenv("GROQ_API_KEY")
)


async def classify_email(sender, subject, date):

    prompt = f"""
You are an email classifier.

Classify this email as exactly one of:

IMPORTANT
NOT_IMPORTANT

IMPORTANT examples:
- Job opportunities
- Interview invitations
- Recruiter emails
- Security alerts
- Account alerts
- Payment alerts
- Important work emails
- Important personal emails

NOT_IMPORTANT examples:
- Advertisements
- Promotions
- Newsletters
- Marketing emails
- Sales offers
- Spam

Email:

From: {sender}
Subject: {subject}
Date: {date}

Return ONLY:
IMPORTANT

or:

NOT_IMPORTANT
"""

    response = await client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0,
        max_completion_tokens=200
    )

    result = response.choices[0].message.content

    print(f"Raw AI result: {result}")

    if not result:
        return "NOT_IMPORTANT"

    result = result.strip().upper()

    if result == "IMPORTANT":
        return "IMPORTANT"

    return "NOT_IMPORTANT"