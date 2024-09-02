#!/bin/bash

# Update and install required packages
sudo apt-get update
sudo apt-get install -y python3 python3-pip python3-venv screen

# Navigate to the directory containing bot.py (assuming this script is in the same directory)
BASE_DIR=$(dirname "$(readlink -f "$0")")
cd "$BASE_DIR"

# Prompt the user to paste their private key
PRIVATE_KEY_PATH="$BASE_DIR/id_rsa"
echo "Please paste your RSA private key (including the '-----BEGIN RSA PRIVATE KEY-----' and '-----END RSA PRIVATE KEY-----' lines), then press Ctrl+D:"
cat > "$PRIVATE_KEY_PATH"

# Check if the private key was saved successfully
if [[ -f "$PRIVATE_KEY_PATH" ]]; then
    echo "Private key saved successfully to $PRIVATE_KEY_PATH."

    # Set permissions for the private key
    chmod 600 "$PRIVATE_KEY_PATH"
    echo "Private key permissions set to 600."
else
    echo "Failed to save the private key."
    exit 1
fi

# Prompt the user to add their Telegram ID to admins.txt
echo "Please enter your Telegram ID (admin ID):"
read TELEGRAM_ID
echo "$TELEGRAM_ID" > admins.txt
echo "Telegram ID saved to admins.txt."

# Prompt the user to enter their Telegram bot token and username
echo "Please enter your Telegram bot token:"
read TOKEN
echo "Please enter your Telegram bot username (starting with @):"
read BOT_USERNAME

# Ensure the bot username starts with '@'
if [[ "$BOT_USERNAME" != @* ]]; then
    echo "Bot username must start with '@'."
    exit 1
fi

# Replace the token and bot username in main.py
sed -i "s|TOKEN: Final = ''|TOKEN: Final = '$TOKEN'|" main.py
sed -i "s|BOT_USERNAME: Final = \"@\"|BOT_USERNAME: Final = \"$BOT_USERNAME\"|" main.py

# Confirm the changes
echo "Bot token and username have been set in main.py."
