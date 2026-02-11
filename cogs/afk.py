import discord
from discord.ext import commands
from discord import app_commands

afk = {}

class AFK(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="afk",
        description="AFK（離席）状態を設定します"
    )
    @app_commands.describe(
        msg="離席理由（省略可）"
    )
    async def setafk(self, interaction: discord.Interaction, msg: str = "離席中"):
        afk[interaction.user.id] = msg
        await interaction.response.send_message("✅ AFKを設定しました")

    @commands.Cog.listener()
    async def on_message(self, m: discord.Message):

        # Botは無視
        if m.author.bot:
            return

        # 発言したらAFK解除
        if m.author.id in afk:
            del afk[m.author.id]
            await m.channel.send("🔔 AFK解除しました")

        # メンションチェック
        for u in m.mentions:
            if u.id in afk:
                await m.channel.send(f"💤 {u.name} はAFK中: {afk[u.id]}")

async def setup(bot):
    await bot.add_cog(AFK(bot))
