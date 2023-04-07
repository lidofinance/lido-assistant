import os
from collections import defaultdict

import discord

from dotenv import load_dotenv
from src.chat_model import chat

load_dotenv()


class DiscordReader(discord.Client):
    chats: dict

    def __init__(self, channels, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.channels = channels

    async def on_ready(self):
        self.chats = defaultdict(chat)
        print('Logged on as', self.user)

    async def on_message(self, message: discord.Message):
        if message.author == self.user:
            return
        if message.author.bot is True:
            return
        if message.channel.name not in self.channels:
            return

        if self.user in message.mentions or (message.reference and message.reference.resolved.author == self.user):
            name = message.author.name + "#" + message.author.discriminator
            answer = self.chats[name](message.content).get("answer", "I don't know")
            await message.reply(answer)


def run():
    intents = discord.Intents.default()
    intents.message_content = True
    token = os.getenv("DISCORD_BOT_TOKEN")
    channels = os.getenv("DISCORD_CHANNELS").split(",")

    client = DiscordReader(channels=channels, intents=intents)

    client.run(token)
