# Smart Email Telegram Bot

First version of a Gmail metadata reader.

## Flow

Gmail API -> Python -> email metadata -> later classification -> Telegram notification

## Setup

Put the downloaded Google OAuth file in this folder and name it:

`credentials.json`

Create a virtual environment:

```bash
python -m venv .venv
```

Activate it on Windows:

```bash
.venv\\Scripts\\activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run:

```bash
python main.py
```

The first run opens Google's OAuth authorization page and creates `token.json`.

`credentials.json` and `token.json` are ignored by Git and should never be committed.
