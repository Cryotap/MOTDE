import endstone.plugin
from endstone.command import *
import array
from endstone.plugin import Plugin
from endstone import ColorFormat
import time
import sqlite3
import random
from endstone.event import EventPriority, ServerLoadEvent, event_handler
from endstone.event import ServerListPingEvent


class Motde(Plugin):
    name = "Motde"
    version = "0.1.0"
    api_version = "0.4"
    description = "My first Python plugin for Endstone servers!"

    commands = {
        "motde": {
            "description": "Set the motd's that the server will shullfe.",
            "usages": ["/motde","/motde [value: str] [value: int]","/motde [value: str] [value: int] [value: message]"],
            "permissions": ["motde.command.usage"],
        },
    }

    permissions = {
        "python_example.command": {
            "description": "Allow users to use the Motde commands.",
            "default": False,
            },
        }

    cf = ColorFormat

    @event_handler
    def ping_event(self, event: ServerListPingEvent):
        con = sqlite3.connect('motdlist.db', timeout=3)
        cursor = con.cursor()
        rows = cursor.execute("SELECT id FROM motds WHERE id IS NOT NULL").fetchall()
        if rows:
            ids = len(rows)
            vals = random.randint(1, ids)
            v = vals
            vald = random.choice(rows)
            vd = int(vald[0])
            feedback = cursor.execute('select motd from motds where id =?', (vd,))
            feedback = cursor.fetchone()
            a = str(feedback)
            event.motd = a.strip("('`,')")
            con.commit()
            con.close()
        else:
            con.commit()
            con.close()


    def on_command(self, sender: CommandSender, command: Command, args: list[str], cf=cf) -> bool:
        if command.name == "motde":
            if len(args) > 0:
                con = sqlite3.connect('motdlist.db', timeout=3)
                cursor = con.cursor()
                if args[0] == "del":
                    cursor.execute('delete from motds where id =?', (args[1],))
                    con.commit()
                    con.close()
                    sender.send_message(f"{cf.MATERIAL_NETHERITE}Deleted!")
                elif args[0] == "add":
                    if len(args) > 1:
                        a = args[1]
                        b = ' '.join(args[2:])
                        c = b.replace('&', '§')
                        rows = cursor.execute("""SELECT id FROM motds WHERE id=?""", (args[1],))
                        cursor.execute('delete from motds where id =?', (args[1],))
                        cursor.execute("""INSERT INTO motds(id,motd) VALUES (?, ?)""", (int(a), c))
                        con.commit()
                        con.close()
                        sender.send_message(f"{cf.AQUA}Added.")
                    else:
                        con.commit()
                        con.close()
                else:
                    sender.send_message(f"{cf.MATERIAL_REDSTONE}/motde add id motd, /motde del id")
                    con.commit()
                    con.close()
            else:
                con = sqlite3.connect('motdlist.db', timeout=3)
                cursor = con.cursor()
                rows = cursor.execute("SELECT motd FROM motds WHERE motd IS NOT NULL").fetchall()
                n = list(rows)
                el = ",".join(str(element) for element in n)
                sender.send_message(f"{cf.AQUA} " + el)
                con.commit()
                con.close()
                sender.send_message(f"{cf.MATERIAL_REDSTONE}/motde add id motd, /motde del id")
                return False
        return True

    def on_load(self) -> None:
        self.logger.info("on_load is called!")

    def on_enable(self) -> None:
        self.logger.info("Booting Up Motde.exe!")
        con = sqlite3.connect('motdlist.db',timeout=3)
        cursor = con.cursor()
        cursor.execute("""CREATE TABLE IF NOT EXISTS motds(id INT PRIMARY KEY, motd TEXT)""")
        con.commit()
        con.close()
        self.register_events(self)

    def on_disable(self) -> None:
        self.logger.info("on_disable is called!")
