# TLEBot

🤖 **A multi-purpose Discord bot for game servers, originally designed for The Luxury Elevator.**

⚒️ **Easy to set up and available to use for any game's Discord server, official or otherwise.**

🌐 **Links with MediaWiki or Fandom wikis seamlessly, with easily customisable commands.**

🎨 **Customise your bot's appearance and profile.**
## 💻 Get started with the bot
If you're a Python and Git user already, you can skip to [this section](#i-have-everything-set-up-now-what) to start running the bot. 

Otherwise, we recommend reading the guide below to set up and run the bot for your own server.

## 🤔 I'm a beginner. How do I run the bot?
First, let's check if you have Python installed on your computer by opening your computer's terminal.

On Windows, this is called **PowerShell** or **Command Prompt** (they do the same thing), and on macOS it is called **Terminal**.

Open the terminal, then run the command `python --version` in the terminal to check if you have Python installed.

If you have Python already, it should respond with something like `Python 3.12.1`.

If it responds with a red error, or the number starts with 2 instead of 3, you'll need to [install Python](https://www.python.org/downloads/).

Now let's check for Git, another tool we need to use during setup. Run `git --version`, and if it's not installed, [download it](https://www.git-scm.com/downloads).

Now you can proceed to the next step - setting up the bot.

## 🧑‍💻 I have everything set up. Now what?

Let's get the code to run the bot ready. Create a new folder anywhere you want, then open your terminal again.

In the terminal, navigate to the folder you created by running `cd <folder-path>` - for example, `cd "C:/Users/bests/Documents/MyGameBot"`.

We can now use Git to clone this repo to your local machine. Run `git clone https://github.com/bestcoderboy/TLEBot` to copy the files.

Now that everything is ready, let's create a virtual environment for Python to use by running `python -m venv discord-bot` in your shell.

Once the virtual environment is created, run the activation script for your OS:

 - Windows: `.\discord-bot\Scripts\activate` for Command Prompt, `.\discord-bot\Scripts\Activate.ps1` for PowerShell
 - Mac or Linux: `source discord-bot/bin/activate`

After running the script, you will see the name of the environment, like `(discord-bot)`, next to the shell.

Run `pip install -r requirements.txt` to install all the necessary packages for the bot.

Then create a `.env` file and put your discord token inside like this:

```env
DISCORD_TOKEN=<YOUR-TOKEN-HERE>
```

Finally, run `python main.py` to run the script and start the bot.
