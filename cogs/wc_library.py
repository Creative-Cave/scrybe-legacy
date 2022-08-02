from discord.ext import commands
from discord.commands import SlashCommandGroup
from resources.get_library import *
from datetime import datetime
import resources.get_configs
import discord
import json

guilds = resources.get_configs.get_attr("guilds")


with open("resources/emoji.json", "r") as fp:
    e = json.load(fp)
    empty_star = e["empty_star"]
    half_star = e["half_star"]
    full_star = e["full_star"]
    verified = e["verified"]
    loading = e["loading"]


def human_rating(book) -> str:
    """Convert numerical rating to a string of corresponding star emojis"""

    if isinstance(book, dict):
        if book["reviews"] == {}:
            rating = 2.5
        else:
            rating = 0
            for review in book["reviews"].keys():
                rating += book["reviews"][review]["rating"]
            rating /= len(book["reviews"])
            rating = round(rating * 2) / 2

        stars = ""
        count = 0
        while rating > 0:
            if rating > 0.5:
                stars += full_star
                rating -= 1
                count += 1
            elif rating == 0.5:
                stars += half_star
                rating -= 0.5
                count += 1

        stars += empty_star*(5-count)

        return stars


with open("resources/config.json") as fp:
    config = json.load(fp)

library = get_library()["library"]


class Library(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    library_group = SlashCommandGroup(
        "library", "Commands for the server library")

    edit_library = library_group.create_subgroup(
        "edit", "Manage the library")

    @library_group.command(
        guild_ids=guilds,
        description="Shows the books in the server library"
    )
    async def list(self, ctx):
        r = await ctx.send_response(f"{loading} Thinking...")
        library = get_library()["library"]
        e = discord.Embed(title="Writer's Cave Library")
        e.set_footer(
            text="To view more information, including the links to read each book, run /library info")

        for id in library:
            book = library[id]
            e.add_field(name=f"{book['title']}",
                        value=f"by {book['author']}\n{human_rating(book)} *{len(book['reviews'])} reviews*")

        await r.edit_original_message(content=None, embed=e)

    @library_group.command(
        guild_ids=guilds,
        description="Shows more information on a specified book"
    )
    async def info(self, ctx, book: discord.Option(choices=[discord.OptionChoice(name=library[book]["title"], value=book) for book in library])):
        r = await ctx.send_response(f"{loading} Thinking...")
        library = get_library()["library"]
        book = library[str(book)]

        verified_link = False
        for link in config["verified_links"]:
            if book["link"].startswith(link):
                verified_link = True


        class LinkView(discord.ui.View):
            def __init__(self):
                super().__init__(timeout=None)
                urlbutton = discord.ui.Button(
                    label=f"Read this book", style=discord.ButtonStyle.gray, url=book["link"], emoji="👀")
                self.add_item(urlbutton)


        e = discord.Embed(
            title=book["title"], description=config["unverified_link_message"] if not verified_link else config["verified_link_message"].format(verified))

        e.add_field(name="Author", value=book["author"])

        e.add_field(
            name="Rating", value=f'{human_rating(book)}\n(*{len(book["reviews"])} reviews)*')

        await r.edit_original_message(content=None, embed=e, view=LinkView())

    @library_group.command(
        guild_ids=guilds,
        description="Submit a review on a specified book"
    )
    async def review(self, ctx, book: discord.Option(choices=[discord.OptionChoice(name=library[book]["title"], value=book) for book in library]), rating: discord.Option(
            choices=[str(n) for n in [0, 0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5]]), content: discord.Option(default="")):
        r = await ctx.send_response(f"{loading} Thinking...")
        add_review(book, {
            "rating": rating,
            "content": content,
            "author": ctx.author.id,
            "timestamp": datetime.timestamp(datetime.now())
        })
        await r.edit_original_message(content="Review submitted!")

    @edit_library.command(
        guild_ids=guilds,
        description="Add a book to the server library"
    )
    @discord.default_permissions(administrator=True)
    async def add(self, ctx, title: discord.Option(str), author: discord.Option(str), link: discord.Option(str)):
        r = await ctx.send_response(f"{loading} Thinking...")

        library = get_library()["library"]
        for book in library:
            if title.lower() == library[book]["title"].lower():
                return await ctx.send_response(":x: A book with that title already exists; consider changing it slightly.")
            elif link == library[book]["link"]:
                return await ctx.send_response(":x: A book with that link already exists.")
            else:
                continue

        add_book(title, author, link)
        await r.edit_original_message(content=f"Added {title} by {author} to the library.")

    @edit_library.command(
        guild_ids=guilds,
        description="Removes a book from the server library"
    )
    @discord.default_permissions(administrator=True)
    async def remove(self, ctx, book: discord.Option(choices=[discord.OptionChoice(name=library[book]["title"], value=book) for book in library])):
        r = await ctx.send_response(f"{loading} Thinking...")
        book_details = get_library()["library"][str(book)]
        remove_book(book)
        await r.edit_original_message(content=f"Deleted {book_details['title']} by {book_details['author']} (ID {book})")


def setup(bot):
    bot.add_cog(Library(bot))
