# Telegram Bot for GTI Project

## Description

This is a Telegram Bot for the GTI Project. It is written in Python. It is a simple bot that receives images of bank transactions, processes them and saves them in a database.

## Installation

### Requirements

- Python 3.6 or higher

### Steps

1. Clone the repository
2. Install the requirements with `pip install -r requirements.txt`
3. Create a `.env` file with the following variables:
    - `TELEGRAM_TOKEN`: The token of the Telegram bot
4. Run the bot using docker with `docker-compose up -d`