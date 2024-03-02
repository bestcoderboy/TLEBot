import difflib
import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from commands.embeds import error_embed, help_embed, info_embed, empty_embed
import toml
from os import path
#
# --- IMPORT SETTINGS ---
base_path = path.dirname(__file__)
file_path = path.abspath(path.join(base_path, "../config.toml"))
with open(file_path, "r") as f:
    print("Opening config")
    data = toml.load(f)
    # bot_name = data['Bot']['Name']
    # bot_description = data['Bot']['Description']
    bot_prefix = data['Bot']['Prefix']
    bot_brand_color = data['Bot']['BrandColor']
    bot_version_number = data['Bot']['Version']
    guild_id_array = data['Bot']['EnabledGuilds']

    credit_name = data['Credit']['Name']
    credit_profile = data['Credit']['Profile']

    modules_enabled = data['Bot']['Modules']
    print("Config initialised")


load_dotenv()  # load all the variables from the env file
bot = discord.Bot()

for cog in modules_enabled:
    print(f"Added {cog} to bot")
    bot.load_extension(f'commands.{cog}')

@bot.event
async def on_ready():
    print(f"{bot.user} is ready and online!")


# Command to change the bot's settings. TODO: Expand settings to change from bot
@bot.command(guild_ids=guild_id_array, description="Admin command to change bot settings")
@commands.has_permissions(administrator=True)
async def settings(ctx, *, setting=None):
    if setting is None:
        await ctx.respond(embed=error_embed("⚠️ >settings needs an option to change and a value."))
    else:
        command = setting.split(" ", 2)
        if command[0] == "activity":
            # could do streaming here but w h y
            if command[1] == "playing" and len(command) == 3:
                await bot.change_presence(activity=discord.Game(name=command[2]))
                await ctx.respond(embed=empty_embed(f"✅  Successfully set presence to 'Playing {command[2]}'"), ephemeral=True)
            elif command[1] == "listening":
                await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=command[2]))
                await ctx.respond(embed=empty_embed(f"✅  Successfully set presence to 'Listening to {command[2]}'"), ephemeral=True)
            elif command[1] == "watching":
                await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name=command[2]))
                await ctx.respond(embed=empty_embed(f"✅  Successfully set presence to 'Watching {command[2]}'"), ephemeral=True)
            else:
                await ctx.respond(embed=error_embed("⚠️ Invalid syntax for the activity setting."), ephemeral=True)


# Event handler for command errors
@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        # Handling command not found errors by suggesting a similar command
        user_command = ctx.message.content.split()[0][1:]
        all_commands = [command.name for command in bot.commands]
        closest_match = difflib.get_close_matches(user_command, all_commands, n=1)
        if closest_match:
            await ctx.respond(embed=error_embed(f"⚠️ Did you mean `{bot_prefix}{closest_match[0]}`?"))
        else:
            await ctx.respond(embed=error_embed("⚠️ Command not found. Use '>help' to see available commands."))
    elif isinstance(error, commands.MissingPermissions):
        await ctx.respond(embed=error_embed("⚠️ This is an admin-only command - check you have the permissions to run it."))
    else:
        # Handling other unexpected errors by providing a detailed error message
        await ctx.respond(embed=error_embed(f"""⚠️ An unexpected error occurred when running that command. Ping **@{credit_name}** for help.
||```elixir
#{repr(error)}
```||"""))


# Command to display help information
@bot.command(aliases=['commands'], guild_ids=guild_id_array, description="Shows the help embed")
async def help(ctx):
    await ctx.respond(embed=help_embed())


# Command to display bot information
@bot.command(aliases=['information'], guild_ids=guild_id_array, description="Shows info about the bot")
async def info(ctx):
    await ctx.respond(embed=info_embed())


bot.run(os.getenv('DISCORD_TOKEN'))  # run the bot with the token
