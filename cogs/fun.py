import discord, random
from discord.ext import commands
from discord import app_commands

class Fun(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ===== コイン投げ =====

    @app_commands.command(
        name="coinflip",
        description="コインを投げます（表 / 裏）"
    )
    async def coin(self, interaction: discord.Interaction):
        await interaction.response.send_message(
            random.choice(["🪙 表", "🪙 裏"])
        )

    # ===== サイコロ =====

    @app_commands.command(
        name="dice",
        description="サイコロを振ります"
    )
    @app_commands.describe(
        sides="面の数（デフォルト6）"
    )
    async def dice(self, interaction: discord.Interaction, sides: int = 6):

        if sides < 2 or sides > 1000:
            await interaction.response.send_message(
                "❌ 面の数は 2〜1000 にしてください",
                ephemeral=True
            )
            return

        await interaction.response.send_message(
            f"🎲 {random.randint(1, sides)}"
        )

async def setup(bot):
    await bot.add_cog(Fun(bot))
