import discord, asyncio
from discord.ext import commands
from discord import app_commands

class Remind(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="remind",
        description="指定した分後にリマインドメッセージを送ります"
    )
    @app_commands.describe(
        minutes="何分後に通知するか",
        msg="通知する内容"
    )
    async def remind(self, i: discord.Interaction, minutes: int, msg: str):

        # 上限チェック（安全）
        if minutes <= 0 or minutes > 1440:
            await i.response.send_message("1〜1440分で指定してください", ephemeral=True)
            return

        await i.response.send_message(f"⏰ {minutes}分後に通知します")

        await asyncio.sleep(minutes * 60)

        await i.followup.send(
            f"{i.user.mention} ⏰ リマインド:\n{msg}"
        )

async def setup(bot):
    await bot.add_cog(Remind(bot))
