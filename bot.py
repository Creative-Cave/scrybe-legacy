from enum import auto
from dotenv import load_dotenv
from discord.ext import tasks
import discord
import os


if __name__ == "__main__":
    bot = discord.Bot()

    load_dotenv()

    for fn in os.listdir("./cogs"):
        if fn.endswith(".py"):
            bot.load_extension(f"cogs.{fn[:-3]}")

    bot.run(os.environ["bot_token"])
