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
from utils.utils import load_opus_lib		
from utils.logger import Logger
from command_writer import CommandWriter
from youtube_dl.utils import ExtractorError

bot = commands.Bot(command_prefix="$", description="Music Bot")
logger = Logger()
command_writer = CommandWriter(bot)

@bot.event
async def on_ready():
	"""
		Called on script start
	"""
	print("Logged in as: ", bot.user.name)

@bot.event
async def on_message(message):
	logger.log_event("[{}][{}] : {}\n".format(message.channel, message.author, message.content))
	await command_writer.process_command(message.channel, message.content)
	await bot.process_commands(message)

class Playlist:
	def __init__(self, bot):
		global logger
		global command_writer
		load_opus_lib()
		self.bot = bot
		self.voice_state = VoiceState(self.bot)
		self.bot.add_cog(self.voice_state)
		self.bot.add_cog(command_writer)
		self.logger = logger
		self.logger.start()

		self.queue = asyncio.Queue()
		self.play_event = asyncio.Event()
		self.bot.loop.create_task(self.play())

	def toggle(self):
		self.bot.loop.call_soon_threadsafe(self.play_event.set)
	
	@commands.command(pass_context=True)
	async def add(self, ctx, url : str):
		if not self.voice_state.is_active():
			await self.voice_state.join(ctx.message.author.voice_channel)
		await bot.say("Adding song to playlist...")
		await self.queue.put((url, ctx.message.channel))

	@commands.command()
	async def skip(self):
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
			info = await self.queue.get()
			url = info[0]
			try:
				self.player = await self.voice_state.voice_state.create_ytdl_player(url, after=self.toggle)
				self.player.start()
				await self.play_event.wait()
			except Exception as e:
				#For some reason youtube_dl wont let me catch its errors here so we have to go general TODO: find a fix?
				await self.bot.send_message(info[1], "The given URL was invalid...")
	
	
	@commands.command()
	async def restart(self):
		#Some would call this a crude hack... They'd be right.
		exit(1)

if __name__ == "__main__":
	file_ = open("token.txt", 'r')
	token = file_.readline().strip()
	file_.close()
	
	bot.add_cog(Playlist(bot))
	bot.run(token)
