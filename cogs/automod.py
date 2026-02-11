import discord,re
from discord.ext import commands
from collections import defaultdict

spam=defaultdict(list)

class AutoMod(commands.Cog):
    def __init__(self,bot):
        self.bot=bot

    @commands.Cog.listener()
    async def on_message(self,m):
        if m.author.bot: return

        if re.search(r"discord\.gg",m.content):
            await m.delete()
            return

        spam[m.author.id].append(m.created_at)
        if len(spam[m.author.id])>=6:
            await m.author.timeout(
                discord.utils.utcnow()+discord.timedelta(minutes=5),
                reason="spam"
            )

async def setup(bot):
    await bot.add_cog(AutoMod(bot))
