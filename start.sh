#!/bin/bash

# Navigate to the directory containing bot.py (assuming this script is in the same directory)
BASE_DIR=$(dirname "$(readlink -f "$0")")
cd "$BASE_DIR"

# Create a new screen session named 'ssh' and run the following commands within it
screen -dmS ssh bash -c "
    # Create a Python virtual environment
    python3 -m venv myenv;

    # Activate the virtual environment
    source myenv/bin/activate;

    # Install required Python packages
    pip3 install -r requirements.txt;

    # Run the bot
    python3 main.py;

    # Keep the screen session open
    exec bash
"

# Attach to the screen session
screen -r ssh
