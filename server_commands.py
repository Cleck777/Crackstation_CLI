
import os

class ServerCommands:
    SList = {
        "settings": {
            "Description": "Server settings",
            "Options": {
                "Username": "",
                "Server_IP": "",
                "Server_Port": "443",
    
    
                }
                
            },
        "help": {
            "Description": "Display help menu"},

        "exit": {
            "Description": "Exit the program"},
        "back": {
            "Description": "Return to the previous command"},
        

        "crack": {
            "Description": "Queue a hash",
            "Options": {
                "Hash_Location": "",
                "Wordlist": "",
                "Hash_Type": ""
            }
        },  
    }
    def __init__(self):
        
        if ServerCommands.SList["settings"]["Options"]["Username"] == "":
            try:
                ServerCommands.SList["settings"]["Options"]["Username"] = os.getlogin()
            except:
                ServerCommands.SList["settings"]["Options"]["Username"] = ""
        if ServerCommands.SList["settings"]["Options"]["Server_IP"] == "":
            ServerCommands.SList["settings"]["Options"]["Server_IP"] = "localhost"


    
   
