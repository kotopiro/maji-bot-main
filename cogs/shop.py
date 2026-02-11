import discord
from discord.ext import commands
from db import get_user,update_user

SHOP={
    "vip":500,
    "color":300
}

class Shop(commands.Cog):
    def __init__(self,bot):
        self.bot=bot

    @discord.app_commands.command(name="shop")
    async def shop(self,i):
        txt="\n".join([f"{k}:{v}" for k,v in SHOP.items()])
        await i.response.send_message(txt)

    @discord.app_commands.command(name="buy")
    async def buy(self,i,item:str):
        if item not in SHOP:
            await i.response.send_message("ない")
            return

        xp,lv,c=get_user(i.guild.id,i.user.id)
        cost=SHOP[item]

        if c<cost:
            await i.response.send_message("コイン不足")
            return

        update_user(i.guild.id,i.user.id,coins=c-cost)
        await i.response.send_message(f"{item}購入")

async def setup(bot):
    await bot.add_cog(Shop(bot))
