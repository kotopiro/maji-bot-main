import discord
from discord.ext import commands
from discord import app_commands

cmds = {}

class CC(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ===== 追加 =====

    @app_commands.command(
        name="addcmd",
        description="カスタムコマンドを追加します（管理者のみ）"
    )
    @app_commands.describe(
        name="呼び出しワード",
        text="送信される内容"
    )
    async def add(self, interaction: discord.Interaction, name: str, text: str):

        if not interaction.user.guild_permissions.manage_guild:
            await interaction.response.send_message(
                "❌ 管理者のみ追加できます",
                ephemeral=True
            )
            return

        cmds[name] = text
        await interaction.response.send_message(
            f"✅ コマンド `{name}` を追加しました"
        )

    # ===== 一覧 =====

    @app_commands.command(
        name="listcmd",
        description="登録されているカスタムコマンド一覧を表示"
    )
    async def list_cmd(self, interaction: discord.Interaction):

        if not cmds:
            await interaction.response.send_message("登録なし")
            return

        text = "\n".join(cmds.keys())
        await interaction.response.send_message(f"📜 コマンド一覧\n{text}")

    # ===== 削除 =====

    @app_commands.command(
        name="delcmd",
        description="カスタムコマンドを削除（管理者のみ）"
    )
    async def delete_cmd(self, interaction: discord.Interaction, name: str):

        if not interaction.user.guild_permissions.manage_guild:
            await interaction.response.send_message(
                "❌ 管理者のみ削除できます",
                ephemeral=True
            )
            return

        if name in cmds:
            del cmds[name]
            await interaction.response.send_message("🗑 削除しました")
        else:
            await interaction.response.send_message("見つかりません")

    # ===== 実行 =====

    @commands.Cog.listener()
    async def on_message(self, m: discord.Message):
        if m.author.bot:
            return

        if m.content in cmds:
            await m.channel.send(cmds[m.content])

async def setup(bot):
    await bot.add_cog(CC(bot))
