import discord
from discord.ext import commands
import random

class Verify(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # =====================
    # ✅ VERIFY（計算認証）
    # =====================
    @discord.app_commands.command(
        name="verify",
        description="計算認証ボタンを設置します"
    )
    async def verify(self, i: discord.Interaction, role: discord.Role):
        view = VerifyView(role)
        await i.response.send_message("認証ボタンを押してください", view=view)

# =====================
# 認証UI
# =====================
class VerifyView(discord.ui.View):
    def __init__(self, role):
        super().__init__(timeout=None)  # 無期限
        self.role = role

    @discord.ui.button(label="答える", style=discord.ButtonStyle.green)
    async def btn(self, i: discord.Interaction, b: discord.ui.Button):
        a = random.randint(1, 99)
        b_num = random.randint(1, 99)
        await i.response.send_modal(VerifyModal(self.role, a, b_num))


class VerifyModal(discord.ui.Modal):
    def __init__(self, role, a, b):
        super().__init__(title="計算認証")
        self.role = role
        self.answer = a + b
        self.ans = discord.ui.TextInput(label=f"問題: {a} + {b} = ?")
        self.add_item(self.ans)

    async def on_submit(self, i: discord.Interaction):
        if self.ans.value.isdigit() and int(self.ans.value) == self.answer:
            await i.user.add_roles(self.role)
            await i.response.send_message("✅ 認証成功", ephemeral=True)
        else:
            await i.response.send_message("❌ 不正解", ephemeral=True)


async def setup(bot):
    await bot.add_cog(Verify(bot))
