from typing import Callable, Dict, Optional
#from CommandFactory import CommandFactory
from prompt_toolkit import PromptSession
import random
from prompt_toolkit.history import InMemoryHistory
from prompt_toolkit.styles import Style
from prompt_toolkit import print_formatted_text, HTML, ANSI
from termcolor import colored
from HelpTable import HelpTable
from OptionsTable import OptionsTable
from APIHandler import APIHandler
from Farwells import farewells
from halo import Halo
import os
import getpass
import json
import subprocess

class CrackStation:
    current_command = ""
    success = colored('[+] ', 'green')
    info = colored('[*] ', 'blue')
    fail = colored('[-] ', 'red')
    item = colored('[$] ', 'magenta', attrs=['blink'])  
    connected = False
    
    
    spinner = Halo(text="Trying to connect", spinner='dots')
    def __init__(self) -> None:
        
        self.api_handler = APIHandler()
        self.login_user()
    
    def sub_command_handler(self, command: str) -> None:
        if command in self.api_handler.server_commands.SList[self.current_command]["commands"]:
            if command == 'queue':
                result = self.api_handler.queue_operations()
            

        else:
            print(self.fail + "Unknown command")
            self.input_handler(command)

    def login_user(self) -> None:
        username = self.api_handler.server_commands.SList["settings"]["Options"]["Username"]["Value"]

        password = getpass.getpass("Enter password for " + username + ": ")
        username = self.api_handler.server_commands.SList["settings"]["Options"]["Username"]["Value"]
        credentials = {"user": username, "password": password}
        #print(credentials)

        self.spinner.start()
        error = self.api_handler.authentication_operations("login", credentials)
        self.spinner.stop()
        if error == "OK":
            print(self.success + "CONNECTED")
            self.connected = True
        else:
            print(self.fail + error)
            
    
    
    def input_handler(self, user_input: str) -> None:



        parts = user_input.split(maxsplit=1)
        if len(parts) < 1:  # Add this check
            print(self.fail + "Invalid command")
            return
        
        command = parts[0]
        self.spinner = Halo(text="Requesting for " + command, spinner='dots')
        if len(parts) > 1:
            args = parts[1]
        else:
            args = ""

        if command == "exit":
            print(self.success +  random.choice(farewells))
            exit()
        elif command == "help":
            self.api_handler.server_commands.HelperTable.display()
            self.api_handler.server_commands.AdvancedTable.display()
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
            self.spinner.start()
            error = self.api_handler.option_operations()
            self.spinner.stop()
            print(self.fail + error)
        elif command == "login":
            self.login_user()
        elif command == "show":
            if not args:
                print(self.fail + "Please state what you would like to show")
                return
            if args == "options" and self.current_command:
                self.show_options()
            else: 
                print(self.fail + "No command selected")
            
        else:
            try:
                details = self.api_handler.server_commands.SList[self.current_command]["commands"]
            except KeyError:
                print(self.fail + "Unknown server and bash command")
                return
        
            print(details)
            if self.current_command and command in details:
                self.sub_command_handler(command)
            else:
                process = subprocess.run(user_input, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                
                if process.returncode == 0:
                    print(process.stdout)
                else:
                    print(self.fail + "Unknown server and bash command")
            
        

    def show_options(self):
        print(self.success + self.current_command)
        if not self.current_command or self.current_command not in self.api_handler.server_commands.SList:
            print(self.fail + "No command selected or no options available for the current command.")
            return
        table = self.api_handler.server_commands.SList[self.current_command]["Table"]
        table.display()
        print(self.info + "Avaliable commands")
        if self.current_command:
            details = self.api_handler.server_commands.SList[self.current_command]
            if "commands" in details:
                
                for cmd, cmd_details in details["commands"].items():
                    print(" "+ self.item + cmd + " : " + cmd_details['Description'])
        else:
            print(self.fail + "No command selected")
    def set_option(self, option: str, value: str) -> None:
    
        if self.current_command:
            if option in self.api_handler.server_commands.SList[self.current_command]["Options"] and value:
                self.api_handler.server_commands.SList[self.current_command]["Options"][option]["Value"] = value
                self.api_handler.server_commands.SList[self.current_command]["Table"].modify_row(self.api_handler.server_commands.SList[self.current_command]["Options"][option]["Location"] , value)
                print(" "+ self.success + "Set " + option + " to " + value)
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
    
   
    
    print(Banner)
    CrackStation = CrackStation()
    
    
    CrackStation.spinner.start()
   
    CrackStation.spinner.stop()
    
    session = PromptSession(history=InMemoryHistory())
    
    try:
        while True:
            username = CrackStation.api_handler.server_commands.SList["settings"]["Options"]["Username"]["Value"]
            if CrackStation.connected:

                if CrackStation.current_command:
                
                    prompt_text = HTML('<ansiblue>{username}</ansiblue><ansiwhite>@{ip}></ansiwhite> <ansiwhite>[</ansiwhite><ansired>{command}</ansired><ansiwhite>] > </ansiwhite>'.format(username=username, ip=CrackStation.api_handler.server_commands.SList["settings"]["Options"]["Server_IP"]["Value"], command=CrackStation.current_command))
                else:
                    prompt_text = HTML('<ansiblue>{username}</ansiblue><ansiwhite>@{ip}></ansiwhite> '.format(username=username, ip=CrackStation.api_handler.server_commands.SList["settings"]["Options"]["Server_IP"]["Value"]))
            else:

                if CrackStation.current_command:
                
                    prompt_text = HTML('<ansiblue>{username}</ansiblue><ansiwhite>@</ansiwhite><ansired>{ip}</ansired><ansiwhite>></ansiwhite> <ansiwhite>[</ansiwhite><ansired>{command}</ansired><ansiwhite>] > </ansiwhite>'.format(username=username, ip="NOT_CONNECTED", command=CrackStation.current_command))
                else:
                    prompt_text = HTML('<ansiblue>{username}</ansiblue><ansiwhite>@</ansiwhite><ansired>{ip}</ansired><ansiwhite>></ansiwhite> '.format(username=username, ip="NOT_CONNECTED"))

            # Use prompt_toolkit's session to read input with support for history
            
            user_input = session.prompt(prompt_text)
            CrackStation.input_handler(user_input)
    except KeyboardInterrupt:
        print(CrackStation.success + random.choice(farewells))
        CrackStation.api_handler.server_commands.save_settings()
        exit()
