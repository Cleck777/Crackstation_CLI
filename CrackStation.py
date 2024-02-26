from typing import Callable, Dict, Optional
#from CommandFactory import CommandFactory
from prompt_toolkit import PromptSession
import random
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.styles import Style
from prompt_toolkit import print_formatted_text, HTML, ANSI
from server_commands import ServerCommands 
from termcolor import colored
from HelpTable import HelpTable
from OptionsTable import OptionsTable
from Farwells import farewells
import os

class CrackStation:
    current_command = ""
    success = colored('[+] ', 'green')
    fail = colored('[-] ', 'red')
    server_commands = ServerCommands()
    
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
            print(self.success +  random.choice(farewells))
            exit()
        elif command == "help":
            self.server_commands.HelperTable.display()
            self.server_commands.AdvancedTable.display()
        elif command == "settings":
            self.current_command = "settings"
        elif command == "crack":
            self.current_command = "crack"
        elif command == "back":
            self.current_command = None
        elif command == "show":
            if not args:
                print(self.fail + "Please state what you would like to show")
                return
            if args == "options" and self.current_command:
                self.show_options()
            else: 
                print(self.fail + "No command selected")
            
        else:
            print(self.fail + "Unknown command " +'"' + command + '"')

    def show_options(self):
        print(self.success + self.current_command)
        if not self.current_command or self.current_command not in self.server_commands.SList:
            print(self.fail + "No command selected or no options available for the current command.")
            return
        table = self.server_commands.SList[self.current_command]["Table"]
        table.display()
            


if __name__ == "__main__":

    Banner = colored('''┏┓┳┓┏┓┏┓┓┏┓┏┓┏┳┓┏┓┏┳┓┳┏┓┳┓''', 'green') + '''\n'''
    Banner += colored('''┃ ┣┫┣┫┃ ┃┫ ┗┓ ┃ ┣┫ ┃ ┃┃┃┃┃''', 'light_green') + '''\n'''
    Banner += colored('''┗┛┛┗┛┗┗┛┛┗┛┗┛ ┻ ┛┗ ┻ ┻┗┛┛┗''', 'white') + '''\n'''
    Banner += colored('''SUNY SOC              v1.0''', 'white') + '''\n'''
    style = Style.from_dict({
    'prompt': '#ff6b6b',  # Using an RGB value for custom color
})
    current_command = CrackStation.current_command
    server_commands = CrackStation.server_commands
   
    username = server_commands.SList["settings"]["Options"]["Username"]["Value"]
 
    CrackStation = CrackStation()
    print(Banner)
    session = PromptSession(history=InMemoryHistory())
    try:
        while True:
            if CrackStation.current_command:
               
                prompt_text = HTML('<ansiblue>{username}</ansiblue><ansiwhite>@{ip}></ansiwhite> <ansiwhite>[</ansiwhite><ansired>{command}</ansired><ansiwhite>] > </ansiwhite>'.format(username=username, ip=server_commands.SList["settings"]["Options"]["Server_IP"]["Value"], command=CrackStation.current_command))
            else:
                prompt_text = HTML('<ansiblue>{username}</ansiblue><ansiwhite>@{ip}></ansiwhite> '.format(username=username, ip=server_commands.SList["settings"]["Options"]["Server_IP"]["Value"]))
            # Use prompt_toolkit's session to read input with support for history
            
            user_input = session.prompt(prompt_text)
            CrackStation.input_handler(user_input)
    except KeyboardInterrupt:
        print(CrackStation.success + random.choice(farewells))
        exit()
