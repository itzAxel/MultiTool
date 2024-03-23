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
from cryptography.fernet import Fernet
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
    {Color.PURPLE}-crypt (or crypt):{Color.OK} Encrypt/Decrypt file or string and save key in file
    {Color.PURPLE}-about (or about):{Color.OK} About this program
    """)

def about() -> None:
    print(f"""
{Color.PURPLE}About:
    {Color.PURPLE}MultiTool, version: 1.2.1 {Color.OK}Stable 
    {Color.PURPLE}Author, main creator: ItzAxel, Special Thanks for: NikSne
    {Color.PURPLE}Project on GitHub: https://github.com/itzAxel/MultiTool
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


class Command:
    sfc = "sfc /scannow"
    dism = "DISM /Online /Cleanup-Image /RestoreHealth"
    restart = "shutdown /r"
    ato = "slmgr /ato"

while True:
    match input(f"{Color.PURPLE}Enter command:").lower()[:3]:
        case "-di":
            shell(Command.dism, True)

        case "-sf":
            shell(Command.sfc, True)

        case "-ac":
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

        case "-he":
            help()

        case "-cl":
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

        case "-cr":
            print(f"""
{Color.PURPLE}Please select operation:
    1-Decrypt
    2-Encrypt
            """)
            op = input("Operation (Number):")
            print("""
Please select type of data:
    1-File
    2-Text
            """)
            type = input("Type (Number):")
            if op=="2":
                if input("Use existing key?(y/n)")=="y":
                    name=input("Please enter .key file name (Only name):")
                    key = open(f"{name}.key", "rb").read()
                    f = Fernet(key)
                else:
                    name = input("Please enter .key file name (Only name):")
                    print("Generating key...")
                    key = Fernet.generate_key()
                    f = Fernet(key)
                    with open(f"{name}.key", "wb") as key_file:
                        key_file.write(key)
                    print(f"{Color.OK}Encrypt Key Successfully generated and saved as file '{name}.key' ")

                if type=="1":
                    file_name = input(f"{Color.PURPLE}Please enter file name (format: file.txt):")
                    try:
                        with open(file_name, "rb") as file:
                            file_data = file.read()
                        encrypted_data = f.encrypt(file_data)
                        with open(file_name, "wb") as file:
                            file.write(encrypted_data)
                        print(f"{Color.OK}File Successfully Encrypted")
                    except Exception as e:
                        print(f'{Color.RED}[!]ERROR: {Color.WARN}{e}')
                        continue
                if type=="2":
                    text = input(f"{Color.PURPLE}Please enter string to encrypt:").encode()
                    enc_file_name = input(f"{Color.PURPLE}Please enter file name where will be saved text:")
                    try:
                        encrypted_data = f.encrypt(text)
                        with open(f"{enc_file_name}.txt", "wb") as file:
                            file.write(encrypted_data)
                        print(f"{Color.OK}Text Successfully Encrypted")
                    except Exception as e:
                        print(f'{Color.RED}[!]ERROR: {Color.WARN}{e}')
                        continue

            if op=="1":
                name=input("Please enter .key file name (Only name):")
                print("Importing key...")
                try:
                    key = open(f"{name}.key", "rb").read()
                    f = Fernet(key)
                except Exception as e:
                    print(f'{Color.RED}[!]ERROR: {Color.WARN}{e}')
                    continue
                print(f"{Color.OK}Decrypt Key Successfully imported ")

                if type=="1":
                    file_name = input(f"{Color.PURPLE}Please enter file name (format: file.txt):")
                    try:
                        with open(file_name, "rb") as file:
                            file_data = file.read()
                        decrypted_data = f.decrypt(file_data)
                        with open(file_name, "wb") as file:
                            file.write(decrypted_data)
                        print(f"{Color.OK}File Successfully Decrypted")
                    except Exception as e:
                        print(f'{Color.RED}[!]ERROR: {Color.WARN}{e}')
                        continue
                if type=="2":
                    text = input(f"{Color.PURPLE}Please enter string to decrypt:")
                    enc_file_name = input(f"{Color.PURPLE}Please enter file name where will be saved text:")
                    try:
                        decrypted_data = f.decrypt(text)
                        with open(f"{enc_file_name}.txt", "w") as file:
                            file.write(decrypted_data.decode())
                        print(f"{Color.OK}Text Successfully Decrypted")
                        print(f"{Color.PURPLE}Decrypted text:{decrypted_data}")
                    except Exception as e:
                        print(f'{Color.RED}[!]ERROR: {Color.WARN}{e}')
                        continue

        case "-ab":
            about()

        case _:
            print(f"{Color.RED}[!]ERROR: {Color.WARN}Undefined command!")