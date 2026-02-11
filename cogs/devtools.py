import discord
from discord.ext import commands
from discord import app_commands
from db import get_user, update_user
from datetime import timedelta
import random

# BOT開発者ID（複数可）
DEV_IDS = [1272012685520928773]  # ← 自分のDiscordIDに変更

class DevTools(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # ギャンブル勝率（デフォルト50%）
        if not hasattr(bot, "gamble_chance"):
            bot.gamble_chance = 0.5

    def is_dev(self, user_id):
        return user_id in DEV_IDS

    # =====================
    # 開発者専用: コイン追加
    # =====================
    @app_commands.command(
        name="addcoins",
        description="開発者専用: 指定ユーザーにコインを追加"
    )
    async def addcoins(
        self,
        i: discord.Interaction,
        member: discord.Member,
        amount: int
    ):
        if not self.is_dev(i.user.id):
            await i.response.send_message("❌ 開発者専用コマンドです", ephemeral=True)
            return

        xp, lv, coins = get_user(i.guild.id, member.id)
        coins += amount
        update_user(i.guild.id, member.id, coins=coins)
        await i.response.send_message(f"✅ {member.mention} に {amount} コイン追加 (合計: {coins})")

    # =====================
    # 開発者専用: ギャンブル勝率設定
    # =====================
    @app_commands.command(
        name="setchance",
        description="開発者専用: ギャンブル勝率を変更"
    )
    async def setchance(
        self,
        i: discord.Interaction,
        chance: float
    ):
        if not self.is_dev(i.user.id):
            await i.response.send_message("❌ 開発者専用コマンドです", ephemeral=True)
            return

        if not 0 <= chance <= 1:
            await i.response.send_message("❌ 0～1 の範囲で指定してください", ephemeral=True)
            return

        self.bot.gamble_chance = chance
        await i.response.send_message(f"🎲 ギャンブルの勝率を {chance*100:.1f}% に設定しました")

    # =====================
    # 開発者専用: チャンネルロック
    # =====================
    @app_commands.command(
        name="lock",
        description="開発者専用: チャンネル単体または全チャンネルをロック"
    )
    async def lock(
        self,
        i: discord.Interaction,
        channel: discord.TextChannel = None,
        all_channels: bool = False
    ):
        if not self.is_dev(i.user.id):
            await i.response.send_message("❌ 開発者専用コマンドです", ephemeral=True)
            return

        targets = i.guild.text_channels if all_channels else [channel or i.channel]
        for ch in targets:
            overwrite = ch.overwrites_for(i.guild.default_role)
            overwrite.send_messages = False
            await ch.set_permissions(i.guild.default_role, overwrite=overwrite)

        msg = "🔒 全チャンネル" if all_channels else f"🔒 {targets[0].mention}"
        await i.response.send_message(msg)

    @app_commands.command(
        name="unlock",
        description="開発者専用: チャンネル単体または全チャンネルをアンロック"
    )
    async def unlock(
        self,
        i: discord.Interaction,
        channel: discord.TextChannel = None,
        all_channels: bool = False
    ):
        if not self.is_dev(i.user.id):
            await i.response.send_message("❌ 開発者専用コマンドです", ephemeral=True)
            return

        targets = i.guild.text_channels if all_channels else [channel or i.channel]
        for ch in targets:
            overwrite = ch.overwrites_for(i.guild.default_role)
            overwrite.send_messages = True
            await ch.set_permissions(i.guild.default_role, overwrite=overwrite)

        msg = "🔓 全チャンネル" if all_channels else f"🔓 {targets[0].mention}"
        await i.response.send_message(msg)

    # =====================
    # 開発者専用: レベルアップ
    # =====================
    @app_commands.command(
        name="lankup",
        description="開発者専用: ユーザーのレベルを直接上げる"
    )
    async def lankup(
        self,
        i: discord.Interaction,
        member: discord.Member,
        amount: int
    ):
        if not self.is_dev(i.user.id):
            await i.response.send_message("❌ 開発者専用コマンドです", ephemeral=True)
            return

        xp, lv, coins = get_user(i.guild.id, member.id)
        lv += amount
        update_user(i.guild.id, member.id, lv=lv)
        await i.response.send_message(f"🔝 {member.mention} のレベルを {amount} 上げました (Lv: {lv})")

    # =====================
    # 一般ユーザー用: ping
    # =====================
    @app_commands.command(
        name="ping",
        description="BOTのレスポンスとインターネット疎通確認"
    )
    async def ping(self, i: discord.Interaction):
        import time, aiohttp
        start = time.perf_counter()
        async with aiohttp.ClientSession() as session:
            try:
                async with session.get("https://www.google.com") as resp:
                    if resp.status == 200:
                        latency = (time.perf_counter() - start) * 1000
                        await i.response.send_message(f"🏓 Pong! 応答時間: {latency:.0f}ms")
                        return
            except:
                pass
        await i.response.send_message("⚠️ 外部サーバーに接続できません")

async def setup(bot):
    await bot.add_cog(DevTools(bot))
