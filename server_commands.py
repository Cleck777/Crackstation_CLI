import os
from OptionsTable import OptionsTable
from HelpTable import HelpTable
import json
class ServerCommands:
    AdvancedTable = HelpTable("Advanced Commands", ["Command", "Description"])
    HelperTable = HelpTable("Generic Commands", ["Command", "Description"])
    SettingsTable = OptionsTable("Settings", ["Setting", "Value", "Required", "Description"])
    CrackTable = OptionsTable("Password Cracking", ["Setting", "Value", "Required", "Description"])
    rules = []
    mask = []
    hash_list = ["cc3a0280e4fc1415930899896574e118"]
    ServList = {
        "show": {
            "Description": "Show information",
            "Options": {
                "Options": ""
            }
        },
        "help": {
            "Description": "Display help menu"
        },
        "exit": {
            "Description": "Exit the program"
        },
        "back": {
            "Description": "Return to the previous command"
        },
        "set": {
            "Description": "Set a value"
        },
    }
    SList = {
        "settings": {
            "Description": "Server settings",
            "Options": {
                "Username": {
                    "Value": "",
                    "Required": "Yes",
                    "Description": "Username",
                    "Location": 0
                },
                "Server_IP": {
                    "Value": "",
                    "Required": "Yes",
                    "Description": "Username",
                    "Location": 1
                },
                "Server_Port": {
                    "Value": "",
                    "Required": "Yes",
                    "Description": "Username",
                    "Location": 2
                }
            },
            "Table": SettingsTable,
            "commands": {
                "save": {
                    "Description": "Save settings"
                },
                "load": {
                    "Description": "Load settings"
                }

            }

        },
        "crack": {
            "Description": "Queue a hash",
            "Options": {
                "name": {
                    "Value" : "",
                    "Required": "Yes",
                    "Description": "Name of job",
                    "Location": 0
                },
                "hash_mode": {
                    "Value" : "",
                    "Required": "Yes",
                    "Description": "Number for the hash mode in relation to number described in hashcat",
                    "Location": 1
                },
                "hash_list": {
                    "Value" : ["cc3a0280e4fc1415930899896574e118"],
                    "Required": "Yes",
                    "Description": "Path of the hash list",
                    "Location": 2
                },
                "wordlist": {
                    "Value" : "",
                    "Required": "Yes",
                    "Description": "Path of the Wordlist typically found in /etc/wordlists",
                    "Location": 3
                },
                "wordlist2" : {
                    "Value" : "null",
                    "Required": "No",
                    "Description": "Path of the Wordlist typically found in /etc/wordlists",
                    "Location": 4
                },
                "rules": {
                    "Value" : [],
                    "Required": "No",
                    "Description": "Path of the rules typically found in /etc/rules",
                    "Location": 5
                },
                "attack_mode": {
                    "Value" : "",
                    "Required": "Yes",
                    "Description": "Number for the attack mode in relation to number described in hashcat",
                    "Location": 6
                },
                "mask"  : {
                    "Value" : "null",
                    "Required": "No",
                    "Description": "Mask for the attack",
                    "Location": 7
                },
                "mask_file" : {
                    "Value" : [],
                    "Required": "No",
                    "Description": "Mask file for the attack",
                    "Location": 8
                },
                "notify": {
                    "Value" : "false",
                    "Required": "No",
                    "Description": "Email to notify when job is done",
                    "Location": 9
                },
                "increment": {
                    "Value" : "false",
                    "Required": "No",
                    "Description": "Increment the attack",
                    "Location": 10
                },
                "potcheck": {
                    "Value" : "false",
                    "Required": "No",
                    "Description": "Check the potfile",
                    "Location": 11
                },
                "timeout": {
                    "Value" : "1814400",
                    "Required": "yes",
                    "Description": "Timeout for the job",
                    "Location": 12
                },
           


            },
            "Table": CrackTable,
            "commands": {
                "queue": {
                    "Description": "Queue a hash"
                },
                "status": {
                    "Description": "Check status of a hash"
                },
                "remove": {
                    "Description": "Remove a hash"
                },

        },
        },
        
        "log": {
            "Description": "Show logs"
        },
    }
   


    '''def save_settings(self, filepath='settings.json'):
        
        settings = {}
        for cmd in self.SList:
            if 'Options' in self.SList[cmd]:  # Check if 'Options' key exists
                options = self.SList[cmd]['Options']
                settings[cmd] = {}
                for opt in options:
                    if isinstance(options[opt], dict) and 'Value' in options[opt]:
                        # Ensure it is a dictionary and has a 'Value' key
                        settings[cmd][opt] = options[opt]['Value']
                    else:
                        # Log or handle cases where the expected structure isn't met
                        print(f"Error: Expected a dictionary for options under {cmd}, but got {type(options[opt]).__name__}")
        with open(filepath, 'w') as file:
            json.dump(settings, file, indent=4)
            '''
    
    def save_settings(self, filepath='settings.json'):
        """Save current settings to a JSON file."""
        settings = {}
        for cmd in self.SList:
            if 'Options' in self.SList[cmd]:  # Check if 'Options' key exists
                options = self.SList[cmd]['Options']
                settings[cmd] = {}
                for opt in options:
                    option_value = options[opt]
                    if isinstance(option_value, dict) and 'Value' in option_value:
                        # Option is a dictionary and has a 'Value' key
                        settings[cmd][opt] = option_value['Value']
                    elif isinstance(option_value, (list, str, int, float, bool)):
                        # Directly save the value if it's a simple type
                        settings[cmd][opt] = option_value
                    else:
                        # Log or handle cases where the data type isn't expected
                        print(f"Error: Unexpected data type for option under '{cmd}', option '{opt}': {type(option_value).__name__}")
        with open(filepath, 'w') as file:
            json.dump(settings, file, indent=4)



    
    def load_settings(self, filepath='settings.json'):
        """Load settings from a JSON file."""
        if os.path.exists(filepath):
            with open(filepath, 'r') as file:
                settings = json.load(file)
                for cmd in settings:
                    for opt in settings[cmd]:
                        if opt in self.SList[cmd]['Options']:
                            self.SList[cmd]['Options'][opt]['Value'] = settings[cmd][opt]


    # Update set_option to save settings after change
    def set_option(self, command, option, value):
        """Set an option for a command and save the settings."""
        if command in self.SList and option in self.SList[command]['Options']:
            self.SList[command]['Options'][option]['Value'] = value
            self.SList[command]['Table'].modify_row(self.SList[command]['Options'][option]['Location'], value)
            print(self.success + "Set " + option + " to " + value)
            self.save_settings()  # Save after setting
        else:
            print(self.fail + "Option not found or no command selected")

    def __init__(self):
        # Load settings from file, or establish default if file does not exist
        
        self.load_settings()
        

        # Check if Username and Server_IP are empty and set defaults if necessary
        if ServerCommands.SList["settings"]["Options"]["Username"]["Value"] == "":
            try:
                ServerCommands.SList["settings"]["Options"]["Username"]["Value"] = os.getlogin()
            except:
                ServerCommands.SList["settings"]["Options"]["Username"]["Value"] = "default_user"
            self.save_settings()  # Save if we're setting a default value

        if ServerCommands.SList["settings"]["Options"]["Server_IP"]["Value"] == "":
            ServerCommands.SList["settings"]["Options"]["Server_IP"]["Value"] = "localhost"
            self.save_settings()  # Save if we're setting a default value

        # Populate help tables
        for command in self.ServList:
            ServerCommands.HelperTable.add_row(command, ServerCommands.ServList[command]["Description"])

        for command in self.SList:
            ServerCommands.AdvancedTable.add_row(command, ServerCommands.SList[command]["Description"])

        # Setup or update option tables for commands with options
        for command in ServerCommands.SList:
            if "Options" in self.SList[command]:
                # Check if a table already exists, if not, create one
                if not hasattr(self.SList[command], 'Table') or self.SList[command]['Table'] is None:
                    self.SList[command]['Table'] = OptionsTable(command, ["Option", "Value", "Required", "Description"])
                
                # Update or populate the table
                for option in self.SList[command]['Options']:
                    option_data = self.SList[command]['Options'][option]
                    self.SList[command]['Table'].add_row(option, option_data['Value'], option_data['Required'], option_data['Description'])
"""
    def __init__(self):
        if ServerCommands.SList["settings"]["Options"]["Username"]["Value"] == "":
            try:
                ServerCommands.SList["settings"]["Options"]["Username"]["Value"] = os.getlogin()
            except:
                ServerCommands.SList["settings"]["Options"]["Username"]["Value"] = ""
        if ServerCommands.SList["settings"]["Options"]["Server_IP"]["Value"] == "":
            ServerCommands.SList["settings"]["Options"]["Server_IP"]["Value"] = "localhost"

        for command in self.ServList:
            ServerCommands.HelperTable.add_row(command, ServerCommands.ServList[command]["Description"])
        for command in self.SList:
            ServerCommands.AdvancedTable.add_row(command, ServerCommands.SList[command]["Description"])

        for command in ServerCommands.SList:
            if "Options" in self.SList[command]:
                self.SList[command]["Table"] = OptionsTable(command, ["Option", "Value", "Required", "Description"])
                for option in self.SList[command]["Options"]:
                    option_data = self.SList[command]["Options"][option]
                    self.SList[command]["Table"].add_row(option, option_data["Value"], option_data["Required"], option_data["Description"])                    
"""
