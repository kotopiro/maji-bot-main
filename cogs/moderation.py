import discord
from discord.ext import commands
from discord import app_commands
from datetime import timedelta
import random

class Mod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # =====================
    # BAN
    # =====================
    @app_commands.command(
        name="ban",
        description="指定したメンバーをBANします"
    )
    @app_commands.checks.has_permissions(ban_members=True)
    async def ban(self, i: discord.Interaction, member: discord.Member, reason: str = "なし"):
        await member.ban(reason=reason)
        await i.response.send_message(f"🔨 BANしました: {member}")

    # =====================
    # KICK
    # =====================
    @app_commands.command(
        name="kick",
        description="指定したメンバーをキックします"
    )
    @app_commands.checks.has_permissions(kick_members=True)
    async def kick(self, i: discord.Interaction, member: discord.Member):
        await member.kick()
        await i.response.send_message(f"👢 キックしました: {member}")

    # =====================
    # TIMEOUT
    # =====================
    @app_commands.command(
        name="timeout",
        description="指定メンバーをタイムアウトします"
    )
    @app_commands.checks.has_permissions(moderate_members=True)
    async def timeout(self, i: discord.Interaction, member: discord.Member, minutes: int):
        until = discord.utils.utcnow() + timedelta(minutes=minutes)
        await member.timeout(until)
        await i.response.send_message(f"⏱️ {minutes}分タイムアウトしました")

    # =====================
    # 🔒 LOCK
    # =====================
    @app_commands.command(
        name="lock",
        description="このチャンネルをロックします"
    )
    @app_commands.checks.has_permissions(manage_channels=True)
    async def lock(self, i: discord.Interaction):
        ow = i.channel.overwrites_for(i.guild.default_role)
        ow.send_messages = False
        await i.channel.set_permissions(i.guild.default_role, overwrite=ow)
        await i.response.send_message("🔒 ロックしました")

    # =====================
    # 🔓 UNLOCK
    # =====================
    @app_commands.command(
        name="unlock",
        description="このチャンネルをアンロックします"
    )
    @app_commands.checks.has_permissions(manage_channels=True)
    async def unlock(self, i: discord.Interaction):
        ow = i.channel.overwrites_for(i.guild.default_role)
        ow.send_messages = True
        await i.channel.set_permissions(i.guild.default_role, overwrite=ow)
        await i.response.send_message("🔓 アンロックしました")

    # =====================
    # 🧹 PURGE
    # =====================
    @app_commands.command(
        name="purge",
        description="メッセージを指定数削除します"
    )
    @app_commands.checks.has_permissions(manage_messages=True)
    async def purge(self, i: discord.Interaction, amount: int):
        await i.response.send_message("削除中...", ephemeral=True)
        deleted = await i.channel.purge(limit=amount)
        await i.followup.send(f"🧹 {len(deleted)}件削除しました")

  # =====================
# 認証UI
# =====================

class VerifyModal(discord.ui.Modal, title="計算認証"):
    ans = discord.ui.TextInput(label="答え")

    def __init__(self, role, answer):
        super().__init__()
        self.role = role
        self.answer = answer

    async def on_submit(self, i: discord.Interaction):
        if self.ans.value.isdigit() and int(self.ans.value) == self.answer:
            await i.user.add_roles(self.role)
            await i.response.send_message("✅ 認証成功", ephemeral=True)
        else:
            await i.response.send_message("❌ 不正解", ephemeral=True)


class VerifyView(discord.ui.View):
    def __init__(self, role, answer):
        super().__init__(timeout=180)
        self.role = role
        self.answer = answer

    @discord.ui.button(label="答える", style=discord.ButtonStyle.green)
    async def btn(self, i: discord.Interaction, b: discord.ui.Button):
        await i.response.send_modal(
            VerifyModal(self.role, self.answer)
        )


# =====================
# Mod Cog
# =====================

class Mod(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ---------- VERIFY ----------
    @app_commands.command(
        name="verify",
        description="計算認証ボタンを設置します"
    )
    @app_commands.checks.has_permissions(manage_roles=True)
    async def verify(self, i: discord.Interaction, role: discord.Role):

        await i.response.defer()  # ← interaction timeout防止

        a = random.randint(1, 9)
        b = random.randint(1, 9)

        view = VerifyView(role, a + b)

        await i.followup.send(
            f"認証してください: {a} + {b} = ?",
            view=view
        )


async def setup(bot):
    await bot.add_cog(Mod(bot))
