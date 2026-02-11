import discord
from discord.ext import commands
import os

intents = discord.Intents.all()

class Bot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix="!",
            intents=intents
        )

    async def setup_hook(self):
        for file in os.listdir("./cogs"):
            if file.endswith(".py"):
                await self.load_extension(f"cogs.{file[:-3]}")
        await self.tree.sync()

bot = Bot()

@bot.event
async def on_ready():
    print(f"最強Bot起動: {bot.user}")
    await bot.change_presence(
        activity=discord.Game("/help | school-rekisi.kesug.com")
    )

bot.run(os.getenv("TOKEN"))
