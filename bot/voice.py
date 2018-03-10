"""
    description: Contains class for making a music playing bot
    file: voice.py

    author: Ellis Wright
    language: python3.6
"""
import asyncio
import discord
from discord.ext import commands
from voice import *

class VoicePlayer:
    def __init__(self, bot, channel):
        self.bot = bot
        self.voice_channel = channel
        self.players = asyncio.Queue()
        self.current = None
        self.play_song = asyncio.Event()
        self.player = self.bot.loop.create_task(self.player_task())

    def set_voice_state(self, state):
        self.voice_channel = state

    def skip(self):
        if self.current != None:
            self.current.stop()


    async def add_song(self, song):
        await self.players.put(await self.voice_channel.create_ytdl_player(song))

    async def player_task(self):
        while True:
            self.play_song.clear()
            self.current = await self.players.get()
            self.current.start()
            await self.play_song.wait()
