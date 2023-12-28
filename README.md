# TLEWikiBot
## Getting started
To host the TLEWikiBot locally, follow these steps.

First, create a virtual environment for Python to use by running `python -m venv discord-bot`.

Once the virtual environment is created, run the activation script for your OS:

 - Windows: `.\discord-bot\Scripts\activate` for Command Prompt, .\discord-bot\Scripts\Activate.ps1` for PowerShell
 - Mac or Linux: `source discord-bot/bin/activate`

After running the script, you will see the name of the environment, like `(discord-bot)`, next to the shell.

Run `pip install -r requirements.txt` to install all necessary packages.

Then create a `.env` file and put your discord token inside like this:

```env
DISCORD_TOKEN=<YOUR-TOKEN-HERE>
```

Finally, run `python main.py` to run the script and start the bot.
