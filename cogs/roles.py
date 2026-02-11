import discord
from discord.ext import commands

class RoleView(discord.ui.View):
    def __init__(self,role):
        super().__init__(timeout=None)
        self.role=role

    @discord.ui.button(label="ロール取得")
    async def get(self,i,b):
        await i.user.add_roles(self.role)
        await i.response.send_message("付与",ephemeral=True)

class Roles(commands.Cog):
    def __init__(self,bot):
        self.bot=bot

    @discord.app_commands.command(name="buttonrole")
    async def buttonrole(self,i,role:discord.Role):
        await i.response.send_message(
            "押して取得",
            view=RoleView(role)
        )

async def setup(bot):
    await bot.add_cog(Roles(bot))
