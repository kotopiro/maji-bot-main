import discord
from discord.ext import commands
from discord import app_commands

# =========================
# ロール付与ボタンView
# =========================
class RoleView(discord.ui.View):
    def __init__(self, role: discord.Role):
        super().__init__(timeout=None)  # 永続ボタン
        self.role = role

    # ボタンが押された時の処理
    @discord.ui.button(label="ロール取得", style=discord.ButtonStyle.green)
    async def get(self, i: discord.Interaction, button: discord.ui.Button):

        # 権限チェック
        if not i.guild.me.guild_permissions.manage_roles:
            await i.response.send_message("Botにロール管理権限がありません", ephemeral=True)
            return

        # ロール付与
        await i.user.add_roles(self.role)

        await i.response.send_message(
            f"✅ {self.role.name} を付与しました",
            ephemeral=True
        )


# =========================
# Cog本体
# =========================
class Roles(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="buttonrole",
        description="ボタンでロールを取得できるメッセージを作成します"
    )
    @app_commands.describe(
        role="ボタンで付与するロール"
    )
    async def buttonrole(self, i: discord.Interaction, role: discord.Role):

        await i.response.send_message(
            f"👇 押すと **{role.name}** が付与されます",
            view=RoleView(role)
        )


async def setup(bot):
    await bot.add_cog(Roles(bot))
