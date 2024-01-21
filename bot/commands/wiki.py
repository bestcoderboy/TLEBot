import discord
import re
import requests
import urllib.parse

from discord import option
# noinspection PyUnresolvedReferences
from libs.wiki_to_dict import convert_wikitext_to_dict
from discord.ext import commands
import toml
# noinspection PyUnresolvedReferences
from commands.embeds import error_embed
from os import path

# --- IMPORT SETTINGS ---
basepath = path.dirname(__file__)
filepath = path.abspath(path.join(basepath, "../..", "config.toml"))
with open(filepath, "r") as f:
    data = toml.load(f)
    bot_brand_color = data['Bot']['BrandColor']
    bot_version_number = data['Bot']['Version']

    credit_name = data['Credit']['Name']
    credit_profile = data['Credit']['Profile']

    wiki_url = data['Wiki']['URL']


class WikiCommands(commands.Cog):
    def __init__(self, bot):  # this is a special method that is called when the cog is loaded
        self.bot = bot

    # Command to fetch details about a page in the Wiki
    @option(
        "floor",
        description="The floor's name to retrieve",
        required=True,
        default=''
    )
    @commands.slash_command(aliases=['floor'], description="Returns information about a wiki page")
    async def floor(self, ctx, *, floor=None):
        if floor is None:
            await ctx.respond(f"<{wiki_url}>")
        else:
            # Parsing flooruments and creating a link to the Wiki based on user input
            arguments = re.findall(r'\(.*?\)', floor)
            attribute = re.findall(r'\[.*?]', floor)
            exact_value = re.findall(r'".*?"', floor)

            wiki_link = re.sub(r' \(.*?\)| \[.*?]|"', "", floor)
            wiki_link_parsed = wiki_link.replace(" ", "_")
            if len(exact_value) == 0:
                wiki_link_parsed = wiki_link_parsed.title()

            # Checking for special flooruments and responding accordingly
            if "(embed)" in arguments:
                await ctx.respond(f"{wiki_url}/wiki/{urllib.parse.quote(wiki_link_parsed)}")
            elif "(link)" in arguments:
                await ctx.respond(f"<{wiki_url}/wiki/{urllib.parse.quote(wiki_link_parsed)}>")
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
                        await ctx.respond(
                            embed=error_embed(f"""I can't find **{urllib.parse.quote(wiki_link_parsed).replace('_', ' ')}** in the wiki. Do you want to `/create` it?
 > You may want to check the capitalisation of the page's name."""))
                    else:
                        floor_attributes = convert_wikitext_to_dict(r_body.get("parse").get("wikitext"))
                        if floor_attributes is None:
                            await ctx.respond(embed=error_embed(
                                f"[{urllib.parse.quote(wiki_link_parsed).replace('_', ' ')}]({wiki_url}/wiki/{urllib.parse.quote(wiki_link_parsed)}) isn't a floor. Maybe there's no infobox?"))
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
                            await ctx.respond(embed=embed)
                        else:
                            attribute_parsed = re.sub('\[', "", attribute[0])
                            attribute_parsed = re.sub(']', "", attribute_parsed)
                            await ctx.respond(
                                f" > The {attribute_parsed} of {floor_attributes.get('title1')} is **{floor_attributes.get(attribute_parsed)}**.")
                except requests.exceptions.Timeout:
                    await ctx.respond(embed=error_embed("The request to the server timed out :cry:"))

    # Command to generate a link for creating a new Wiki page
    @commands.slash_command(description="Returns a link to create a wiki page")
    @option(
        "page",
        description="The page name to create",
        required=True,
        default=''
    )
    async def create(self, ctx, *, page):
        if page is None:
            await ctx.respond(embed=error_embed("`>create` requires an argument."))
        else:
            wiki_link = re.sub(' \(.*?\)', "", page)
            wiki_link_parsed = wiki_link.title().replace(" ", "_")
            await ctx.respond(f"<{wiki_url}/w/index.php?title=" + wiki_link_parsed + "&veaction=edit>")

    # Command to search the Wiki and display results
    @commands.slash_command(description="Searches the wiki for pages.")
    @option(
        "query",
        description="The query to search for",
        required=True,
        default=''
    )
    async def search(self, ctx, *, query=None):
        print(query)
        if query is None:
            await ctx.respond(embed=error_embed("`>search` requires an argument."))
        else:
            try:
                # Making a request to the Wiki API to perform a search
                params = {
                    "action": "query",
                    "list": "search",
                    "srsearch": urllib.parse.quote(query),
                    "format": "json"
                }
                r = requests.get(f"{wiki_url}/w/api.php", params=params)
                r_body = r.json()
                print(r_body)
                search_array = r_body.get("query").get("search")
                print(search_array)

                # Responding with search results or an error message if no results are found
                if not search_array:
                    await ctx.respond(embed=error_embed("Couldn't find a result!"))
                else:
                    embed_desc = ""
                    for value in search_array:
                        embed_desc += f"""
    • [{value.get("title")}]({wiki_url}/wiki/{value.get("title").replace(" ","_")})"""
                    if len(search_array) == 10:
                        embed_desc += f"""
    > Note: will only return up to ten results"""
                    embed = discord.Embed(title="Search Results", color=bot_brand_color, description=embed_desc)
                    embed.set_footer(text=f"Created by {credit_name} • {bot_version_number}",
                                     icon_url=credit_profile)
                    await ctx.respond(embed=embed)
            except:
                await ctx.respond(embed=error_embed("Something went wrong processing your search."))

    # Command to provide a link for users to sign up on the Wiki
    @commands.slash_command(description="Returns a link to sign up for the wiki")
    async def signup(self, ctx):
        await ctx.respond(f"<{wiki_url}/wiki/Special:CreateAccount>")

    # Command to provide special links to the Wiki
    @commands.slash_command(description="Returns a link to the wiki")
    async def wiki(self, ctx, *, arg=None):
        if arg is None:
            await ctx.respond(f"<{wiki_url}>")
        elif arg == "recent":
            await ctx.respond(f"<{wiki_url}/wiki/Special:RecentChanges>")
        elif arg == "signup":
            await ctx.respond(f"<{wiki_url}/wiki/Special:RecentChanges>")
        else:
            await ctx.respond(embed=error_embed("That isn't a"))  # was an accident, but it's funny so i'm keeping it

    # Command to provide a link to pages on the Wiki
    @commands.slash_command(aliases=['link'], description="Provides a link to the wiki")
    async def wikilink(self, ctx, *, link=None):
        if link is None:
            await ctx.respond(embed=error_embed("`>wikilink` requires an argument."))
        else:
            wiki_link = re.sub(' \(.*?\)', "", link)
            wiki_link_parsed = wiki_link.title().replace(" ", "_")
            await ctx.respond(f"<{wiki_url}/wiki/{wiki_link_parsed}>")


def setup(bot):  # this is called by Pycord to set up the cog
    bot.add_cog(WikiCommands(bot))  # add the cog to the bot
