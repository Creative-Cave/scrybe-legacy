from discord.ext import commands
from resources import get_configs, reloader
import discord
import os

cogs = os.listdir("./cogs")
guilds = get_configs.get_attr("guilds")


class Management(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command()
    async def refresh(self, ctx, cog_name: discord.Option(choices=[fn[:-3] for fn in cogs if fn != "management.py"])):
        reloader.reload_cog(self.bot, cog_name)
        await ctx.send_response(f"Reloaded {cog_name}", ephemeral=True)


def setup(bot):
    bot.add_cog(Management(bot))
