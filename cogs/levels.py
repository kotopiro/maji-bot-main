import discord, random, time
from discord.ext import commands
from discord import app_commands
from db import get_user, update_user

xp_cd = {}  # XPクールダウン

class Levels(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # ===== XP付与 =====

    @commands.Cog.listener()
    async def on_message(self, m: discord.Message):

        if m.author.bot or not m.guild:
            return

        uid = m.author.id

        # 30秒クールダウン
        if uid in xp_cd and time.time() - xp_cd[uid] < 30:
            return

        xp, lv, coins = get_user(m.guild.id, uid)

        gain = random.randint(5, 10)
        xp += gain

        need = lv * 100

        if xp >= need:
            lv += 1
            xp -= need
            await m.channel.send(
                f"🎉 {m.author.mention} が Lv{lv} にアップ！"
            )

        update_user(m.guild.id, uid, xp=xp, level=lv)
        xp_cd[uid] = time.time()

    # ===== レベル確認 =====

    @app_commands.command(
        name="level",
        description="現在のレベルとXPを表示します"
    )
    @app_commands.describe(
        user="確認するユーザー（省略可）"
    )
    async def level_cmd(
        self,
        interaction: discord.Interaction,
        user: discord.User = None
    ):
        target = user or interaction.user

        xp, lv, coins = get_user(interaction.guild.id, target.id)

        need = lv * 100

        await interaction.response.send_message(
            f"📊 {target.display_name}\n"
            f"Lv: {lv}\n"
            f"XP: {xp}/{need}"
        )

async def setup(bot):
    await bot.add_cog(Levels(bot))
