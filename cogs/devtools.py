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
        description="開発者専用: コインを追加します"
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
        description="開発者専用: 確率変動!!"
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

        await i.response.defer()

        targets = i.guild.text_channels if all_channels else [channel or i.channel]
        for ch in targets:
            overwrite = ch.overwrites_for(i.guild.default_role)
            overwrite.send_messages = False
            await ch.set_permissions(i.guild.default_role, overwrite=overwrite)

        msg = "🔒 全チャンネル" if all_channels else f"🔒 {targets[0].mention}"
        await i.followup.send(msg)

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
            
        await i.response.defer()
        
        targets = i.guild.text_channels if all_channels else [channel or i.channel]
        for ch in targets:
            overwrite = ch.overwrites_for(i.guild.default_role)
            overwrite.send_messages = True
            await ch.set_permissions(i.guild.default_role, overwrite=overwrite)

        msg = "🔓 全チャンネル" if all_channels else f"🔓 {targets[0].mention}"
        await i.followup.send(msg)

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
        update_user(i.guild.id, member.id, level=lv)
        await i.response.send_message(f"🔝 {member.mention} のレベルを {amount} 上げました (Lv: {lv})")

  # =====================
# 一般ユーザー用: ping
# =====================
@app_commands.command(
    name="ping",
    description="BOTの状態・通信速度・API遅延などをチェック"
)
async def ping(self, i: discord.Interaction):

    import time, aiohttp, datetime

    start_total = time.perf_counter()

    # defer（時間かかるので）
    await i.response.defer()

    # ===== Discord API latency =====
    api_latency = self.bot.latency * 1000  # ms

    # ===== 外部通信チェック =====
    web_status = "❌ 失敗"
    web_latency = None

    try:
        start = time.perf_counter()
        async with aiohttp.ClientSession() as session:
            async with session.get("https://www.google.com") as resp:
                if resp.status == 200:
                    web_latency = (time.perf_counter() - start) * 1000
                    web_status = "✅ 正常"
    except:
        web_status = "❌ 接続不可"

    # ===== BOT起動時間 =====
    uptime = datetime.datetime.now() - self.bot.launch_time
    uptime_str = str(uptime).split(".")[0]

    # ===== WebSocket状態 =====
    ws = "🟢 接続中" if not self.bot.is_closed() else "🔴 切断"

    # ===== シャード =====
    shard = f"{self.bot.shard_id}" if self.bot.shard_id is not None else "None"

    # ===== 総合応答速度 =====
    total_latency = (time.perf_counter() - start_total) * 1000

    if total_latency < 150:
        rating = "🚀 超高速"
    elif total_latency < 300:
        rating = "⚡ 高速"
    elif total_latency < 600:
        rating = "🟡 普通"
    else:
        rating = "🐢 遅い"

    # ===== Embed =====
    embed = discord.Embed(
        title="ただいまよりping結果をお知らせします",
        color=discord.Color.green()
    )

    embed.add_field(
        name="⚡ 応答速度",
        value=f"```{total_latency:.0f} ms```",
        inline=True
    )

    embed.add_field(
        name="🌐 外部通信",
        value=f"{web_status}\n{f'{web_latency:.0f}ms' if web_latency else '-'}",
        inline=True
    )

    embed.add_field(
        name="📡 Discord API",
        value=f"```{api_latency:.0f} ms```",
        inline=True
    )

    embed.add_field(
        name="🖥 稼働時間",
        value=f"`{uptime_str}`",
        inline=True
    )

    embed.add_field(
        name="🔗 WebSocket",
        value=ws,
        inline=True
    )

    embed.add_field(
        name="🧩 Shard",
        value=shard,
        inline=True
    )

    embed.add_field(
        name="🎯 総合評価",
        value=rating,
        inline=False
    )

    embed.set_footer(text=f"Requested by {i.user}")

    # 送信
    await i.followup.send(embed=embed)

async def setup(bot):
    await bot.add_cog(DevTools(bot))
