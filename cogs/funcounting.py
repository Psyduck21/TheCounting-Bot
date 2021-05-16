import discord
from discord.ext import commands
import json


class Funcounting(commands.Cog):
    def __init__(self, bot):
        self.bot = bot



    # Initializing command for game
    @commands.command()
    @commands.has_permissions(manage_messages = True)
    async def start(self, ctx):
        await ctx.guild.create_text_channel("fun-counting")
        fun_channel = discord.utils.get(ctx.guild.channels, name="fun-counting")
        await ctx.send(f"Game has started check out {fun_channel.mention}")
        emb = discord.Embed(
            description="*Rules of the game*\n1. No Member :octagonal_sign: should send 2 numbers in a row.\n2. Member should send consecutive numbers.\n*Disobeying any of the above Rule the game will be restarted*",
            colour=discord.Colour.blue())
        await fun_channel.send(embed=emb)
        await fun_channel.send("1")

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        #making a channel for the game
        fun_channel = discord.utils.get(message.guild.channels, name="fun-counting")
        try:
            if message.channel == fun_channel and message.content not in ["$start", f"{message.author.mention}has disobeyed the rules\nRestarting the game"]: # Some measures such as if author is bot don't do this 
                def check(msg):
                    return msg.channel == fun_channel and msg.content not in ["$start",
                                                                            f"{message.author.mention}has disobeyed the rules\nRestarting the game"]

                msg = await self.bot.wait_for("message", check=check)
                # Loadind a json file 
                with open("./json/fun.json") as json_file: 
                    data = json.load(json_file)
                # entring data to json file
                    fun_entry = {'user_id': message.author.id,
                                'content': message.content}

                    data.append(fun_entry)

                with open("./json/fun.json", 'w') as f:
                    json.dump(data, f, indent=4)

                i = data[-1]
                n = i['content'] # Getting number from json
                member_id = i['user_id'] # Getting user_id from json
                next_number = int(n) + 1 # Converting number which we get from json into int as json save it as a str and adding 1 to it
                next_number = str(next_number) # Converting number back to string so that we can compare it with next number to be entered
                if msg.content == next_number and msg.author.id != member_id: # (msg.content == next_number) checking number should be equal to next number and (msg.author.id != member_id) checking user should not send two numbers in row
                    print("passed")

                else: # If any of rules disobeyed the what to do ?
                    # As i don't know how many message to delete so i just delete and recreated the channel and restat the game by sending 1 in it
                    await fun_channel.delete() 
                    await message.guild.create_text_channel("fun-counting")
                    fun_channel = discord.utils.get(message.guild.channels, name="fun-counting")
                    await fun_channel.send(f"{msg.author.mention} has disobeyed the rules\nRestarting the game")
                    emb = discord.Embed(
                        description="*Rules of the game*\n1. No Member :octagonal_sign: should send 2 numbers in a row.\n2. Member should send consecutive numbers.\n*Disobeying any of the above Rule the game will be restarted*",
                        colour=discord.Colour.blue())
                    await fun_channel.send(embed=emb)
                    await fun_channel.send("1")
        except ValueError:
            pass

    # Command to stop the game manually
    @commands.command()
    @commands.has_permissions(manage_messages = True)
    async def stop(self, ctx):
        fun_channel = discord.utils.get(ctx.guild.channels, name="fun-counting")
        await fun_channel.delete()
        await ctx.send(f"Stopped!")


def setup(bot):
    bot.add_cog(Funcounting(bot))
    print("Fun counting Added")
