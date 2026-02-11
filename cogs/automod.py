import discord, re
from discord.ext import commands
from discord import app_commands
from collections import defaultdict
from datetime import timedelta

spam = defaultdict(list)

class AutoMod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ===== 説明コマンド =====

    @app_commands.command(
        name="automod",
        description="このサーバーの自動モデレーション内容を表示します"
    )
    async def automod_info(self, interaction: discord.Interaction):

        embed = discord.Embed(
            title="🛡 AutoMod",
            description="現在の自動対策",
            color=0xff5555
        )

        embed.add_field(
            name="招待リンク",
            value="discord.gg を含むメッセージを削除",
            inline=False
        )

        embed.add_field(
            name="スパム",
            value="短時間に6発言で5分タイムアウト",
            inline=False
        )

        await interaction.response.send_message(embed=embed)

    # ===== メッセージ監視 =====

    @commands.Cog.listener()
    async def on_message(self, m: discord.Message):
        if m.author.bot:
            return

        # 招待リンク削除
        if re.search(r"discord\.gg", m.content):
            await m.delete()
            await m.channel.send("🚫 招待リンクは禁止です", delete_after=5)
            return

        # スパム検出（60秒以内）
        now = discord.utils.utcnow()
        spam[m.author.id] = [
            t for t in spam[m.author.id]
            if (now - t).total_seconds() < 60
        ]

        spam[m.author.id].append(now)

        if len(spam[m.author.id]) >= 6:
            await m.author.timeout(
                now + timedelta(minutes=5),
                reason="spam"
            )
            await m.channel.send(
                f"🔇 {m.author.mention} を5分タイムアウトしました"
            )

async def setup(bot):
    await bot.add_cog(AutoMod(bot))
