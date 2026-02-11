import discord
from discord.ext import commands
from discord import app_commands
from db import get_user, update_user

# =========================
# ショップ商品リスト
# =========================
SHOP = {
    "vip": 500,
    "color": 300
}

class Shop(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    # =========================
    # /shop コマンド
    # ショップ一覧を表示
    # =========================
    @app_commands.command(
        name="shop",
        description="ショップの商品一覧と価格を表示します"
    )
    async def shop(self, i: discord.Interaction):

        txt = "\n".join([
            f"🛒 {name} — {price}コイン"
            for name, price in SHOP.items()
        ])

        await i.response.send_message(
            f"**ショップ一覧**\n{txt}"
        )

    # =========================
    # /buy コマンド
    # 商品を購入
    # =========================
    @app_commands.command(
        name="buy",
        description="ショップの商品を購入します"
    )
    @app_commands.describe(
        item="購入する商品の名前"
    )
    async def buy(self, i: discord.Interaction, item: str):

        # 商品チェック
        if item not in SHOP:
            await i.response.send_message(
                "❌ その商品は存在しません",
                ephemeral=True
            )
            return

        xp, lv, coins = get_user(i.guild.id, i.user.id)
        cost = SHOP[item]

        # コインチェック
        if coins < cost:
            await i.response.send_message(
                f"💰 コイン不足（必要: {cost}）",
                ephemeral=True
            )
            return

        # コイン更新
        update_user(i.guild.id, i.user.id, coins=coins - cost)

        await i.response.send_message(
            f"✅ **{item}** を購入しました！"
        )


async def setup(bot):
    await bot.add_cog(Shop(bot))
