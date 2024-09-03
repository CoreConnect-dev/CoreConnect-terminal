# Coreconnect Terminal Bot

Coreconnect Terminal Bot allows you to manage and run SSH commands directly through a Telegram bot. This setup guide will walk you through the steps to install, configure, and run the bot on your server.

## Installation

### 1. Clone the Repository
First, clone the Coreconnect Terminal Bot repository to your server:
```bash
git clone https://github.com/CoreConnect-dev/CoreConnect-terminal/
```

2. Navigate to the Repository
Change into the repository directory:
```
cd CoreConnect-terminal
```
3. Make Scripts Executable
```
chmod +x start.sh
chmod +x auto.sh
```

Setup
4. Run the Setup Script
To begin the setup, run the following command:
```
./auto.sh
```

5. Add Your Private SSH Key
The script will prompt you to paste the private SSH key you used to log in to your server. After pasting it, press Ctrl+D twice to continue.

6. Configure Your Telegram Bot
The script will then ask for your Telegram bot token. You can create a new bot and obtain the token using BotFather on Telegram:

Start a conversation with [BotFather](https://t.me/BotFather).
Use the /newbot command.
Choose a name for your bot.
Copy the token provided under "Use this token to access the HTTP API."
Paste this token into your server terminal and press Enter.

7. Enter Your Telegram ID and Bot Username
The script will prompt you to enter your Telegram ID number without @ and bot username (starting with @) Make sure you give your bot @ and not link, for example @mybotname. To find your  Telegram ID, you can use the [UserInfoBot](https://t.me/userdatailsbot).

Continue pressing Enter after providing each piece of information.

8. Start the Bot
Once the setup is complete, you can start the bot using:
```
./start.sh
```
If you've entered all the information correctly, your bot should be up and running, allowing you to execute SSH commands via Telegram.

If you encounter any issues during setup, double-check that you've entered the correct information and that your SSH key is properly configured. If problems persist, consult the repository's issues section or seek help from the community.

```
Upcoming fixes:

1. Change the apt process on the bot to be able to do apt commands from telegram.
2. File uploading and downloading from telegram.
3. Memorize directories diving to be able to run commands/scripts in specific directories.

```
