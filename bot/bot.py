"""
	file: bot.py
	author: Ellis Wright/Brian Shaw
	language: python 3.6
	description: Bot with few functionalities for discord
"""
#NOTE: DEPENDENCY: python3 discord module
#https://discordapp.com/api/oauth2/authorize?client_id=375689285690589186&scope=bot&permissions=0
import discord
import asyncio
from discord.ext import commands
from queue import Queue
import string
from voice_state import VoiceState
from utils import load_opus_lib		

bot = commands.Bot(command_prefix="$", description="Music Bot")

@bot.event
async def on_ready():
	"""
		Called on script start
	"""
	print("Logged in as: ", bot.user.name)

class Playlist:
	def __init__(self, bot):
		load_opus_lib()
		self.bot = bot
		self.voice_state = VoiceState(self.bot)
		self.bot.add_cog(self.voice_state)
		
		self.queue = asyncio.Queue()
		self.play_event = asyncio.Event()
		self.bot.loop.create_task(self.play())

	def toggle(self):
		self.bot.loop.call_soon_threadsafe(self.play_event.set)
	
	@commands.command(pass_context=True)
	async def add(self, ctx, url : str):
		if not self.voice_state.is_active():
			self.voice_state.join(ctx.message.author.voice_channel)
		await bot.say("Adding song to playlist...")
		await self.queue.put(url)

	@commands.command()
	async def kill(self):
		if self.player != None:
			self.player.stop()

	@commands.command()
	async def pause(self):
		if self.player != None:
			self.player.pause()
	
	@commands.command()
	async def resume(self):
		if self.player != None:
			self.player.resume()
	
	async def play(self):
		while True:
			self.play_event.clear()
			url = await self.queue.get()
			self.player = await self.voice_state.create_ytdl_player(url, after=self.toggle)
			self.player.start()
			await self.play_event.wait()

	@commands.command()
	async def scared():
		await bot.say("https://i.imgur.com/Dqbyu3x.gifv")

if __name__ == "__main__":
	bot.add_cog(Playlist(bot))
	bot.run('NDI2NTI0MDg0MDA0NzE2NTU3.DZXPBA.h7B44TMwKXmD-PWbgF5_LK8bZj4')
