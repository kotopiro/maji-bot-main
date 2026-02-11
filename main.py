import discord
from discord.ext import commands
from flask import Flask
from threading import Thread
import os

# ---------- keep alive ----------
app = Flask(__name__)

@app.route("/")
def home():
    return "bot alive"

def run_web():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

def keep_alive():
    t = Thread(target=run_web)
    t.start()

# ---------- discord ----------
intents = discord.Intents.all()

class Bot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!", intents=intents)

    async def setup_hook(self):
        for file in os.listdir("./cogs"):
            if file.endswith(".py"):
                await self.load_extension(f"cogs.{file[:-3]}")
        await self.tree.sync()

bot = Bot()

@bot.event
async def on_ready():
    print(f"起動: {bot.user}")
    await bot.change_presence(
        activity=discord.Game("/help | school-rekisi.kesug.com")
    )

# ← ここで起動
keep_alive()

bot.run(os.getenv("TOKEN"))
