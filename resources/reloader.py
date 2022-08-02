import os

def reload_cog(bot, cog_name):
    if f"{cog_name}.py" in os.listdir("./cogs"):
        bot.reload_extension(f"cogs.{cog_name}")
        return 1
    else:
        return None
        