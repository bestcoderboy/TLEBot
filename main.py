# Importing necessary modules and packages
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

# ---------
# BOT SETUP
# ---------

# Bot Settings
bot_command_prefix = "!"
bot_name = "TLEBot"
bot_description = "A bot created by **@BestSpyBoy**, designed specifically for the Luxury Elevator's official Discord server! Type `>help` to get started."
bot_brand_color = 0xde8114
# Changes every update. This shouldn't be edited unless you're forking your own version.
bot_version_number = "v1.1.0"

# Wiki Settings
wiki_commands_enabled = True  # Set to True if you have a MediaWiki setup (includes Fandom)
wiki_url = "https://wiki.theluxuryelevator.com"  # Change to your wiki domain, for example: "https://doors-game.fandom.com"

# Credit Settings
# Change this if you want to, but it's nice if you keep credit :)
credit_name = "BestSpyBoy"
credit_profile = "https://cdn.discordapp.com/avatars/725417693699899534/1fecf89ce5fefa638d2f273ed1d986aa.webp"

# Gets your bot token from a .env file
load_dotenv()

# ---------
# END BOT SETUP
# ---------

# Setting up Discord bot with command prefix and intents
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix=bot_command_prefix, intents=intents)

# Removing default help command to replace it with a custom one
bot.remove_command('help')


# Function to create a help embed for commands
def help_embed():
    # Creating an embed object with title, color, and fields
    embed = discord.Embed(title=f"{bot_name} Help", color=bot_brand_color)
    embed.add_field(name=">floor `<page name>`", value="Returns details about the floor given.")
    embed.add_field(name=">search `<query>`", value="Returns search results for that query.")
    embed.add_field(name=">create `<page name>`", value="Generates a link to create a wiki page with the name given.")
    embed.add_field(name=">signup", value="Returns a link to sign up to the Wiki.")
    embed.add_field(name=">help", value="Shows this embed.")
    embed.set_footer(text=f"Created by {credit_name} • {bot_version_number}",
                     icon_url=credit_profile)
    return embed


# Function to create an empty help embed
def empty_help_embed(name, value):
    # Creating an embed object with title, color, and fields
    embed = discord.Embed(title=f"{bot_name} Help", color=bot_brand_color)
    embed.add_field(name=name, value=value)
    embed.set_footer(text=f"Created by {credit_name} • {bot_version_number}",
                     icon_url=credit_profile)
    return embed


# Function to create an info embed for the bot
def info_embed():
    # Creating an embed object with title, color, and description
    embed = discord.Embed(title=f"{bot_name}", color=bot_brand_color,
                          description=bot_description)
    embed.set_footer(text=f"Created by {credit_name} • {bot_version_number}",
                     icon_url=credit_profile)
    return embed


# Function to create an error embed with a given error message
def error_embed(error):
    # Creating an embed object with a red color and the provided error message
    embed = discord.Embed(color=0xFF0000, description=error)
    embed.set_footer(text=f"Created by {credit_name} • {bot_version_number}",
                     icon_url=credit_profile)
    return embed


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
    print("settings")
    if arg is None:
        print("no")
        await ctx.send(embed=error_embed(">settings needs an option to change and a value."))
    else:
        command = arg.split(" ", 2)
        print(command)
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


# Command to fetch details about a page in the Wiki
@bot.command(aliases=['floor'])
async def page(ctx, *, arg=None):
    if arg is None:
        await ctx.send(f"<{wiki_url}>")
    else:
        # Parsing arguments and creating a link to the Wiki based on user input
        arguments = re.findall(r'\(.*?\)', arg)
        attribute = re.findall(r'\[.*?]', arg)

        wiki_link = re.sub(r' \(.*?\)| \[.*?]', "", arg)
        wiki_link_parsed = wiki_link.title().replace(" ", "_")

        # Checking for special arguments and responding accordingly
        if "(embed)" in arguments:
            await ctx.send(f"{wiki_url}/wiki/" + urllib.parse.quote(wiki_link_parsed),)
        elif "(link)" in arguments:
            await ctx.send(f"<{wiki_url}/wiki/" + urllib.parse.quote(wiki_link_parsed), + ">")
        else:
            try:
                # Making a request to the Wiki API to retrieve floor details
                params = {
                    "action": "parse",
                    "page": urllib.parse.quote(wiki_link_parsed),
                    "prop": "wikitext",
                    "formatversion": 2,
                    "format": "json"
                }
                r = requests.get(f"{wiki_url}/w/api.php", params=params)
                r_body = r.json()
                if "error" in r.text:
                    await ctx.send(
                        embed=error_embed("I can't find that floor in the wiki. Do you want to `>create` it?"))
                else:
                    floor_attributes = convert_wikitext_to_dict(r_body.get("parse").get("wikitext"))
                    if floor_attributes is None:
                        await ctx.send(embed=error_embed(f"[That wiki page]({wiki_url}/wiki/{urllib.parse.quote(wiki_link_parsed)}) isn't a floor. Maybe there's no infobox?"))
                        return

                    # Responding with floor details or a specific attribute if provided
                    if not attribute:
                        embed = discord.Embed(title="Floor Details", color=bot_brand_color)
                        for key, value in floor_attributes.items():
                            if key == "image1":
                                embed.set_image(
                                    url=f"{wiki_url}/wiki/Special:Filepath/" + urllib.parse.quote(value))
                            elif key == "title1":
                                embed.add_field(name="Name",
                                                value=f"[{floor_attributes.get('title1')}]({wiki_url}/wiki/{urllib.parse.quote(wiki_link_parsed)})")
                            else:
                                embed.add_field(name=key.title().replace("_", " "),
                                                value=value)
                        embed.set_footer(text=f"Created by {credit_name} • {bot_version_number}",
                                         icon_url=credit_profile)
                        await ctx.send(embed=embed)
                    else:
                        attribute_parsed = re.sub('\[', "", attribute[0])
                        attribute_parsed = re.sub(']', "", attribute_parsed)
                        await ctx.send(
                            f" > The {attribute_parsed} of {floor_attributes.get('title1')} is **{floor_attributes.get(attribute_parsed)}**.")
            except requests.exceptions.Timeout:
                await ctx.send(embed=error_embed("The request to the server timed out :cry:"))


# Command to generate a link for creating a new Wiki page
@bot.command()
async def create(ctx, *, arg=None):
    if arg is None:
        await ctx.send(embed=error_embed("`>create` requires an argument."))
    else:
        wiki_link = re.sub(' \(.*?\)', "", arg)
        wiki_link_parsed = wiki_link.title().replace(" ", "_")
        await ctx.send(f"<{wiki_url}/w/index.php?title=" + wiki_link_parsed + "&veaction=edit>")


# Command to search the Wiki and display results
@bot.command()
async def search(ctx, *, arg=None):
    if arg is None:
        await ctx.send(embed=error_embed("`>search` requires an argument."))
    else:
        try:
            # Making a request to the Wiki API to perform a search
            params = {
                "action": "query",
                "list": "search",
                "srsearch": urllib.parse.quote(arg),
                "format": "json"
            }
            r = requests.get(f"{wiki_url}/w/api.php", params=params)
            r_body = r.json()
            search_array = r_body.get("query").get("search")

            # Responding with search results or an error message if no results are found
            if not search_array:
                await ctx.send(embed=error_embed("Couldn't find a result!"))
            else:
                embed_desc = ""
                for value in search_array:
                    embed_desc += f"""
• {value.get("title")}"""
                if len(search_array) == 10:
                    embed_desc += f"""
> Note: will only return up to ten results"""
                embed = discord.Embed(title="Search Results", color=bot_brand_color, description=embed_desc)
                embed.set_footer(text=f"Created by {credit_name} • {bot_version_number}",
                                 icon_url=credit_profile)
                await ctx.send(embed=embed)

        except:
            await ctx.send(embed=error_embed("Something went wrong processing your search."))


# Command to provide a link for users to sign up on the Wiki
@bot.command()
async def signup(ctx, *, arg=None):
    await ctx.send(f"<{wiki_url}/wiki/Special:CreateAccount>")


# Command to provide special links to the Wiki
@bot.command()
async def wiki(ctx, *, arg=None):
    if arg is None:
        await ctx.send(f"<{wiki_url}>")
    elif arg == "recent":
        await ctx.send(f"<{wiki_url}/wiki/Special:RecentChanges>")
    elif arg == "signup":
        await ctx.send(f"<{wiki_url}/wiki/Special:RecentChanges>")
    else:
        await ctx.send(embed=error_embed("That isn't a"))  # was an accident, but it's funny so i'm keeping it


# Command to provide a link to pages on the Wiki
@bot.command(aliases=['link'])
async def wikilink(ctx, *, arg=None):
    if arg is None:
        await ctx.send(embed=error_embed("`>wikilink` requires an argument."))
    else:
        wiki_link = re.sub(' \(.*?\)', "", arg)
        wiki_link_parsed = wiki_link.title().replace(" ", "_")
        await ctx.send(f"<{wiki_url}/wiki/{wiki_link_parsed}>")

# Command to link to the Floors List on the Luxury Elevator Wiki
@bot.command(aliases=['floorslist'])
async def floorlist(ctx, *, arg=None):
    await ctx.send(f"<{wiki_url}/wiki/Floors_List>")


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
