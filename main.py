# Importing necessary modules and packages
import difflib
import discord
import re
import requests
from discord.ext import commands
import urllib.parse
from wiki_to_dict import convert_wikitext_to_dict
import os
from dotenv import load_dotenv

load_dotenv()

# Setting up Discord bot with command prefix and intents
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='>', intents=intents)

# Removing default help command to replace it with a custom one
bot.remove_command('help')


# Function to create a help embed for commands
def help_embed():
    # Creating an embed object with title, color, and fields
    embed = discord.Embed(title="TLEWikiBot Help", color=0xde8114)
    embed.add_field(name=">floor `<page name>`", value="Returns details about the floor given.")
    embed.add_field(name=">search `<query>`", value="Returns search results for that query.")
    embed.add_field(name=">create `<page name>`", value="Generates a link to create a wiki page with the name given.")
    embed.add_field(name=">signup", value="Returns a link to sign up to the Wiki.")
    embed.add_field(name=">help", value="Shows this embed.")
    embed.set_footer(text="Created by BestSpyBoy • v1.0.3",
                     icon_url="https://cdn.discordapp.com/avatars/725417693699899534/6d3934a6a8467f0420b530905f7b4361.webp")
    return embed


# Function to create an empty help embed
def empty_help_embed(name, value):
    # Creating an embed object with title, color, and fields
    embed = discord.Embed(title="TLEWikiBot Help", color=0xde8114)
    embed.add_field(name=name, value=value)
    embed.set_footer(text="Created by BestSpyBoy • v1.0.3",
                     icon_url="https://cdn.discordapp.com/avatars/725417693699899534/6d3934a6a8467f0420b530905f7b4361.webp")
    return embed


# Function to create an info embed for the bot
def info_embed():
    # Creating an embed object with title, color, and description
    embed = discord.Embed(title="TLEWikiBot", color=0xde8114,
                          description="A bot created by **@BestSpyBoy** to search and explore the Luxury Elevator Wiki! Type `>help` to get started.")
    embed.set_footer(text="Created by BestSpyBoy • v1.0.3",
                     icon_url="https://cdn.discordapp.com/avatars/725417693699899534/6d3934a6a8467f0420b530905f7b4361.webp")
    return embed


# Function to create an error embed with a given error message
def error_embed(error):
    # Creating an embed object with a red color and the provided error message
    print(error)  # Consider removing or replacing this print statement
    embed = discord.Embed(color=0xFF0000, description=error)
    embed.set_footer(text="Created by BestSpyBoy • v1.0.3",
                     icon_url="https://cdn.discordapp.com/avatars/725417693699899534/6d3934a6a8467f0420b530905f7b4361.webp")
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
    else:
        # Handling other unexpected errors by providing a detailed error message
        await ctx.send(embed=error_embed(f"""An unexpected error occurred when running that command. Ping **@BestSpyBoy** for help.
||```elixir
#{repr(error)}
```||"""))


# Command to display help information
@bot.command(aliases=['commands'])
async def help(ctx, *, arg=None):
    if arg is None:
        await ctx.send(embed=help_embed())
    else:
        await ctx.send(embed=help_embed())


# Command to display bot information
@bot.command(aliases=['information'])
async def info(ctx):
    await ctx.send(embed=info_embed())


# Command to fetch details about a floor from the Luxury Elevator Wiki
@bot.command()
async def floor(ctx, *, arg=None):
    print(">floor")  # Consider removing or replacing this print statement
    if arg is None:
        await ctx.send("<https://wiki.theluxuryelevator.com>")
    else:
        # Parsing arguments and creating a link to the Wiki based on user input
        arguments = re.findall(r'\(.*?\)', arg)
        attribute = re.findall(r'\[.*?]', arg)

        wiki_link = re.sub(r' \(.*?\)| \[.*?]', "", arg)
        wiki_link_parsed = wiki_link.title().replace(" ", "_")

        # Checking for special arguments and responding accordingly
        if "(embed)" in arguments:
            await ctx.send("https://wiki.theluxuryelevator.com/wiki/" + wiki_link_parsed)
        elif "(link)" in arguments:
            await ctx.send("<https://wiki.theluxuryelevator.com/wiki/" + wiki_link_parsed + ">")
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
                r = requests.get("https://wiki.theluxuryelevator.com/w/api.php", params=params)
                r_body = r.json()
                if "error" in r.text:
                    await ctx.send(
                        embed=error_embed("I can't find that floor in the wiki. Do you want to `>create` it?"))
                else:
                    floor_attributes = convert_wikitext_to_dict(r_body.get("parse").get("wikitext"))
                    if floor_attributes is None:
                        await ctx.send(embed=error_embed("That wiki page isn't a floor. Maybe there's no infobox?"))
                        return

                    # Responding with floor details or a specific attribute if provided
                    if not attribute:
                        embed = discord.Embed(title="Floor Details", color=0xde8114)
                        for key, value in floor_attributes.items():
                            if key == "image1":
                                embed.set_image(
                                    url="https://wiki.theluxuryelevator.com/wiki/Special:Filepath/" + urllib.parse.quote(
                                        value))
                            elif key == "title1":
                                embed.add_field(name="Name",
                                                value=f"[{floor_attributes.get('title1')}](https://wiki.theluxuryelevator.com/wiki/{urllib.parse.quote(wiki_link_parsed)})")
                            else:
                                embed.add_field(name=key.title().replace("_", " "),
                                                value=value)
                        embed.set_footer(text="Created by BestSpyBoy • v1.0.3",
                                         icon_url="https://cdn.discordapp.com/avatars/725417693699899534/6d3934a6a8467f0420b530905f7b4361.webp")
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
        await ctx.send("<https://wiki.theluxuryelevator.com/w/index.php?title=" + wiki_link_parsed + "&veaction=edit>")


# Command to provide a link to the Luxury Elevator Wiki
@bot.command()
async def wiki(ctx, *, arg=None):
    await ctx.send("<https://wiki.theluxuryelevator.com>")


# Command to search the Luxury Elevator Wiki and display results
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
            r = requests.get("https://wiki.theluxuryelevator.com/w/api.php", params=params)
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
                embed = discord.Embed(title="Search Results", color=0xde8114, description=embed_desc)
                embed.set_footer(text="Created by BestSpyBoy • v1.0.3",
                                 icon_url="https://cdn.discordapp.com/avatars/725417693699899534/6d3934a6a8467f0420b530905f7b4361.webp")
                await ctx.send(embed=embed)

        except:
            await ctx.send(embed=error_embed("Something went wrong processing your search."))


# Command to provide a link for users to sign up on the Luxury Elevator Wiki
@bot.command()
async def signup(ctx, *, arg=None):
    await ctx.send("<https://wiki.theluxuryelevator.com/wiki/Special:CreateAccount>")


# Command to provide a link to recent changes on the Luxury Elevator Wiki
@bot.command()
async def recent(ctx, *, arg=None):
    await ctx.send("<https://wiki.theluxuryelevator.com/wiki/Special:RecentChanges>")


# Command to provide a link to recent changes on the Luxury Elevator Wiki
@bot.command()
async def link(ctx, *, arg=None):
    wiki_link = re.sub(' \(.*?\)', "", arg)
    wiki_link_parsed = wiki_link.title().replace(" ", "_")
    await ctx.send(f"<https://wiki.theluxuryelevator.com/wiki/{wiki_link_parsed}/>")


# Running the Discord bot with the provided token
bot.run(os.getenv('DISCORD_TOKEN'))
