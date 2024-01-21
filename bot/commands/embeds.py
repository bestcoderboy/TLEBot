import os
import discord
import toml
from os import path

# --- IMPORT SETTINGS ---
basepath = path.dirname(__file__)
filepath = path.abspath(path.join(basepath, "../..", "config.toml"))
with open(filepath, "r") as f:
    data = toml.load(f)
    bot_name = data['Bot']['Name']
    bot_description = data['Bot']['Description']
    bot_prefix = data['Bot']['Prefix']
    bot_brand_color = data['Bot']['BrandColor']
    bot_version_number = data['Bot']['VersionNumber']

    credit_name = data['Credit']['Name']
    credit_profile = data['Credit']['Profile']


# Function to create a help embed for commands
def help_embed():
    # Creating an embed object with title, color, and fields
    embed = discord.Embed(title=f"{bot_name} Help", color=bot_brand_color)
    embed.add_field(name=f"{bot_prefix}floor `<page name>`", value="Returns details about the floor given.")
    embed.add_field(name=f"{bot_prefix}search `<query>`", value="Returns search results for that query.")
    embed.add_field(name=f"{bot_prefix}create `<page name>`", value="Generates a link to create a wiki page with the name given.")
    embed.add_field(name=f"{bot_prefix}signup", value="Returns a link to sign up to the Wiki.")
    embed.add_field(name=f"{bot_prefix}help", value="Shows this embed.")
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
    print(error)
    # Creating an embed object with a red color and the provided error message
    embed = discord.Embed(color=0xFF0000, description=error)
    embed.set_footer(text=f"Created by {credit_name} • {bot_version_number}",
                     icon_url=credit_profile)
    return embed