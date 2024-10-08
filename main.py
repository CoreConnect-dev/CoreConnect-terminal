from typing import Final
from telegram.ext import Application, CommandHandler, MessageHandler, filters
from bot import start_command, help_command, add_admin, add_server_handler, del_server_handler, servers_list, connect_to_server_handler, disconnect_from_server, command_handler, error

TOKEN: Final = ''
BOT_USERNAME: Final = "@"

if __name__ == '__main__':
    print("Starting bot...")
    app = Application.builder().token(TOKEN).build()

    # Commands
    app.add_handler(CommandHandler('start', start_command))
    app.add_handler(CommandHandler('help', help_command))
    app.add_handler(CommandHandler('add_admin', add_admin))
    app.add_handler(CommandHandler('add_server', add_server_handler))
    app.add_handler(CommandHandler('del_server', del_server_handler))
    app.add_handler(CommandHandler('servers_list', servers_list))
    app.add_handler(CommandHandler('connect', connect_to_server_handler))
    app.add_handler(CommandHandler('disconnect', disconnect_from_server))

    # Messages
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, command_handler))

    # Errors
    app.add_error_handler(error)

    print("Starting...")
    app.run_polling(poll_interval=3)