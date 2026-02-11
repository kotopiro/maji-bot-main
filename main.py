import discord
from discord.ext import commands
from flask import Flask
from threading import Thread
import os

# =========================
# keep alive web server
# =========================
app = Flask(__name__)

@app.route("/")
def home():
    return "bot alive"

def run_web():
    port = int(os.getenv("PORT", 8000))
    app.run(host="0.0.0.0", port=port)

def keep_alive():
    t = Thread(target=run_web, daemon=True)
    t.start()

# =========================
# discord bot
# =========================
intents = discord.Intents.all()

class Bot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix="!",
            intents=intents
        )

    async def setup_hook(self):

        # cogs 読み込み
        if os.path.isdir("./cogs"):
            for file in os.listdir("./cogs"):
                if file.endswith(".py"):
                    try:
                        await self.load_extension(f"cogs.{file[:-3]}")
                        print(f"Loaded cog: {file}")
                    except Exception as e:
                        print(f"Cog load error {file}: {e}")

        # スラッシュコマンド同期
        await self.tree.sync()
        print("Slash commands synced")

bot = Bot()

@bot.event
async def on_ready():
    print(f"起動: {bot.user}")
    await bot.change_presence(
        activity=discord.Game("/help | school-rekisi.kesug.com")
    )

# =========================
# start
# =========================
keep_alive()

TOKEN = os.getenv("TOKEN")
if not TOKEN:
    raise RuntimeError("TOKEN が設定されていません")

bot.run(TOKEN)
