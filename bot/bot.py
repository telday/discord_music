"""
	file: bot.py
	author: Ellis Wright
	language: python 3.6
	description: Bot made mostly for playing music in a discord server with
	some other functionalities built in.
"""
#NOTE: DEPENDENCY: python3 discord module
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

#Initialize the bot as a command extended version of the client.
bot = commands.Bot(command_prefix="$", description="Music Bot")
#Initialize the logger and command writer before bot starts.
logger = Logger()
command_writer = CommandWriter(bot)

@bot.event
async def on_ready():
	"""
		Called on bot start to notify successful connection
	"""
	print("Logged in as: ", bot.user.name)

@bot.event
async def on_message(message):
	"""
		Required to process extra info for the command writer and logger before passing
		each message off to the api to process for commands.
	"""
	logger.log_event("[{}][{}] : {}\n".format(message.channel, message.author, message.content))
	await command_writer.process_command(message.channel, message.content)
	await bot.process_commands(message)

class Playlist:
	"""
		The main class for the bot to run off of. Contains most of the commands
		for the voice implementation.
	"""
	
	def __init__(self, bot):
		"""
			Adds the additional cogs for the voice_state and command_writer
			classed and starts the logger.
		"""
		global logger
		global command_writer
		#opus_libs required for voice work
		load_opus_lib()
		self.bot = bot
		
		self.voice_state = VoiceState(self.bot)
		self.bot.add_cog(self.voice_state)
		self.bot.add_cog(command_writer)
		self.logger = logger
		self.logger.start()

		#Initialization of the music queue and the loop on which they play
		self.queue = asyncio.Queue()
		self.play_event = asyncio.Event()
		self.bot.loop.create_task(self.play())

	def toggle(self):
		#Old way of changing to new song
		self.bot.loop.call_soon_threadsafe(self.play_event.set)
	
	@commands.command(pass_context=True)
	async def add(self, ctx, url : str):
		"""
			Adds a song to the queue and notifies the user.
			Checking if the url is invalid happens on song creation
		"""
		if not self.voice_state.is_active():
			await self.voice_state.join(ctx.message.author.voice_channel)
		await bot.say("Adding song to playlist...")
		await self.queue.put((url, ctx.message.channel))

	@commands.command()
	async def skip(self):
		"""
			Stops the current song and skips to next song
		"""
		if self.player != None:
			self.player.stop()

	@commands.command()
	async def pause(self):
		"""
			Pauses the music player
		"""
		if self.player != None:
			self.player.pause()
	
	@commands.command()
	async def resume(self):
		"""
			Resumes the music player
		"""
		if self.player != None:
			self.player.resume()
	
	async def play(self):
		"""
			The main loop keeping the music player going
		"""
		while True:
			#Reset play flag and get new song info from the queue
			self.play_event.clear()
			info = await self.queue.get()
			url = info[0]
			
			try:
				#Attempt to create a new player with the given url.
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
