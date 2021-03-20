import asyncio
from pyrogram import Client,filters
from credentials import bot_token, bot_user_name,API_HASH,APP_ID,TOOLSDIR,WDIR
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
import requests
import os

app = Client(
    "MegaDown",
    bot_token=bot_token,
    api_id=APP_ID,
    api_hash=API_HASH,

)


comm="{} dl  --path {} ".format(TOOLSDIR,WDIR)

from subprocess import Popen, PIPE

def run(command):
    process = Popen(command, stdout=PIPE, shell=True)
    while True:
        line = process.stdout.readline().rstrip()
        if not line:
            break
        yield line


def progress(current, total):
    print(f"{current * 100 / total:.1f}%")



@app.on_message(filters.command(["start"]))
def start(client, message):
    client.send_message(chat_id=message.chat.id,
                        text="Hi")


@app.on_message(filters.text)
def handleText(client,message):
    tempcomm=comm+message.text
    print(tempcomm)
    x = client.send_message(chat_id=message.chat.id,
                            text="Starting...")
    for path in run(tempcomm):

        client.edit_message_text(chat_id=message.chat.id, message_id=x.message_id, text=path)

    arr = os.listdir(WDIR)
    client.send_message(chat_id=message.chat.id,
                        text="Uploading...")
    for doc in arr:

        app.send_document(chat_id=message.chat.id, document=WDIR+"/"+doc, progress=progress)
        os.remove(WDIR+"/"+doc)

    client.send_message(chat_id=message.chat.id,
                        text="Finished")

if __name__ == "__main__":

    app.run()
    



