import discord
from discord.ext import commands

class Util(commands.Cog):
    def __init__(self,bot):
        self.bot=bot

    @discord.app_commands.command(name="serverinfo")
    async def serverinfo(self,i):
        g=i.guild
        await i.response.send_message(
            f"{g.name}\n人数:{g.member_count}"
        )

async def setup(bot):
    await bot.add_cog(Util(bot))
