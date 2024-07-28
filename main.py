import os
from datetime import datetime
import requests
from colorama import Fore, init, Style
import sys
import fade
import whois
from rootchecker import rootchecker # yayyy this is my pacakge
import phonenumbers
from phonenumbers import geocoder, carrier, timezone





init(autoreset=True)

is_termux = rootchecker.check_root()["running_on_termux"]
version = "0.0.3"
default_input_text = f"{Fore.RED}{Style.BRIGHT}delta{Fore.BLUE}@python{sys.version_info[0]}.{sys.version_info[1]}.{sys.version_info[2]} {Style.RESET_ALL}$ "
sigint = "\nReceived keyboard interrupt, exiting."
version_fetch_url = "https://raw.githubusercontent.com/yakupaslantas/delta/main/etc/version.txt"
enter_to_return = " Press [ ENTER ] key to return"




art = """

    ████████▄     ▄████████  ▄█           ███        ▄████████      
    ███   ▀███   ███    ███ ███       ▀█████████▄   ███    ███      
    ███    ███   ███    █▀  ███          ▀███▀▀██   ███    ███      
    ███    ███  ▄███▄▄▄     ███           ███   ▀   ███    ███      
    ███    ███ ▀▀███▀▀▀     ███           ███     ▀███████████      
    ███    ███   ███    █▄  ███           ███       ███    ███      
    ███   ▄███   ███    ███ ███▌    ▄     ███       ███    ███      
    ████████▀    ██████████ █████▄▄██    ▄████▀     ███    █▀       
                        ▀                                    
                    [github.com/yakupaslantas]
"""

if is_termux == True:
    art = """
    
    
    ·▄▄▄▄  ▄▄▄ .▄▄▌  ▄▄▄▄▄ ▄▄▄· 
    ██▪ ██ ▀▄.▀·██•  •██  ▐█ ▀█ 
    ▐█· ▐█▌▐▀▀▪▄██▪   ▐█.▪▄█▀▀█ 
    ██. ██ ▐█▄▄▌▐█▌▐▌ ▐█▌·▐█ ▪▐▌
    ▀▀▀▀▀•  ▀▀▀ .▀▀▀  ▀▀▀  ▀  ▀ 
    """


def check_for_net_connection():
    try:
        requests.post("https://google.com/")
    except:
        print("Unstable network connection, please try again later.")
        sys.exit()



def generate_new_session():
    try:
        os.mkdir("./session")
    except FileExistsError:
        pass
    path = f"./session/{datetime.now().strftime('%Y%m%d%H%M%S')}/"
    os.mkdir(path)
    os.mkdir(path+"phonenumberosint")
    os.mkdir(path+"iposint")
    os.mkdir(path+"whoisosint")
    return path


def clear():
    if os.name == "nt":
        os.system("cls")
    else:
        os.system("clear")



main_menu_choices = """

    0|  EXIT
    c|  CHANGELOG
    
    1|  IP OSINT
    2|  Website OSINT
    3|  Phone Number OSINT
"""


changelog = f"""
What's new in {version}

- Added new osint option : phone numbers
- Fixed two bugs that causing a exception when user try to save result of query in website osint result menu
- Fixed four bugs that causing - Please type a valid option - to trigger even when its not needed
- Added new feature : changelog screen
- KeyboardInterrupt exception handler now buffers a new line before printing out - sigint - 
"""



def changelog_menu(update):
    clear()
    print(changelog)
    try:
        input(enter_to_return)
        main(update)
    except KeyboardInterrupt:
        print(sigint)
        sys.exit()



def phonenumber_osint(error=False):
    clear()
    if error == True:
        print("PLease enter a valid phone number!")
    if error == "invalid_country_number":
        print("Please enter country code!")
    try:
        phone_number = input("Enter phone number :")
    except KeyboardInterrupt:
        print(sigint)
        sys.exit()
    if len(phone_number) < 5:
        phonenumber_osint(error=True)
        return
    try:
        parsed_number = phonenumbers.parse(phone_number)
    except:
        phonenumber_osint(error="invalid_country_number")
        return
    region = geocoder.description_for_number(parsed_number, "en")
    number_timezone = timezone.time_zones_for_number(parsed_number)
    carrier_name = carrier.name_for_number(parsed_number, 'en')
    stylized_data = f"""
    Country          : {region}
    Timezone        : {number_timezone}
    Carrier Name    : {carrier_name} 
    """
    print(stylized_data)
    print("""
    0|  BACK

    1|  Save
    2|  New Query
            """)
    while True:
        try:
            choice = input(default_input_text)
        except KeyboardInterrupt:
            print(sigint)
            sys.exit()
        if choice == "0":
            main()
        if choice == "1":
            with open(path+"phonenumberosint/" + phone_number + ".txt", "w") as file:
                file.write(stylized_data)
            print(f"Saved in {path}/phonenumberosint/{phone_number}.txt\n")
            continue
        if choice == "2":
            phonenumber_osint()
            break
        print("Please type a valid option. \n")



    



def ip_osint_generate_table(data):
    stylized_data = f"""
    IP Adress           : {data["ip"]}
    Network IP Adress   : {data["network"]}
    IP Version          : {data["version"]}
    IP Organization     : {data["org"]}
    
    Latitude            : {data["latitude"]}
    Longitude           : {data["longitude"]}
    
    Country             : {data["country_name"]}
    City                : {data["city"]}
    Postal code         : {data["postal"]}
    Region              : {data["region"]}
    Region Code         : {data["region_code"]}
    
    Country Name        : {data["country_name"]}
    Country Code        : {data["country_code"]}
    Country ISO3 Code   : {data["country_code_iso3"]}
    Capital Of Country  : {data["country_capital"]}
    Country Timezone    : {data["timezone"]}
    Country UTC Code    : {data["utc_offset"]}
    Country Call Code   : {data["country_calling_code"]}
    Country Currency    : {data["currency"]}
    Country KM Area     : {data["country_area"]}
    Country Population  : {data["country_population"]}
    """
    return stylized_data


def ip_osint(error = False):
    clear()
    if error == True:
        print("Please enter a valid IP adress!\n")
    try:
        ip_adress = input("Type IP adress: ")
    except KeyboardInterrupt:
        print(sigint)
        sys.exit()
    clear()
    ip_adress_info = get_information_of_ip_adress(ip_adress)
    if ip_adress_info == 1:
        ip_osint(error=True)
    print(ip_osint_generate_table(ip_adress_info))
    print("""
    0|  BACK
    
    1|  Save
    2|  Save (raw json data)
    3|  New Query
    """)
    while True:
        try:
            choice = input(default_input_text)
        except KeyboardInterrupt:
            print(sigint)
            sys.exit()
        if choice == "0":
            main()
            break
        if choice == "1":
            with open(path + "iposint/" + ip_adress + ".txt", "w") as file:
                file.write(ip_osint_generate_table(ip_adress_info))
            print(f"Saved in {path}/iposint/{ip_adress}.txt\n")
            continue
        if choice == "2":
            with open(path + "iposint/" + ip_adress + "__RAW.txt", "w") as file:
                file.write(str(ip_adress_info))
            print(f"Saved in {path}/iposint/{ip_adress}.__RAWtxt\n")
            continue
        if choice == "3":
            ip_osint()
            break
        print("Please type a valid option. \n")






def get_information_of_ip_adress(ip_adress):
    ip_information = requests.get(f'https://ipapi.co/{ip_adress}/json/').json()
    try:
        if ip_information["error"]:
            return 1
    except:
        pass
    return ip_information




def whois_osint_generate_table(data):
    stylized_data = f"""
    Domain          : {data.domain}
    Registrar       : {data.registrar}
    Creation Date   : {data.creation_date}
    Expiration Date : {data.expiration_date}
    Name Server     : {data.name_servers}
    Whois Server    : {data.whois_server}
    Updated Date    : {data.updated_date}
    """
    return stylized_data


def whois_osint(error = False):
    clear()
    if error == True:
        print("Enter a valid web adress.\n")
    try:
        web_adress = input("Type web adress: ")
    except KeyboardInterrupt:
        print(sigint)
        sys.exit()
    web_adress_data = whois_lookup(web_adress)
    if web_adress_data == 1:
        whois_osint(error=True)
    print(whois_osint_generate_table(web_adress_data))
    print("""
    0|  BACK
    
    1|  Save
    2|  Save (raw json data)
    3|  New Query
    """)
    while True:
        try:
            choice = input(default_input_text)
        except KeyboardInterrupt:
            print(sigint)
            sys.exit()
        if choice == "0":
            main()
            break
        if choice == "1":
            with open(path+"whoisosint/" + web_adress + ".txt", "w") as file:
                file.write(whois_osint_generate_table(web_adress_data))
            print(f"Saved in {path}/whoisosint/{web_adress}.txt\n")
            continue
        if choice == "2":
            with open(path+"whoisosint/" + web_adress + "__RAW.txt", "w") as file:
                file.write(web_adress_data)
            print(f"Saved in {path}/whoisosint/{web_adress}__RAW.txt\n")
            continue
        if choice == "3":
            whois_osint()
        print("Please type a valid option.\n")


def whois_lookup(web_adress):
    try:
        data = whois.whois(web_adress)
    except whois.parser.PywhoisError:
        return 1
    return data



def version_descriptor(v):
    return v.split(".")


def check_for_update():
    cloud_version = requests.get(version_fetch_url)
    cloud_version = cloud_version.text.splitlines()[0]
    xcloud_version = version_descriptor(cloud_version)
    current_version = version_descriptor(version)
    xcloud_version = list(map(int, xcloud_version))
    current_version = list(map(int, current_version))
    if xcloud_version[0] > current_version[0]:
        return cloud_version
    if xcloud_version[0] == current_version[0]:
        if xcloud_version[1] == current_version[1]:
            if xcloud_version[2] > current_version[2]:
                return cloud_version
        if xcloud_version[1] > current_version[1]:
            return cloud_version
    return 0



def set_title():
    title = f" Delta {version}"
    if os.name == "nt":
        os.system(f"title {title}")

def print_center(text):
    column, row = os.get_terminal_size()
    print(text.center(column))





def main(update_available = False):
    clear()
    print(fade.purpleblue(art))
    if update_available != False:
        print(f"{Style.BRIGHT}{Fore.CYAN}         [ ! ] Update available : {Fore.RED} {version} -> {update_available}")
    print(main_menu_choices)
    while True:
        try:
            choice = input(default_input_text)
        except KeyboardInterrupt:
            print(sigint)
            sys.exit()
        if choice == "0":
            sys.exit()
        if choice == "c":
            changelog_menu(update_available)
            return
        if choice == "1":
            ip_osint()
            break
        if choice == "2":
            whois_osint()
            break
        if choice == "3":
            clear()
            phonenumber_osint()
            break
        print("Please type a valid option.")


if __name__ == '__main__':
    check_for_net_connection()
    set_title()
    clear()
    update_status = check_for_update()
    if update_status != 0:
        update_available = update_status
    else:
        update_available = False
    path = generate_new_session()
    main(update_available)
