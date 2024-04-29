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
from APIHandler import APIHandler
from Farwells import farewells
from halo import Halo
import os
import getpass
import json

class CrackStation:
    current_command = ""
    success = colored('[+] ', 'green')
    fail = colored('[-] ', 'red')
    
    server_commands = ServerCommands()
    
    def __init__(self) -> None:
        pass
    
    def input_handler(self, user_input: str) -> None:
        parts = user_input.split(maxsplit=1)
        if len(parts) < 1:  # Add this check
            print(self.fail + "Invalid command")
            return
        
        command = parts[0]
        spinner = Halo(text="Requesting for " + command, spinner='dots')
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
        elif command == "set":
            if not args:
                print(self.fail + "Please state what you would like to set")
                return
            if self.current_command:
                option, value = args.split(maxsplit=1)
                self.set_option(option, value)
            else:
                print(self.fail + "No command selected")
        elif command == "log":
            spinner.start()
            error = APIHandler.option_operations()
            spinner.stop()
            print(self.fail + error)
        elif command == "login":
            print("")
            username = server_commands.SList["settings"]["Options"]["Username"]["Value"]

            password = getpass.getpass("Enter password for " + username + ": ")
            username = server_commands.SList["settings"]["Options"]["Username"]["Value"]
            credentials = json.dumps({"user": username, "password": password})

            spinner.start()
            error = APIHandler.authentication_operations("login", credentials)
            spinner.stop()
            print(self.fail + error)
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
    def set_option(self, option: str, value: str) -> None:
    
        if self.current_command:
            if option in ServerCommands.SList[self.current_command]["Options"] and value:
                ServerCommands.SList[self.current_command]["Options"][option]["Value"] = value
                ServerCommands.SList[self.current_command]["Table"].modify_row(ServerCommands.SList[self.current_command]["Options"][option]["Location"] , value)
                print(self.success + "Set " + option + " to " + value)
            else:
                print(self.fail + "Option not found")
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
    server_commands = CrackStation.server_commands
   
    username = server_commands.SList["settings"]["Options"]["Username"]["Value"]
 
    CrackStation = CrackStation()
    APIHandler = APIHandler()
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
