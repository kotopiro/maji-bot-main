import discord, random, time
from discord.ext import commands
from discord import app_commands
from db import get_user, update_user

daily_cd = {}  # クールダウン用

class Eco(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ===== デイリー =====

    @app_commands.command(
        name="daily",
        description="1日1回コインを受け取れます"
    )
    async def daily(self, interaction: discord.Interaction):

        uid = interaction.user.id

        # 24時間クールダウン
        if uid in daily_cd and time.time() - daily_cd[uid] < 86400:
            await interaction.response.send_message(
                "⏳ まだ受け取れません（24時間ごと）",
                ephemeral=True
            )
            return

        xp, lv, coins = get_user(interaction.guild.id, uid)

        coins += 200
        update_user(interaction.guild.id, uid, coins=coins)
        daily_cd[uid] = time.time()

        await interaction.response.send_message(
            f"💰 デイリー報酬 +200コイン\n現在: {coins}"
        )

    # ===== ギャンブル =====

@app_commands.command(
    name="gamble",
    description="コインを賭けて勝負します"
)
@app_commands.describe(
    amount="賭けるコイン数"
)
async def gamble(self, interaction: discord.Interaction, amount: int):

    if amount <= 0:
        await interaction.response.send_message("❌ 正の数を指定")
        return

    xp, lv, coins = get_user(interaction.guild.id, interaction.user.id)

    if amount > coins:
        await interaction.response.send_message("❌ コイン不足")
        return

    # ⭐ここ重要（確変対応）
    chance = getattr(self.bot, "gamble_chance", 0.5)

    if random.random() < chance:
        coins += amount
        msg = f"🎉 勝ち！ +{amount}"
    else:
        coins -= amount
        msg = f"💸 負け… -{amount}"

    update_user(interaction.guild.id, interaction.user.id, coins=coins)

    await interaction.response.send_message(
        f"{msg}\n現在残高: {coins}"
    )

async def setup(bot):
    await bot.add_cog(Eco(bot))
