import discord
from discord.ext import commands
from discord import app_commands

class Util(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # =========================
    # /serverinfo コマンド
    # サーバー情報を表示
    # =========================
    @app_commands.command(
        name="serverinfo",
        description="このサーバーの基本情報を表示します"
    )
    async def serverinfo(self, i: discord.Interaction):

        g = i.guild

        embed = discord.Embed(
            title=f"📊 {g.name}",
            color=discord.Color.blue()
        )

        embed.add_field(name="👥 メンバー数", value=str(g.member_count))
        embed.add_field(name="🆔 サーバーID", value=str(g.id))
        embed.add_field(name="👑 オーナー", value=str(g.owner))

        if g.icon:
            embed.set_thumbnail(url=g.icon.url)

        await i.response.send_message(embed=embed)


async def setup(bot):
    await bot.add_cog(Util(bot))
