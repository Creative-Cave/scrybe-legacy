from discord.ext import commands
from discord.commands import SlashCommandGroup
from PyMultiDictionary import MultiDictionary
from PyDictionary import PyDictionary
import resources.get_configs
import discord

guilds = resources.get_configs.get_attr("guilds")
words = MultiDictionary()
dwords = PyDictionary()


class Language(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        

    dictionary_group = SlashCommandGroup(
        "dictionary", "Commands for vocabulary")

    @dictionary_group.command(
        guild_ids=guilds,
        description="Shows definitions for a specified English word"
    )
    async def define(self, ctx, word: discord.Option(str)):
        word = word.lower()
        response = await ctx.send_response(f":mag_right: Searching for *\"{word}\"*...")

        definition = dwords.meaning(word)
        e = discord.Embed(
            title=f':notebook_with_decorative_cover: Definitions for "{word}"'
        )
        if not definition:
            e.description = ":question: No definitions found."
        else:
            for tick, k in enumerate(definition):
                for d in (definition[k])[:7]: #  only show up to eight definitions due to message content length cap
                    e.add_field(
                        name=k, value=f"{tick+1}: {d}", inline=False)

        await response.edit_original_message(embed=e, content="")

    @dictionary_group.command(
        guild_ids=guilds,
        description="Shows synonyms for a specified English word"
    )
    async def synonyms(self, ctx, word: discord.Option(str)):
        word = word.lower()
        response = await ctx.send_response(f":mag_right: Searching for *\"{word}\"*...")

        syns = words.synonym(word=word, lang="en")
        e = discord.Embed(
            title=f':notebook_with_decorative_cover: Synonyms for "{word}"',
            description=', '.join(syns)
        )

        await response.edit_original_message(embed=e, content="")


def setup(bot):
    bot.add_cog(Language(bot))
