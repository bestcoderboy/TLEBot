# Importing necessary modules and packages
import asyncio
import difflib                                         # Auto command matching on error
import discord                                         # Literally running the bot
import re                                              # Regular expressions for wiki search
import requests                                        # HTTP requests to the wiki API
from discord.ext import commands                       # For the Discord bot commands
import urllib.parse                                    # To sanitize user input for the API
from wiki_to_dict import convert_wikitext_to_dict      # Idk why this is in another file, it's neat i guess
import os                                              # For getting token from environment variables
from dotenv import load_dotenv                         # As above
import random as rand_lib                              # For the >random command
from commands.embeds import error_embed, help_embed, info_embed
import toml
from commands.wiki import WikiCommands

from os import path

basepath = path.dirname(__file__)
filepath = path.abspath(path.join(basepath, "config.toml"))
with open(filepath, "r") as f:
    data = toml.load(f)
    # bot_name = data['BotName']
    # bot_description = data['BotDescription']
    bot_prefix = data['BotPrefix']
    bot_brand_color = data['BotBrandColor']
    bot_version_number = data['BotVersionNumber']

    credit_name = data['credits']['CreditName']
    credit_profile = data['credits']['CreditProfile']

    wiki_commands_enabled = data['wiki']['WikiCommandsEnabled']


# Gets your bot token from a .env file
load_dotenv()

# ---------
# END BOT SETUP
# ---------

# Setting up Discord bot with command prefix and intents
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=bot_prefix, intents=intents)

# Removing default help command to replace it with a custom one
bot.remove_command('help')


async def add_cogs():
    if wiki_commands_enabled:
        print("enabled wiki")
        await bot.add_cog(WikiCommands(bot))


asyncio.run(add_cogs())


# Event handler for command errors
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        # Handling command not found errors by suggesting a similar command
        user_command = ctx.message.content.split()[0][1:]
        all_commands = [command.name for command in bot.commands]
        closest_match = difflib.get_close_matches(user_command, all_commands, n=1)
        if closest_match:
            await ctx.send(embed=error_embed(f"Did you mean `{bot.command_prefix}{closest_match[0]}`?"))
        else:
            await ctx.send(embed=error_embed("Command not found. Use '>help' to see available commands."))
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send(embed=error_embed("⚠️ This is an admin-only command - check you have the permissions to run it."))
    else:
        # Handling other unexpected errors by providing a detailed error message
        await ctx.send(embed=error_embed(f"""An unexpected error occurred when running that command. Ping **@{credit_name}** for help.
||```elixir
#{repr(error)}
```||"""))



# Command to display help information
@bot.command(aliases=['commands'])
async def help(ctx, *, arg=None):
    await ctx.send(embed=help_embed())


# Command to display bot information
@bot.command(aliases=['information'])
async def info(ctx):
    await ctx.send(embed=info_embed())


# Command to change the bot's settings. TODO: Expand settings to change from bot
@bot.command()
@commands.has_permissions(administrator=True)
async def settings(ctx, *, arg=None):
    if arg is None:
        await ctx.send(embed=error_embed(">settings needs an option to change and a value."))
    else:
        command = arg.split(" ", 2)
        if command[0] == "activity":
            # could do streaming here but w h y
            if command[1] == "playing" and len(command) == 3:
                await bot.change_presence(activity=discord.Game(name=command[2]))
            elif command[1] == "listening":
                await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=command[2]))
            elif command[1] == "watching":
                await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=command[2]))
            else:
                await ctx.send(embed=error_embed("Invalid syntax for the activity setting."))


# Preparing list of fun facts
original_fun_facts = [
    "If you submit <#561140450962964482> there's a chance it'll get added to the game!",
    """The Luxury Elevator was once featured on **ItsFunneh's** channel. 
[The video](https://www.youtube.com/watch?v=AycjO0rwR4E) of her playing the game got 16 million views!""",
    "The lobby was only added almost two years after the game was first uploaded to Roblox! You would spawn in the elevator instead.",
    "Several old floors had to be deleted after Roblox introduced their audio update in 2022... wait that's not a fun fact :(",
    "This bot was created in only two hours, and all the code running it is [available](https://github.com/bestcoderboy/TLEbot) for anyone to use on their own server!",
    "In 2024, The Luxury Elevator will receive a super update, with new floors, a UI overhaul, bug fixes and more.",
    "### ################ ## # ###### #### ####### ####### ######### - ##### # #### ## #######. ### #####...",
    "The game has 48 badges - four of them are future badges and three badges can no longer be obtained.",
    "More fun facts are coming soon, promise!"
]
fun_facts = original_fun_facts

current_fun_fact = ""
previous_facts = []


# Command to give random facts - why not?
@bot.command(aliases=['fact', 'randomfact', 'funfact', 'facts'])
async def random(ctx, *, arg=None):
    global fun_facts, current_fun_fact, previous_facts  # Needed to stop error
    if len(fun_facts) == 0:  # Resets the fun facts
        fun_facts = original_fun_facts
        rand_lib.shuffle(fun_facts)
        fun_fact = fun_facts.pop()
        previous_facts.append(fun_fact)
        # print(previous_facts)
        # print(fun_fact)
    else:
        previous_facts.append(current_fun_fact)
        fun_fact = fun_facts.pop()
        if fun_fact in previous_facts:
            fun_facts.insert(0, fun_fact)
            fun_fact = fun_facts.pop()
        if len(previous_facts) > 3:
            previous_facts.pop(1)
        # print(previous_facts)
        # print(fun_fact)

    embed = discord.Embed(title="Fun fact", color=bot_brand_color, description=f"""{current_fun_fact}""")
    embed.set_footer(text=f"Created by {credit_name} • {bot_version_number}",
                     icon_url=credit_profile)
    await ctx.send(embed=embed)


@bot.command(aliases=['credit'])
async def credits(ctx, *, arg=None):
    embed = discord.Embed(title="TLE Credits", color=bot_brand_color, description=f"""Game Creator: **Milo Murphy**
Lead Developer / Game Owner: **Ferb_Fletcher**
(retired) Developer: **Phineas_Flynn**
    """)
    embed.set_footer(text=f"Created by {credit_name} • {bot_version_number}",
                     icon_url=credit_profile)
    await ctx.send(embed=embed)


# Running the Discord bot with the provided token
bot.run(os.getenv('DISCORD_TOKEN'))
