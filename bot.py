import os
import re
import json
import discord
import aiohttp
import requests
from dotenv import load_dotenv
from discord.ext import commands
from discord import app_commands

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
VT_API_KEY = os.getenv("VT_API_KEY")

VT_HEADERS = {"x-apikey": VT_API_KEY}
URL_REGEX = r"https?://[^\s]+"
CONFIG_PATH = "config.json"

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)
tree = bot.tree

# Load and save config
def load_config():
    if not os.path.exists(CONFIG_PATH):
        return {"language": "en"}
    with open(CONFIG_PATH, "r") as f:
        return json.load(f)

def save_config(config):
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=2)

# Load language files
def load_language(lang_code):
    try:
        with open(f"languages/{lang_code}.json", "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

config = load_config()
LANG = load_language(config.get("language", "en"))

@bot.event
async def on_ready():
    try:
        await tree.sync()
        print("Commands synced.")
    except Exception as e:
        print(f"Gagal sync command: {e}")
    print(f"Bot {bot.user} sudah aktif.")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    urls = re.findall(URL_REGEX, message.content)
    if urls:
        await message.channel.send(LANG.get("scanning_url", "Scanning URL..."))
        for url in urls:
            await scan_url(message.channel, url)

    if message.attachments:
        await message.channel.send(LANG.get("scanning_file", "Scanning file..."))
        for attachment in message.attachments:
            await scan_file(message.channel, attachment)

    await bot.process_commands(message)

@tree.command(name="languages", description="Menampilkan daftar bahasa yang tersedia")
async def show_languages(interaction: discord.Interaction):
    try:
        files = os.listdir("languages")
        langs = [f.replace(".json", "") for f in files if f.endswith(".json")]
        if not langs:
            await interaction.response.send_message("Tidak ada bahasa ditemukan.")
            return
        daftar = "\n".join(f"- `{l}`" for l in langs)
        await interaction.response.send_message(f"**Bahasa yang tersedia:**\n{daftar}")
    except Exception as e:
        await interaction.response.send_message(f"Gagal membaca folder bahasa: {str(e)}")

@tree.command(name="setlanguage", description="Ganti bahasa bot")
@app_commands.describe(language="Kode bahasa, seperti en, id, ru")
@app_commands.autocomplete(language=lambda i, c: [app_commands.Choice(name=lang.replace(".json", ""), value=lang.replace(".json", ""))
                                                  for lang in os.listdir("languages") if lang.endswith(".json")])
async def set_language(interaction: discord.Interaction, language: str):
    global LANG
    LANG = load_language(language)
    if not LANG:
        await interaction.response.send_message("Gagal memuat bahasa tersebut.")
        return

    config["language"] = language
    save_config(config)
    await interaction.response.send_message(f"Bahasa berhasil diubah ke: `{language}`.")

async def scan_url(channel, url):
    data = {"url": url}
    try:
        res = requests.post("https://www.virustotal.com/api/v3/urls", headers=VT_HEADERS, data=data)
        if res.status_code != 200:
            raise Exception(res.text)
        url_id = res.json()["data"]["id"]
        report = requests.get(f"https://www.virustotal.com/api/v3/analyses/{url_id}", headers=VT_HEADERS).json()
        stats = report["data"]["attributes"]["stats"]

        await channel.send(
            f"**{LANG.get('scan_result_url', 'Scan result for URL')}:**\n"
            f"URL: {url}\nMalicious: {stats['malicious']}\nSuspicious: {stats['suspicious']}"
        )
    except Exception as e:
        await channel.send(f"{LANG.get('failed_url', 'Failed to scan URL')}: {url}\n{e}")

async def scan_file(channel, attachment):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(attachment.url) as resp:
                file_data = await resp.read()

        files = {"file": (attachment.filename, file_data)}
        res = requests.post("https://www.virustotal.com/api/v3/files", headers=VT_HEADERS, files=files)
        if res.status_code != 200:
            raise Exception(res.text)

        analysis_id = res.json()["data"]["id"]
        report = requests.get(f"https://www.virustotal.com/api/v3/analyses/{analysis_id}", headers=VT_HEADERS).json()
        stats = report["data"]["attributes"]["stats"]

        await channel.send(
            f"**{LANG.get('scan_result_file', 'Scan result for file')}:**\n"
            f"Nama: {attachment.filename}\nMalicious: {stats['malicious']}\nSuspicious: {stats['suspicious']}"
        )
    except Exception as e:
        await channel.send(f"{LANG.get('failed_file', 'Failed to scan file')}: {attachment.filename}\n{e}")

bot.run(DISCORD_TOKEN)
