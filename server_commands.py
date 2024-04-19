import os
from OptionsTable import OptionsTable
from HelpTable import HelpTable
from APIHandler import APIHandler
class ServerCommands:
    AdvancedTable = HelpTable("Advanced Commands", ["Command", "Description"])
    HelperTable = HelpTable("Generic Commands", ["Command", "Description"])
    SettingsTable = OptionsTable("Settings", ["Setting", "Value", "Required", "Description"])
    CrackTable = OptionsTable("Password Cracking", ["Setting", "Value", "Required", "Description"])
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
            "Table": SettingsTable
        },
        "crack": {
            "Description": "Queue a hash",
            "Options": {
                "Hash_Location": {
                    "Value" : "",
                    "Required": "Yes",
                    "Description": "Path of the hashes for cracking",
                    "Location": 0
                },
                "Wordlist": {
                    "Value" : "",
                    "Required": "Yes",
                    "Description": "Path of the Wordlist typically found in /etc/wordlists",
                    "Location": 1
                },
                "Hash_Type":{
                    "Value" : "",
                    "Required": "Yes",
                    "Description": "Number for the hash type in relation to number described in hashcat",
                    "Location": 2
                }
            },
            "Table": CrackTable
        },
        "log": {
            "Description": "Show logs"
        },
    }

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
