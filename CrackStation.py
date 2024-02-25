from typing import Callable, Dict, Optional
#from CommandFactory import CommandFactory
from prompt_toolkit import PromptSession
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.styles import Style
from prompt_toolkit import print_formatted_text, HTML, ANSI
from server_commands import ServerCommands 
from termcolor import colored
from HelpTable import HelpTable
from OptionsTable import OptionsTable
import os

class CrackStation:
    current_command = None
    success = colored('[+] ', 'green')
    fail = colored('[-] ', 'red')
    HelpTable = HelpTable("Help Menu", ["Command", "Description"])
    SettingsTable = OptionsTable("settings", ["Setting", "Value", "Required", "Description"])
    for command in ServerCommands.SList:
        HelpTable.add_row(command, ServerCommands.SList[command]["Description"])
    for setting in ServerCommands.SList["settings"]["Options"]:
        SettingsTable.add_row(setting, ServerCommands.SList["settings"]["Options"][setting], "Yes", "")
    def __init__(self) -> None:
        pass
    
    def input_handler(self, user_input: str) -> None:
        parts = user_input.split(maxsplit=1)
        command = parts[0]
        if len(parts) > 1:
            args = parts[1]
        else:
            args = ""

        if command == "exit":
            exit()
        elif command == "help":
            self.HelpTable.display()
        elif command == "settings":
            self.current_command = "settings"
        elif command == "back":
            self.current_command = None
        elif command == "show" and args == "options":
            if not self.current_command:
                print(self.fail + "No command selected")
                return
            
        else:
            print(self.fail + "Unknown command " +'"' + command + '"')

    def show_options(self):
        if self.current_command:
            if self.current_command in ServerCommands.SList:
                print(self.SettingsTable.display())
            else:
                print(self.fail + "No options for " + self.current_command)
        else:
            print(self.fail + "No command selected")
            


if __name__ == "__main__":

    Banner = colored('''┏┓┳┓┏┓┏┓┓┏┓┏┓┏┳┓┏┓┏┳┓┳┏┓┳┓''', 'green') + '''\n'''
    Banner += colored('''┃ ┣┫┣┫┃ ┃┫ ┗┓ ┃ ┣┫ ┃ ┃┃┃┃┃''', 'light_green') + '''\n'''
    Banner += colored('''┗┛┛┗┛┗┗┛┛┗┛┗┛ ┻ ┛┗ ┻ ┻┗┛┛┗''', 'white') + '''\n'''
    Banner += colored('''SUNY SOC              v1.0''', 'white') + '''\n'''
    style = Style.from_dict({
    'prompt': '#ff6b6b',  # Using an RGB value for custom color
})
    current_command = CrackStation.current_command
    server_commands = ServerCommands()
   
    username = server_commands.SList["settings"]["Options"]["Username"]
 
    CrackStation = CrackStation()
    print(Banner)
    session = PromptSession(history=InMemoryHistory())
    try:
        while True:
            if CrackStation.current_command:
               
                prompt_text = HTML('<ansiblue>{username}</ansiblue><ansiwhite>@{ip}></ansiwhite> <ansiwhite>[</ansiwhite><ansired>{command}</ansired><ansiwhite>] > </ansiwhite>'.format(username=username, ip=server_commands.SList["settings"]["Options"]["Server_IP"], command=CrackStation.current_command))
            else:
                prompt_text = HTML('<ansiblue>{username}</ansiblue><ansiwhite>@{ip}></ansiwhite> '.format(username=username, ip=server_commands.SList["settings"]["Options"]["Server_IP"]))
            # Use prompt_toolkit's session to read input with support for history
            
            user_input = session.prompt(prompt_text)
            CrackStation.input_handler(user_input)
    except KeyboardInterrupt:
        print(CrackStation.fail + "Exiting CrackStation CLI...")
