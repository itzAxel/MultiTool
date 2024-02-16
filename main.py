from ctypes import windll
from enum import Enum
import os
from os import system, listdir, remove, getlogin
from os.path import isfile, isdir, join
from shutil import rmtree
from subprocess import call
from requests import get
from json import load
import codecs
from bs4 import BeautifulSoup
system("")  # Init colors


class Color:  # Color codes
    PURPLE = '\033[35m'
    OK = '\033[32m'  # Green
    CYAN = '\033[96m'
    RED = '\033[31m'
    WARN = '\033[33m'  # Yellow


def is_not_admin() -> bool:
    try:
        return bool(os.getuid())
    except AttributeError:
        return not windll.shell32.IsUserAnAdmin()

if is_not_admin():
    print(f"{Color.RED}[!]ERROR: {Color.WARN}Program launched without admin permissions")
    input(f"{Color.WARN}Press ENTER to exit...")
    exit()

def help() -> None:
    print(f"""
{Color.PURPLE}Usage:
    {Color.PURPLE}-dism (or dism): {Color.OK}Recovery with DISM (Embedded in SYS) utility (Very Effective, Reload Required, Time:{Color.RED}Long{Color.OK})
    {Color.PURPLE}-sfc (or sfc):{Color.OK} Recovery with SFC (Embedded in SYS) (Effective, Reload required, Time:{Color.WARN}Medium{Color.OK})
    {Color.PURPLE}-activate (or activate):{Color.OK} Activate your OS with KMS server
    {Color.PURPLE}-help (or help):{Color.OK} Print this menu
    {Color.PURPLE}-clear (or clear):{Color.OK} Clear %TEMP% Folder ({Color.WARN}Please, be careful while using this command!{Color.OK})
    """)



def download(file) -> bool :
    print(f"{Color.OK}Automatic download started")
    try:
        if file:
            file_url = "https://raw.githubusercontent.com/itzAxel/MultiTool/main/keys.json"
            name = "keys"
        else:
            file_url = "https://raw.githubusercontent.com/itzAxel/MultiTool/main/servers.json"
            name = "servers"
        file_data = str(BeautifulSoup(get(file_url).text, "html.parser"))
        file=codecs.open(f"{name}.json","w","utf-8")
        file.write(file_data)
        file.close()
        print(f"{Color.OK}Automatic download complete")
        return True
    except Exception as e:
        print(f'{Color.RED}[!]ERROR: {Color.WARN}{e}')
        return False

if isfile("./keys.json"):
    with open(file="keys.json", encoding="utf-8") as file:
        keys = load(file)
else:
    res = input(f'{Color.RED}[!]ERROR:{Color.WARN}"keys.json" {Color.RED}not{Color.WARN} found, download automatically? (y/n)')
    if res == "y":
      if download(True):
        with open(file="keys.json", encoding="utf-8") as file:
            keys = load(file)
      else:
          print(f"{Color.RED}Error occurred while downloading file")
    else:
          print(f"{Color.RED}WARNING:{Color.WARN}Please don't use activation command")

if not isfile("./servers.json"):
    res = input(f'{Color.RED}[!]ERROR:{Color.WARN}"servers.json" {Color.RED}not{Color.WARN} found, download automatically? (y/n)')
    if res == "y":
        if not download(False):
          print(f"{Color.RED}Error occured while downloading file")
        print(f"{Color.RED}WARNING:{Color.WARN}Please specify the KMS server")
    else:
        print(f"{Color.RED}WARNING:{Color.WARN}Please don't use activation command")

print(f"{Color.OK}Successful Start!")
help()

def shell(comm, shell_type) -> int | str:
    if shell_type:
        print(f"{Color.RED}[!] WARNING: {Color.WARN}DO NOT OFF PC OR CLOSE THIS WINDOW!")
    try:
        return call(comm, shell=True)
    except Exception as e:
        return f"{Color.RED}ERROR!: {Color.WARN}{e}"


class Command(Enum):
    sfc = "sfc /scannow"
    dism = "DISM /Online /Cleanup-Image /RestoreHealth"
    restart = "shutdown /r"
    ato = "slmgr /ato"

while True:
    match input(f"{Color.PURPLE}Enter command:").lower()[:2]:
        case "-d":
            shell(Command.dism, True)

        case "-s":
            shell(Command.sfc, True)

        case "-a":
            print(
                f"{Color.PURPLE}Please, enter your Windows version. Supported versions: "
                f"{''.join(f'Windows {version}, ' for version in keys.keys())}".removesuffix(", ")
            )
            while True:
                version = input(f"{Color.PURPLE}Windows version: ").lower().removeprefix("win").removeprefix("dows ")
                if version in keys.keys():
                    break
                print(f"Please, {Color.WARN}enter SUPPORTED version!")

            print(
                f"{Color.PURPLE}Please, enter your windows redaction. Supported redactions: "
                f"{''.join(f'{redaction}, ' for redaction in keys[version].keys())}".removesuffix(", ")
            )
            while True:
                key = keys[version].get(input(f"{Color.PURPLE}Windows redaction: "), "")
                if key:
                    break
                print("Undefined version! Try Again")

            while True:
                with open (file="servers.json", encoding="utf-8") as file:
                    servers = load(file)
                print(
                    f"{Color.PURPLE}Please, enter your KMS server. Your servers (from servers.json): "
                    f"{''.join(f'{name} ({server}), ' for name, server in servers.items())}".removesuffix(", ")
                )
                kms = servers.get(input(f"{Color.PURPLE}KMS server: "), "")
                if kms:
                    break
                print("Undefined server! Try Again")

            print(
                f"{Color.OK}OK!\n"
                f"{Color.WARN}Please, close dialog windows\n"
                f"{Color.PURPLE}Key: {key}"
            )
            shell(f"slmgr /ipk {key}", False)
            print(f"{Color.PURPLE}Activation server: {Color.WARN}{kms}")
            shell(f"slmgr /skms {kms}", False)
            print(f"{Color.PURPLE}Trying to activate...")
            shell(Command.ato, False)
            print(f'{Color.OK}Activation procedure complete!')

        case "-h":
            help()

        case "-c":
            temp_folder = fr'C:\Users\{getlogin()}\AppData\Local\Temp'
            print(f"{Color.PURPLE}Directory:{temp_folder}")
            contents = listdir(temp_folder)
            for item in contents:
                item_path = join(temp_folder, item)
                try:
                    if isfile(item_path):
                        remove(item_path)
                        continue
                    if isdir(item_path):
                        rmtree(item_path)
                        continue
                    print(f"{Color.WARN}Skipped: {item_path} (Not a file or directory)")
                except Exception as e:
                    print(f"{Color.RED}Error occurred while deleting {item_path}:{Color.WARN} {e}")
            print(f"{Color.PURPLE}Procedure Complete")

        case _:
            print(f"{Color.RED}[!]ERROR: {Color.WARN}Undefined command!")
