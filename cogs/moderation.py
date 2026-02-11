import discord
from discord.ext import commands
from discord import app_commands
from datetime import timedelta

class Mod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # =====================
    # BAN コマンド
    # =====================
    @app_commands.command(
        name="ban",
        description="指定したメンバーをBANします"
    )
    @app_commands.checks.has_permissions(ban_members=True)
    async def ban(
        self,
        i: discord.Interaction,
        member: discord.Member,
        reason: str = "なし"
    ):
        await member.ban(reason=reason)
        await i.response.send_message(f"🔨 BANしました: {member}")

    # =====================
    # KICK コマンド
    # =====================
    @app_commands.command(
        name="kick",
        description="指定したメンバーをキックします"
    )
    @app_commands.checks.has_permissions(kick_members=True)
    async def kick(
        self,
        i: discord.Interaction,
        member: discord.Member
    ):
        await member.kick()
        await i.response.send_message(f"👢 キックしました: {member}")

    # =====================
    # TIMEOUT コマンド
    # =====================
    @app_commands.command(
        name="timeout",
        description="指定したメンバーを一定時間タイムアウトします"
    )
    @app_commands.checks.has_permissions(moderate_members=True)
    async def timeout(
        self,
        i: discord.Interaction,
        member: discord.Member,
        minutes: int
    ):
        until = discord.utils.utcnow() + timedelta(minutes=minutes)
        await member.timeout(until)
        await i.response.send_message(f"⏱️ {member} を {minutes}分タイムアウトしました")

async def setup(bot):
    await bot.add_cog(Mod(bot))
