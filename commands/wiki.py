import discord
import re
import requests
import urllib.parse
from wiki_to_dict import convert_wikitext_to_dict
from discord.ext import commands
import toml
from commands.embeds import error_embed, info_embed

from os import path

basepath = path.dirname(__file__)
filepath = path.abspath(path.join(basepath, "..", "config.toml"))
with open(filepath, "r") as f:
    data = toml.load(f)
    bot_brand_color = data['BotBrandColor']
    bot_version_number = data['BotVersionNumber']

    credit_name = data['credits']['CreditName']
    credit_profile = data['credits']['CreditProfile']

    wiki_commands_enabled = data['wiki']['WikiCommandsEnabled']
    wiki_url = data['wiki']['WikiURL']


class WikiCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # wiki_url = passed_wiki_url
        # self._last_member = None

    # @commands.Cog.listener()
    # async def on_member_join(self, member):
    #     channel = member.guild.system_channel
    #     if channel is not None:
    #         await channel.send(f'Welcome {member.mention}.')

    # Command to fetch details about a page in the Wiki
    @commands.command(aliases=['floor'])
    async def page(self, ctx, *, arg=None):
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
                await ctx.send(f"{wiki_url}/wiki/" + urllib.parse.quote(wiki_link_parsed), )
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
                            await ctx.send(embed=error_embed(
                                f"[That wiki page]({wiki_url}/wiki/{urllib.parse.quote(wiki_link_parsed)}) isn't a floor. Maybe there's no infobox?"))
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
    @commands.command()
    async def create(self, ctx, *, arg=None):
        if arg is None:
            await ctx.send(embed=error_embed("`>create` requires an argument."))
        else:
            wiki_link = re.sub(' \(.*?\)', "", arg)
            wiki_link_parsed = wiki_link.title().replace(" ", "_")
            await ctx.send(f"<{wiki_url}/w/index.php?title=" + wiki_link_parsed + "&veaction=edit>")

    # Command to search the Wiki and display results
    @commands.command()
    async def search(self, ctx, *, arg=None):
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
    @commands.command()
    async def signup(self, ctx, *, arg=None):
        await ctx.send(f"<{wiki_url}/wiki/Special:CreateAccount>")

    # Command to provide special links to the Wiki
    @commands.command()
    async def wiki(self, ctx, *, arg=None):
        if arg is None:
            await ctx.send(f"<{wiki_url}>")
        elif arg == "recent":
            await ctx.send(f"<{wiki_url}/wiki/Special:RecentChanges>")
        elif arg == "signup":
            await ctx.send(f"<{wiki_url}/wiki/Special:RecentChanges>")
        else:
            await ctx.send(embed=error_embed("That isn't a"))  # was an accident, but it's funny so i'm keeping it

    # Command to provide a link to pages on the Wiki
    @commands.command(aliases=['link'])
    async def wikilink(self, ctx, *, arg=None):
        if arg is None:
            await ctx.send(embed=error_embed("`>wikilink` requires an argument."))
        else:
            wiki_link = re.sub(' \(.*?\)', "", arg)
            wiki_link_parsed = wiki_link.title().replace(" ", "_")
            await ctx.send(f"<{wiki_url}/wiki/{wiki_link_parsed}>")

    # Command to link to the Floors List on the Luxury Elevator Wiki
    @commands.command(aliases=['floorslist'])
    async def floorlist(self, ctx, *, arg=None):
        await ctx.send(f"<{wiki_url}/wiki/Floors_List>")
