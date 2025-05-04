# Discord URL and File Detector Bot

This is a Discord bot that detects and displays URLs and file attachments sent in a Discord server. The bot does not perform any scanning or processing on the URLs or files. It simply detects and shows them in the channel.

## Features

- **URL Detection**: The bot detects URLs in messages and displays them in the channel.
- **File Detection**: The bot detects file attachments in messages and displays them in the channel.
- **Language Support**: The bot can be configured to support multiple languages.

## Requirements

Before running the bot, ensure you have the following dependencies:

- **Python 3.8+**
- **Discord.py** (`discord.py` library)
- **Aiohttp** (for handling file downloads)
- **Requests** (for making HTTP requests)
- **Python-dotenv** (for loading environment variables)

### Python Libraries

You can install the required libraries using `pip`:

```bash
pip install discord.py aiohttp requests python-dotenv
```

## Setup
1. Clone this Repository
Clone the bot repository to your local machine:
```bash
git clone https://github.com/AlFarrizi/HeroX.git
cd HeroX
```

2. Create a .env File
Create a .env file in the root directory and add the following environment variables:
```bash
DISCORD_TOKEN=<your_discord_bot_token>
VT_API_KEY=<your_virustotal_api_key>
```
Replace <your_discord_bot_token> with your actual Discord bot token, and <your_virustotal_api_key> with your VirusTotal API key (if applicable for future use or reference).

3. Language Files
The bot supports multiple languages. Language files are stored in the languages/ directory. Each language file should be named as <language_code>.json (e.g., en.json, id.json).

4. Run the Bot
To start the bot, run the following command:
```bash
python bot.py
```
The bot will connect to Discord and be ready to start detecting URLs and files in messages.

## Commands
- **/languages** (Shows the available languages supported by the bot).
- **/setlanguage** (Allows you to change the language of the bot. Use the language code (e.g., en, id) as an argument).

Example:
```bash
/setlanguage en
```
Changes the bot's language to English.

## How It Works
» When a user sends a message with URLs, the bot detects and displays those URLs in the channel.

» If a message contains file attachments, the bot detects and displays the file name and URL to the file in the channel.

» You can use slash commands to change the language of the bot or see which languages are available.

## Contributing
If you'd like to contribute to this bot, feel free to fork the repository and submit pull requests.

## License
This project is licensed under the MIT License - see the LICENSE file for details.
```bash
This `README.md` file includes an overview of the bot, setup instructions, command usage, and other helpful information for setting up and running the bot. Let me know if you need further changes or additions!
```
