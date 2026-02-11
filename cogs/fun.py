import discord,random
from discord.ext import commands

class Fun(commands.Cog):
    def __init__(self,bot):
        self.bot=bot

    @discord.app_commands.command(name="coinflip")
    async def coin(self,i):
        await i.response.send_message(random.choice(["表","裏"]))

    @discord.app_commands.command(name="dice")
    async def dice(self,i,sides:int=6):
        await i.response.send_message(str(random.randint(1,sides)))

async def setup(bot):
    await bot.add_cog(Fun(bot))
