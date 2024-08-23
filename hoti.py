from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, InputMediaDocument, Message
import random
import datetime
import os
import requests
import json
import time

api_id = "22665066"
api_hash = "92dbe89d182f72f427972d8993850130"
bot_token = "7296559290:AAEUMr8iugnSqRbKNlrijTSTMQ2ap_5pXvk"

app = Client("132⌁", api_id=api_id, api_hash=api_hash, bot_token=bot_token)

cache_file = "bin_cache.json"

if os.path.exists(cache_file):
    with open(cache_file, "r") as file:
        bin_cache = json.load(file)
else:
    bin_cache = {}

def save_cache():
    with open(cache_file, "w") as file:
        json.dump(bin_cache, file)

def generate_cards(bin, count, expiry_month=None, expiry_year=None):
    cards = set()
    current_year = datetime.datetime.now().year % 100
    current_month = datetime.datetime.now().month
    while len(cards) < count:
        try:
            card_number = bin + str(random.randint(0, 10**(15-len(bin)-1) - 1)).zfill(15-len(bin))
            if luhn_check(card_number):
                expiry_date = generate_expiry_date(current_year, current_month, expiry_month, expiry_year)
                cvv = str(random.randint(0, 999)).zfill(3)
                card = f"{card_number}|{expiry_date['month']}|{expiry_date['year']}|{cvv}"
                cards.add(card)
        except ValueError:
            continue
    return list(cards)

def generate_expiry_date(current_year, current_month, expiry_month=None, expiry_year=None):
    month = str(expiry_month if expiry_month and expiry_month != 'xx' else random.randint(1, 12)).zfill(2)
    year = str(expiry_year if expiry_year and expiry_year != 'xx' else random.randint(current_year, current_year + 5)).zfill(2)
    if int(year) == current_year and int(month) < current_month:
        month = str(random.randint(current_month, 12)).zfill(2)
    return {"month": month, "year": year}

def luhn_check(number):
    def digits_of(n):
        return [int(d) for d in str(n)]
    digits = digits_of(number)
    odd_digits = digits[-1::-2]
    even_digits = digits[-2::-2]
    checksum = sum(odd_digits)
    for d in even_digits:
        checksum += sum(digits_of(d * 2))
    return checksum % 10 == 0

def get_bin_info(bin):
    if bin in bin_cache:
        return bin_cache[bin]
    
    try:
        response = requests.get(f"https://lookup.binlist.net/{bin[:6]}")
        response.raise_for_status()
        data = response.json()
        info = {
            "scheme": data.get("scheme", "").upper(),
            "type": data.get("type", "").upper(),
            "brand": data.get("brand", "").upper(),
            "bank": data.get("bank", {}).get("name", "").upper(),
            "country": data.get("country", {}).get("name", "").upper(),
            "emoji": data.get("country", {}).get("emoji", "")
        }
        bin_cache[bin] = info
        save_cache()
        return info
    except Exception as e:
        print(f"Error fetching BIN info: {e}")
        return {
            "scheme": "",
            "type": "",
            "brand": "",
            "bank": "",
            "country": "",
            "emoji": ""
        }

@app.on_message(filters.regex(r'^[/.]start'))
def start(client, message):
    help_text = (
    "✦━━━━━━━━━━━━━━━━✦\n"
    "• | - Welcome to the visa file creation bot\n\n"
"• | - To create a visa file, use the following command:-\n\n `/generate 123456 10`\n`/generate 123456xxxx|xx|xx|xxx 30` 🥳\n\n"
"• | - To create visas, use the following command:-\n\n /gen 123456\n"
    "✦━━━━━━━━━━━━━━━━✦\n"
    "Author : @fahimhossen27")

    message.reply_video(
        "https://telegra.ph/file/77e6d04088870b90aca8d.mp4",
        caption=help_text,
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("TEAM X RMBD", url="https://t.me/+VssZW7u2USRhMmNl")]
            ]
        )
    )

@app.on_message(filters.regex(r'^[/.]help'))
def help_command(client, message):
    help_text = ("Using the bot:\n"
                 "To create cards, send:\n"
                 "/generate 123456 10\n"
                 "or:\n"
                 "/generate 456331004775xxxx|xx|xx|xxx 30\n"
                 "I will create a text file named combo.txt containing the generated cards."
                 "If you get any error dm @fagimhossen27")
    message.reply(help_text)

@app.on_message(filters.regex(r'^[/.]generate'))
def generate(client, message: Message):
    try:
        start_time = time.time()
        command_parts = message.text.split()
        bin = command_parts[1].split('|')[0].replace('x', '')
        if '|' in command_parts[1]:
            parts = command_parts[1].split('|')
            expiry_month = parts[1] if parts[1] != 'xx' else None
            expiry_year = parts[2] if parts[2] != 'xx' else None
        else:
            expiry_month, expiry_year = None, None
        
        count = int(command_parts[2]) if len(command_parts) == 3 else 10
        count = min(count, 100000)
        
        if count > 100000:
            message.reply("Maximum number of cards is 100,000.")
            return

        cards = generate_cards(bin, count, expiry_month, expiry_year)
        file_path = "combo.txt"

        with open(file_path, "w") as file:
            file.write("\n".join(cards))

        bin_info = get_bin_info(bin[:6])
        
        user_info = message.from_user
        end_time = time.time()
        elapsed_time = end_time - start_time
        additional_info = (
            f"Bin: {bin[:6]}\n"
            f"Requested: {count}\n"
            f"Time: {elapsed_time:.2f} seconds\n"
            f"Scraped By: [{user_info.first_name}](tg://user?id={user_info.id})\n\n"
            f"𝗜𝗻𝗳𝗼: {bin_info['scheme']} - {bin_info['type']} - {bin_info['brand']}\n"
            f"𝐈𝐬𝐬𝐮𝐞𝐫: {bin_info['bank']}\n"
            f"𝗖𝗼𝘂𝗻𝘁𝗿𝘆: {bin_info['country']} {bin_info['emoji']}"
        )

        message.reply_document(file_path, caption=additional_info, reply_to_message_id=message.id)
    except Exception as e:
        message.reply(f"An error occurred:-\n `{e}`\n\n Message the developer to solve the problem:- @fahimhossen27")

@app.on_message(filters.regex(r'^[/.]gen'))
def gen(client, message: Message):
    try:
        command_parts = message.text.split()
        bin = command_parts[1].split('|')[0].replace('x', '')
        if '|' in command_parts[1]:
            parts = command_parts[1].split('|')
            expiry_month = parts[1] if parts[1] != 'xx' else None
            expiry_year = parts[2] if parts[2] != 'xx' else None
        else:
            expiry_month, expiry_year = None, None
        
        count = int(command_parts[2]) if len(command_parts) == 3 else 10

        cards = generate_cards(bin, count, expiry_month, expiry_year)
        bin_info = get_bin_info(bin[:6])
        
        cards_list = "\n".join([f"`{card}`" for card in cards])
        
        info_text = ("𝗕𝗜𝗡 ⇾ `{bin}`\n"
                     "𝗔𝗺𝗼𝘂𝗻𝘁 ⇾ `{count}`\n\n"
                     "{cards_list}\n\n"
                     "𝗜𝗻𝗳𝗼: {scheme} - {type} - {brand}\n"
                     "𝐈𝐬𝐬𝐮𝐞𝐫: {bank}\n"
                     "𝗖𝗼𝘂𝗻𝘁𝗿𝘆: {country} {emoji}").format(
            bin=bin[:6],
            count=count,
            cards_list=cards_list,
            scheme=bin_info['scheme'] or 'N/A',
            type=bin_info['type'] or 'N/A',
            brand=bin_info['brand'] or 'N/A',
            bank=bin_info['bank'] or 'N/A',
            country=bin_info['country'] or 'N/A',
            emoji=bin_info['emoji'] or ''
        )
        
        message.reply(info_text, reply_to_message_id=message.id)
    except Exception as e:
        message.reply(f"An error occurred:-\n `{e}`\n\n Message the developer to solve the problem:- @fahimhossen27")
        
@app.on_message(filters.regex(r'^[/.]id'))
def user_id(client, message: Message):
    user = message.from_user
    user_info = (
        f"𝖀𝖘𝖊𝖗 𝖎𝖓𝖋𝖔 :\n\n"
        f"𝗡𝗮𝗺𝗲: {user.first_name} {user.last_name or ''}\n"
        f"𝗨𝘀𝗲𝗿𝗻𝗮𝗺𝗲: @{user.username}\n"
        f"𝗨𝘀𝗲𝗿 𝗶𝗗: `{user.id}`\n"
        f"𝗣𝗿𝗼𝗳𝗶𝗹𝗲 𝗹𝗶𝗻𝗸: [𝕮𝖑𝖎𝖈𝖐 𝖍𝖊𝖗𝖊](tg://user?id={user.id})"
    )
    message.reply(user_info)
    
@app.on_message(filters.all)
def handle_all_messages(client, message):
    pass

app.run()
