# TLEBot
## Start using the bot
To host the TLEBot locally, follow these steps:

1. Create a virtual environment for Python to use by running `python -m venv discord-bot` in your shell.

2. Once the virtual environment is created, run the activation script for your OS:

 - Windows: `.\discord-bot\Scripts\activate` for Command Prompt, `.\discord-bot\Scripts\Activate.ps1` for PowerShell
 - Mac or Linux: `source discord-bot/bin/activate`

3. After running the script, you will see the name of the environment, like `(discord-bot)`, next to the shell.

4. Run `pip install -r requirements.txt` to install all necessary packages.

5. Then create a `.env` file and put your discord token inside like this:

```env
DISCORD_TOKEN=<YOUR-TOKEN-HERE>
```

6. Finally, run `python main.py` to run the script and start the bot.
