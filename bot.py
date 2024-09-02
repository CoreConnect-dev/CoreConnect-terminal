import os
import json
from telegram import Update
from telegram.ext import ContextTypes
import paramiko
from time import gmtime, strftime
from authentication import isAdminUser, add_admin_to_file
from servers import get_servers_data, is_valid_ip, del_server, add_server, client, do_command, is_connected_to_server

# Path to the stored SSH key in the same directory as bot.py
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SSH_KEY_PATH = os.path.join(BASE_DIR, 'id_rsa')

# Path to servers data file
SERVERS_DATA_FILE = os.path.join(BASE_DIR, 'servers.json')

# Helper function to load servers
def load_servers():
    if os.path.exists(SERVERS_DATA_FILE):
        with open(SERVERS_DATA_FILE, 'r') as f:
            return json.load(f)
    return []

# Helper function to save servers
def save_servers(servers):
    with open(SERVERS_DATA_FILE, 'w') as f:
        json.dump(servers, f)

# Function to clear all servers (useful for debugging or resetting)
def clear_servers():
    save_servers([])

# Load servers at the start
servers = load_servers()

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('Welcome to **CORE TERMINAL**\nInteract and make server commands through telegram!', parse_mode="Markdown")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Here are the available commands:\n\n"
        "/start - Start the bot and see the welcome message.\n"
        "/help - Show this help message.\n"
        "/add_server <IP> <username> - Add a new server with the provided IP and username. This also adds the user as an admin.\n"
        "/del_server <number> - Delete a server from the list by its number.\n"
        "/servers_list - List all added servers with their details.\n"
        "/connect <number> - Connect to a server from the list by its number.\n"
        "/disconnect - Disconnect from the currently connected server.\n"
    )

async def add_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if isAdminUser(update.message.chat.id):
        data: str = update.message.text
        proccessed_data: str = data.replace("/add_admin", '').strip()
        print(f">> new admin added by ({update.message.chat.username} {update.message.chat.id}). \n{proccessed_data} is now admin,\n")
        add_admin_to_file(proccessed_data)
        await update.message.reply_text(f"New admin added \n{proccessed_data} is now admin.")
    else:
        await update.message.reply_text("You don't have access to add a new admin.")

async def del_server_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    sender: str = update.message.chat.id
    if isAdminUser(update.message.chat.id) or isAdminUser(update.message.chat.username):
        data: str = update.message.text
        proccessed_data: int = int(str(data.replace("/del_server", '').strip()))
        if 0 < proccessed_data <= len(servers):
            server = servers.pop(proccessed_data - 1)
            save_servers(servers)
            print(f'>> A server deleted by ({update.message.chat.username} {update.message.chat.id})\n - Server IP : {server[0]}\n - Username : {server[1]}',
                  end="")
            await update.message.reply_text(f'Server Deleted\n'
                                            f'Server IP : {server[0]}\n'
                                            f'Username : {server[1]}\n'
                                            f'Deleted by : {sender} in {strftime("%Y-%m-%d %H:%M:%S", gmtime())}\n')
        else:
            await update.message.reply_text(f"Server doesn't exist, try again")
    else:
        await update.message.reply_text(f'You need admin access to delete a server!')

async def add_server_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    sender: str = update.message.chat.id
    if isAdminUser(sender) or isAdminUser(update.message.chat.username):
        data: str = update.message.text
        proccessed_data: str = data.replace("/add_server", '').strip()
        proccessed_data_list = proccessed_data.split(maxsplit=2)

        if len(proccessed_data_list) != 2:
            await update.message.reply_text("Invalid command format. Please use: /add_server <IP> <username>")
            return

        ip_address = proccessed_data_list[0]
        username = proccessed_data_list[1]

        if is_valid_ip(ip_address):
            await update.message.reply_text(f'IP validation successful.')
            server_info = [ip_address, username, SSH_KEY_PATH, sender, strftime("%Y-%m-%d %H:%M:%S", gmtime())]
            servers.append(server_info)
            save_servers(servers)
            await update.message.reply_text(f'Server added! Now you can connect to it using /connect <server number>.')
        else:
            await update.message.reply_text(f'Adding new server failed!\nPlease enter a valid IP.')
    else:
        await update.message.reply_text(f'You need admin access to add a new server!')

async def servers_list(update: Update, context: ContextTypes.DEFAULT_TYPE):
    sender: str = update.message.chat.id
    if isAdminUser(update.message.chat.id) or isAdminUser(update.message.chat.username):
        print(f">> List of servers asked by : ({update.message.chat.username} {update.message.chat.id}).")
        table = "All Servers:\n\n\n"
        counter = 1
        for server in servers:
            table += (f"Server Number : {counter}\n"
                      f"Server IP : {server[0]}\n"
                      f"Added By : {server[3]}\n"
                      f"Date Added : {server[4]}\n\n---------\n")
            counter += 1
        await update.message.reply_text(table)
    else:
        await update.message.reply_text(f'You need admin access to view the list of servers!')

async def connect_to_server_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    sender: str = update.message.chat.id
    global is_connected_to_server
    if isAdminUser(update.message.chat.id) or isAdminUser(update.message.chat.username):
        if is_connected_to_server is False:
            data: str = update.message.text
            proccessed_data: str = data.replace("/connect", '').strip()
            proccessed_data = int(proccessed_data) - 1
            if 0 <= proccessed_data < len(servers):
                server = servers[proccessed_data]
                print(f'>> Trying to connect to server by ({update.message.chat.username} {update.message.chat.id})\n - Server IP : {server[0]}\n - Username : {server[1]}',
                      end="")
                await update.message.reply_text(f'Trying to connect to server\n'
                                                f'Server IP : {server[0]}\n'
                                                f'Username : {server[1]}\n'
                                                f'added by : {server[3]} in {server[4]}\n')
                try:
                    # Load the SSH private key from the specified path
                    if not os.path.isfile(server[2]):
                        raise FileNotFoundError(f"Private key file not found: {server[2]}")
                    
                    private_key = paramiko.RSAKey.from_private_key_file(server[2])
                    
                    # Attempt to connect using the loaded private key
                    client.connect(
                        hostname=server[0],
                        username=server[1],
                        pkey=private_key
                    )
                    print("Successful!!\n")
                    is_connected_to_server = True
                    await update.message.reply_text(f'Successfully connected to server!')
                except Exception as e:
                    print(f"Failed! {e}\n")
                    is_connected_to_server = False
                    await update.message.reply_text(f'Couldn\'t connect to the server! Error: {e}')
            else:
                await update.message.reply_text(f"Server number is invalid. Please check the server list and try again.")
        else:
            await update.message.reply_text(f'Already connected to a server\nplease disconnect first using:\n/disconnect command')
    else:
        await update.message.reply_text(f'You need admin access to connect to a server!')

async def disconnect_from_server(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global is_connected_to_server
    if isAdminUser(update.message.chat.id) or isAdminUser(update.message.chat.username):
        print(
            f'>> Trying to close the connection by ({update.message.chat.username} {update.message.chat.id})\n - Result : ',
            end="")
        if is_connected_to_server is True:
            client.close()
            is_connected_to_server = False
            print("Successfully closed the connection\n")
            await update.message.reply_text("Connection closed!")
        else:
            print("Failed - no connection found!\n")
            await update.message.reply_text("Failed to do the task! (you sure I was connected to a server?)")
    else:
        await update.message.reply_text(f'You need admin access to disconnect from a server!')

def handle_command(text: str) -> str:
    proccessed_text = text.lower()
    global is_connected_to_server
    if is_connected_to_server is True:
        result = do_command(client, proccessed_text)
        return f"*Done!*\n```shell\n{proccessed_text}\n```\n*output:*\n```\n{result}```"
    else:
        return f"I'm not connected to any server.\nPlease connect me with /connect command"

async def command_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    if text.startswith("/add_server"):
        await add_server_handler(update, context)
    elif text.startswith("/connect"):
        await connect_to_server_handler(update, context)
    elif text.startswith("/servers_list"):
        await servers_list(update, context)
    elif text.startswith("/del_server"):
        await del_server_handler(update, context)
    elif text.startswith("/disconnect"):
        await disconnect_from_server(update, context)
    else:
        response: str = handle_command(text)
        await update.message.reply_text(response, parse_mode="markdown")

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f'Update {update} caused {context.error}')
