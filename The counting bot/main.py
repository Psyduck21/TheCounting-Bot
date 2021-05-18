from os import name
import discord
from discord.colour import Color
from discord.ext import commands

bot = commands.Bot(command_prefix=".", intents=discord.Intents.all())
bot.remove_command("help")

token = open("token.txt", "r").read()


@bot.event
async def on_ready():
    print("Bot is online")

@bot.command()
async def help(ctx):
    embed = discord.Embed(title = "The Counting Bot", color = ctx.author.color)
    embed.add_field(name="How to start counting game?", value="To start the game you have to use `.start`. This will create a new channel with name `fun-counting`.\n\nNow the game has started \nENJOY THE GAME!\n\n*Only admins can start the game!*")
    embed.add_field(name="How to Stop the game?", value="To stop the game use `.stop` command\n\n*Do not use the stop command in fun counting channel!*")
    embed.set_footer(text=f" |    Requested by {ctx.author.name}", icon_url=ctx.author.avatar_url)
    await ctx.send(embed=embed)

@bot.event #normal error handling
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send("Invalid command")
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send("You do not have required permissions")
    else:
        # raise error
        ...

extensions = [
    "cogs.funcounting"
]
if __name__ == "__main__":
    for extension in extensions:
        bot.load_extension(extension)



bot.run(token)
