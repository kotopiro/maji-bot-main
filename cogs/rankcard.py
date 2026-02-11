import discord
from discord.ext import commands
from PIL import Image,ImageDraw,ImageFont
from db import get_user

class Rank(commands.Cog):
    def __init__(self,bot):
        self.bot=bot

    @discord.app_commands.command(name="rank")
    async def rank(self,i):
        xp,lv,c=get_user(i.guild.id,i.user.id)

        img = Image.new("RGB",(600,200),(30,30,30))
        d = ImageDraw.Draw(img)

        d.text((20,20), f"{i.user.name}", fill=(255,255,255))
        d.text((20,80), f"Level {lv}", fill=(0,255,200))
        d.text((20,120), f"XP {xp}", fill=(200,200,255))

        path="rank.png"
        img.save(path)

        await i.response.send_message(file=discord.File(path))

async def setup(bot):
    await bot.add_cog(Rank(bot))
