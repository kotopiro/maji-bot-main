import discord
from discord.ext import commands
from discord import app_commands

class Info(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # =========================
    # /serverinfo
    # =========================
    @app_commands.command(
        name="serverinfo",
        description="サーバー情報を表示します"
    )
    async def serverinfo(self, i: discord.Interaction):
        g = i.guild

        e = discord.Embed(
            title=f"🏠 {g.name}",
            color=0x3498db
        )

        e.add_field(name="人数", value=g.member_count)
        e.add_field(name="サーバーID", value=g.id)
        e.add_field(name="作成日", value=g.created_at.strftime("%Y-%m-%d"))

        if g.icon:
            e.set_thumbnail(url=g.icon.url)

        await i.response.send_message(embed=e)

    # =========================
    # /userinfo
    # =========================
    @app_commands.command(
        name="userinfo",
        description="ユーザー情報を表示します"
    )
    @app_commands.describe(
        member="調べるユーザー（省略で自分）"
    )
    async def userinfo(
        self,
        i: discord.Interaction,
        member: discord.Member | None = None
    ):
        member = member or i.user

        e = discord.Embed(
            title=f"👤 {member}",
            color=member.color if member.color.value else 0x2ecc71
        )

        e.add_field(name="ID", value=member.id)
        e.add_field(name="参加日", value=member.joined_at.strftime("%Y-%m-%d"))
        e.add_field(name="作成日", value=member.created_at.strftime("%Y-%m-%d"))
        e.add_field(name="ロール数", value=len(member.roles)-1)

        e.set_thumbnail(url=member.display_avatar.url)

        await i.response.send_message(embed=e)

    # =========================
    # /embed
    # =========================
    @app_commands.command(
        name="embed",
        description="埋め込みメッセージを送信します"
    )
    @app_commands.describe(
        title="タイトル",
        description="本文",
        color="色コード（例: FF0000）"
    )
    async def embed(
        self,
        i: discord.Interaction,
        title: str,
        description: str,
        color: str = "00aaff"
    ):
        try:
            c = int(color, 16)
        except:
            c = 0x00AAFF

        e = discord.Embed(
            title=title,
            description=description,
            color=c
        )

        await i.response.send_message(embed=e)

    # =========================
    # /help
    # =========================
    @app_commands.command(
        name="help",
        description="コマンド一覧を表示します"
    )
    async def help(self, i: discord.Interaction):

        cmds = self.bot.tree.get_commands()

        lines = [
            f"/{c.name} — {c.description or '説明なし'}"
            for c in cmds
        ]

        e = discord.Embed(
            title="📘 コマンド一覧",
            description="\n".join(sorted(lines)),
            color=0xf1c40f
        )

        await i.response.send_message(embed=e, ephemeral=True)


async def setup(bot):
    await bot.add_cog(Info(bot))
