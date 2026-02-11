import discord
from discord.ext import commands
from discord import app_commands
from PIL import Image, ImageDraw, ImageFont
from db import get_user

class Rank(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(
        name="rank",
        description="あなたのレベル・XP・コインを画像で表示します"
    )
    async def rank(self, i: discord.Interaction):
        xp, lv, c = get_user(i.guild.id, i.user.id)

        # 画像作成
        img = Image.new("RGB", (600, 200), (30, 30, 30))
        d = ImageDraw.Draw(img)

        # フォント（無い場合はデフォルト）
        try:
            font_big = ImageFont.truetype("arial.ttf", 36)
            font_mid = ImageFont.truetype("arial.ttf", 28)
        except:
            font_big = None
            font_mid = None

        # テキスト描画
        d.text((20, 20), i.user.name, fill=(255, 255, 255), font=font_big)
        d.text((20, 90), f"Level : {lv}", fill=(0, 255, 200), font=font_mid)
        d.text((20, 130), f"XP : {xp}", fill=(200, 200, 255), font=font_mid)
        d.text((350, 130), f"Coins : {c}", fill=(255, 220, 120), font=font_mid)

        # ユーザー別ファイル名
        path = f"rank_{i.user.id}.png"
        img.save(path)

        await i.response.send_message(file=discord.File(path))

async def setup(bot):
    await bot.add_cog(Rank(bot))
