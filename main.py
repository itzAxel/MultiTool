from subprocess import call
from ctypes import windll
import os
import shutil
os.system("")   # Init color



class Command:
    sfc = "sfc /scannow"
    dism = "DISM /Online /Cleanup-Image /RestoreHealth"
    reload = "shutdown /r"
    ato = "slmgr /ato"

class Servers:
    kms1 = ""  # Add your own KMS servers
    kms2 = ""


class Keys_Win10:
    home = "TX9XD-98N7V-6WMQ6-BX7FG-H8Q99"
    home_sl = "7HNRX-D7KGG-3K4RQ-4WPJ4-YTDFH"
    pro = "W269N-WFGWX-YVC9B-4J6C9-T83GX"
    enterprise = "ND4DX-39KJY-FYWQ9-X6XKT-VCFCF"
    core = "KTNPV-KTRK4-3RRR8-39X6W-W44T3"


class keys_win11:
    home = "YTMG3-N6DKC-DKB77-7M9GH-8HVX7"
    home_sl = "BT79Q-G7N6G-PGBYW-4YWX6-6F4BT"
    pro = "W269N-WFGWX-YVC9B-4J6C9-T83GX"
    corp = "XGVPP-NMH47-7TTHJ-W3FW7-8HV2C"


class Color:    # Color codes
    PURPLE = '\033[35m'
    OK = '\033[32m'     # Green
    CYAN = '\033[96m'
    RED = '\033[31m'
    WARN = '\033[33m'   # Yellow


def is_admin():
    try:
        return os.getuid() == 0
    except AttributeError:
        return windll.shell32.IsUserAnAdmin() != 0


def shell(comm, shell_type):
    if shell_type:
        print(f"{Color.RED}[!] WARNING: {Color.WARN}DO NOT OFF PC OR CLOSE THIS WINDOW!")
    try:
        return call(comm, shell=True)
    except Exception as e:
        return f"{Color.RED}ERROR!:{Color.WARN}{e}"


def activate_system(version):
    if version == "10":
        print(
            f"{Color.CYAN}For example 'home' , 'pro' , 'home_sl' , 'enterprise' or 'corporative', {Color.WARN}LTSC NOT supported"
        )
    else:
        print(
            f"{Color.CYAN}For example 'home' , 'home_sl' , 'pro' or  'enterprise', {Color.WARN}Education NOT supported"
        )
    while True:
        ver = input(f"{Color.PURPLE}Please , Enter your windows redaction:")
        if ver.startswith("p") or ver.startswith("P"):
            if version == "10":
                key = Keys_Win10.pro
            else:
                key = keys_win11.pro
            break
        elif ver.startswith("h") or ver.startswith("H"):
            if version == "10":
                key = Keys_Win10.home
            else:
                key = keys_win11.home
            break
        elif ver == "home_sl" or ver == "Home_Sl":
            if version == "10":
                key = Keys_Win10.home_sl
            else:
                key = keys_win11.home_sl
            print("Undefined version! Try Again")
            break

        elif ver.startswith("e") or ver.startswith("E"):
            if version == "10":
                key = Keys_Win10.enterprise
            else:
                key = keys_win11.corp
            break
        elif ver.startswith("c") or ver.startswith("C"):
            if version == "10":
                key = Keys_Win10.core
                break
            else:
                print("Undefined version! Try Again")

        else:
            print("Undefined version! Try Again")

    print(f"{Color.OK}OK!")
    print(f"{Color.WARN} Please close dialog windows")
    print(f"{Color.PURPLE}Key:{key}")
    shell(f"slmgr /ipk {key}", False)
    print(f"{Color.PURPLE}Activation server:{Color.WARN}{Servers.kms1}")
    shell(f"slmgr /skms {Servers.kms1}", False)
    print(f"{Color.PURPLE}Trying to activate...")
    shell(Command.ato, False)
    print(f'{Color.OK}Activation procedure complete!')


def activate():
    while True:
        print(
            f"{Color.PURPLE}Please enter your windows version, For Example: 10 or 11 (Type only NUMBERS), {Color.WARN}Warning:8.1 , 8 and etc NOT supported "
        )
        version = input(f"{Color.PURPLE}Windows version:")
        if version == "10" or version == "11":
            activate_system(version)
            break
        else:
            print(f"Please , {Color.WARN}enter NUMBER!")

def clear_folder(directory_path):
    # Get a list of all files and subdirectories in the directory
    contents = os.listdir(directory_path)
    for item in contents:
        item_path = os.path.join(directory_path, item)
        try:
            if os.path.isfile(item_path):
                os.remove(item_path)

            elif os.path.isdir(item_path):
                shutil.rmtree(item_path)

            else:
                print(f"{Color.WARN}Skipped: {item_path} (Not a file or directory)")
        except Exception as e:
            print(f"{Color.RED}Error occurred while deleting {item_path}:{Color.WARN} {e}")
def clear():
    temp_folder = fr'C:\Users\{os.getlogin()}\AppData\Local\Temp'
    print(f"{Color.PURPLE}Directory:{temp_folder}")
    clear_folder(temp_folder)
    print(f"{Color.PURPLE}Procedure Complete")


def help():
    print(f"""
{Color.PURPLE}Usage:
    {Color.PURPLE}-dism (or dism): {Color.OK}Recovery with DISM (Embedded in SYS) utility (Very Effective , Reload Required , Time:{Color.RED}Long{Color.OK})
    {Color.PURPLE}-sfc (or sfc):{Color.OK} Recovery with SFC (Embedded in SYS) (Effective , Reload required , Time:{Color.WARN}Medium{Color.OK})
    {Color.PURPLE}-activate (or activate):{Color.OK} Activate your OS with KMS server (Windows 10 Pro,Home,Home single language) 
    {Color.PURPLE}-help (or help):{Color.OK} Print this menu
    {Color.PURPLE}-clear (or clear):{Color.OK} Clear %TEMP% Folder ({Color.WARN}Please, be careful while using this command!{Color.OK})
    """)


if not is_admin():
    print(f"{Color.RED}[!]ERROR: {Color.WARN}Program launched without admin permissions")
    input(f"{Color.WARN}Press ENTER to exit...")
    exit()

print(f"{Color.OK}Successful Start!")
help()
while True:
    com = input(f"{Color.PURPLE}Enter command:")
    if com.startswith("-d") or com.startswith("d"):
        shell(Command.dism, True)
        continue
    if com.startswith("-s") or com.startswith("s"):
        shell(Command.sfc, True)
        continue
    if com.startswith("-h") or com.startswith("h"):
        help()
        continue
    if com.startswith("-a") or com.startswith("a"):
        activate()
        continue
    if com.startswith("-c") or com.startswith("c"):
        clear()
        continue
    else:
        print(f"{Color.RED}[!]ERROR:{Color.WARN} Undefined command!")
