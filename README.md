# TLEBot

![GitHub Release](https://img.shields.io/github/v/release/bestcoderboy/TLEBot?color=g)
![Language: Python](https://img.shields.io/badge/language-python-blue)
![GitHub Commits](https://img.shields.io/github/commit-activity/t/bestcoderboy/TLEBot?color=red)
![GitHub License](https://img.shields.io/github/license/bestcoderboy/TLEBot)

🤖 **A multi-purpose Discord bot for game servers, originally designed for The Luxury Elevator.**

⚒️ **Easy to set up and available to use for any game's Discord server, official or otherwise.**

🌐 **Links with MediaWiki or Fandom wikis seamlessly, with easily customisable commands.**

🎨 **Customise your bot's appearance and profile, and completely control its data.**
## 💻 Get started with the bot
This guide is for how to set up and run the bot on a server / computer. 

**If you don't want to run it on your own computer**, we recommend using a [DigitalOcean droplet](https://m.do.co/c/084de397ebb4) (get $200 in credit with this affiliate link).

If you're a Python and Git user already, and have set up your Discord bot, you can skip to [this section](#-running-the-bot) to start running the bot. 

Otherwise, we recommend reading the guide below to set up and run the bot for your own server.

## 🔑 Creating the bot's account
To create an "application" or bot on Discord, you first need to go to the [**Discord Developer Portal**](https://discord.com/developers/applications).

Once you're logged in, click the **"New Application"** button in the top-right corner, type in your bot's name and accept the Developer Terms of Service.

This is where you can customise the bot's appearance. You can add a profile picture, change its description - add tags if you really want to!

Next, you're going to go to the **Bot** section. Here, you'll see the bot has already been created. Scroll down and toggle **"Message Content Intent"**.

You could get your bot token now, but you'll only need it at the end, so for now let's add the bot to your server.

Go to the **OAuth2** section of the page, and click **URL Generator**. You'll see checkboxes - tick `bot`, then when the second box appears tick `Send Messages`.

Scroll down to the bottom and click the **Copy** button to copy the invite link to your clipboard. Open a new tab, paste the URL and add the bot to your server.

## 🤔 Setting up your computer for the bot
First, let's check if you have Python installed on your computer by opening your computer's terminal.

On Windows, this is called **PowerShell** or **Command Prompt** (they do the same thing), and on macOS it is called **Terminal**.

Open the terminal, then run this command in the terminal to check if you have Python installed.
```shell
python --version
```

If you have Python already, it should respond with something like `Python 3.12.1`.

If it responds with a red error, or the number starts with 2 instead of 3, you'll need to [install Python](https://www.python.org/downloads/).

Now let's check for Git, another tool we need to use during setup. Run this command, and if it's not installed, [download it](https://www.git-scm.com/downloads).
```shell
git --version
```

Now you can proceed to the next step - setting up the bot.

## 🧑‍💻 Running the bot

Let's get the code to run the bot ready. Create a new folder anywhere you want, then open your terminal again.

In the terminal, navigate to the folder you created by running the command below - for example, `cd "C:/Users/best/Documents/MyGameBot"`.
```shell
cd <your-folder-path>
```

We can now use Git to clone this repo to your local machine. Run this command to copy the files.
```shell
git clone https://github.com/bestcoderboy/TLEBot.git
```

Now that everything is ready, let's create a virtual environment for Python to use by running `python -m venv discord-bot` in your shell.

Once the virtual environment is created, run the activation script for your OS:

 - Windows: `.\discord-bot\Scripts\activate` for Command Prompt, `.\discord-bot\Scripts\Activate.ps1` for PowerShell
 - Mac or Linux: `source discord-bot/bin/activate`

After running the script, you will see the name of the environment like `(discord-bot)` next to the shell.

Next, run this command to install all the Python packages needed to run the bot (you may have to use `pip3` instead of `pip`).
```shell
pip install -r requirements.txt
```

Now you'll get your **bot token**. Remember the [Discord Developer Portal](https://discord.com/developers/applications)? Let's go back to your application's **Bot** tab again.

Click **"Reset Token"**, and if you have two-factor authentication, verify yourself with the code. You'll see the token to copy on the screen.
> [!CAUTION]
> ⚠️ This token should be kept **very safe** - treat it like your password and don't share it with anyone.

To authenticate the bot, create a `.env` file inside the `/discord-bot/` folder and put the bot token you just copied inside it like this:

```env
DISCORD_TOKEN=ABCDEF123-your-token-here-456WXYZ
```

Finally, run this command to run the script and start the bot.

```shell
python main.py
```