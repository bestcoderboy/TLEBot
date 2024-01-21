import discord
import random as rand_lib
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

    wiki_url = data["Wiki"]["URL"]


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
    "More fun facts are coming soon, promise!",

]
fun_facts = original_fun_facts

fun_fact = ""
previous_facts = []

class CustomCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        # wiki_url = passed_wiki_url
        # self._last_member = None

    # Command to give random facts - why not?
    @commands.slash_command(aliases=['randomfact', 'funfact', 'facts']commands.slash_command, description="Gives random facts about the game")
    async def fact(self, ctx):
        global fun_facts, fun_fact, previous_facts  # Needed to stop error
        if len(fun_facts) == 0:  # Resets the fun facts
            print("fun facts reset")
            fun_facts = original_fun_facts
            rand_lib.shuffle(fun_facts)
            fun_fact = fun_facts.pop()
            previous_facts.append(fun_fact)
            # print(previous_facts)
            # print(fun_fact)
        else:
            print("running fact")
            previous_facts.append(fun_fact)
            fun_fact = fun_facts.pop()
            if fun_fact in previous_facts:
                fun_facts.insert(0, fun_fact)
                fun_fact = fun_facts.pop()
            if len(previous_facts) > 3:
                previous_facts.pop(1)
            # print(previous_facts)
            # print(fun_fact)

        # print(current_fun_fact)
        print(fun_facts)
        embed = discord.Embed(title="Fun fact", color=bot_brand_color, description=f"""{fun_fact}""")
        embed.set_footer(text=f"Created by {credit_name} • {bot_version_number}",
                         icon_url=credit_profile)
        await ctx.respond(embed=embed)

    @commands.slash_command(aliases=['credit']commands.slash_command, description="Shows the game's credits")
    async def credits(self, ctx):
        embed = discord.Embed(title="TLE Credits", color=bot_brand_color, description=f"""Game Creator: **Milo Murphy**
    Lead Developer / Game Owner: **Ferb_Fletcher**
    (retired) Developer: **Phineas_Flynn**
        """)
        embed.set_footer(text=f"Created by {credit_name} • {bot_version_number}",
                         icon_url=credit_profile)
        await ctx.respond(embed=embed)

    # Command to link to the Floors List on the Luxury Elevator Wiki
    @commands.slash_command(aliases=['floorslist']commands.slash_command,
                            description="Returns a link to the Floors List")
    async def floorlist(self, ctx):
        await ctx.respond(f"<{wiki_url}/wiki/Floors_List>")


def setup(bot):  # this is called by Pycord to set up the cog
    bot.add_cog(CustomCommands(bot))  # add the cog to the bot
