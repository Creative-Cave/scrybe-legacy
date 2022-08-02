from discord.ext import commands
from resources.colour import colours
import resources.get_configs
import discord

guilds = resources.get_configs.get_attr("guilds")


class Misc(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.slash_command(
        guild_ids=guilds,
        description="Creates an embed and sends it"
    )
    async def embed(self, ctx, title: discord.Option(str), description: discord.Option(str), colour: discord.Option(default="default", choices=[discord.OptionChoice(name=c, value=c) for c in colours])):
        await ctx.respond("...", delete_after=0)
        c = colours[colour]
        await ctx.send(embed=discord.Embed(
            title=title,
            description=description,
            colour=discord.Color.from_rgb(c[0], c[1], c[2])
        ))

    @commands.slash_command(
        guild_ids=guilds,
        description="Sends the bot's latency in ms"
    )
    async def ping(self, ctx):
        await ctx.send_response(embed=discord.Embed(title="Pong!", description=f"Latency: `{round(self.bot.latency*1000, 2)}ms`"), ephemeral=True)
    
    @commands.slash_command(
        guild_ids=guilds,
        description="Submit an issue report or a suggestion"
    )
    async def report(self, ctx):
        await ctx.send_response(embed=discord.Embed(
            title="Found a problem or have a suggestion?",
            description="Submit it [here](https://github.com/Writers-Cave/scrybe-2/issues/new)",
            colour=discord.Colour.blurple()
        ), ephemeral=True)


def setup(bot):
    bot.add_cog(Misc(bot))
