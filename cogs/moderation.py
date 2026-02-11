import discord
from discord.ext import commands
from discord import app_commands

class Mod(commands.Cog):
    def __init__(self,bot):
        self.bot=bot

    @app_commands.command(name="ban")
    @app_commands.checks.has_permissions(ban_members=True)
    async def ban(self,i:discord.Interaction,member:discord.Member,reason:str="なし"):
        await member.ban(reason=reason)
        await i.response.send_message(f"BAN: {member}")

    @app_commands.command(name="kick")
    @app_commands.checks.has_permissions(kick_members=True)
    async def kick(self,i,member:discord.Member):
        await member.kick()
        await i.response.send_message("kick完了")

    @app_commands.command(name="timeout")
    async def timeout(self,i,member:discord.Member,minutes:int):
        until = discord.utils.utcnow() + discord.timedelta(minutes=minutes)
        await member.timeout(until)
        await i.response.send_message("timeout完了")

async def setup(bot):
    await bot.add_cog(Mod(bot))
