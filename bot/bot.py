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

bot = commands.Bot(command_prefix="$", description="Test Bot")		


class Playlist:
	OPUS_LIBS = ['libopus-0.x86.dll', 'libopus-0.x64.dll', 'libopus-0.dll', 'libopus.so.0', 'libopus.0.dylib']

	player = None
	voice_state = None
	
	def __init__(self, bot):
		self.load_opus_lib()
		self.bot = bot
		self.queue = asyncio.Queue()
		self.play_event = asyncio.Event()
		self.bot.loop.create_task(self.play())

	def load_opus_lib(opus_libs=OPUS_LIBS):
		"""
			Loads the opus library for the bot to used. Required for sound.
		"""
		if discord.opus.is_loaded():
			return True

		for opus_lib in opus_libs:
			try:
				discord.opus.load_opus(opus_lib)
				return
			except OSError:
				pass

	def toggle(self):
		self.bot.loop.call_soon_threadsafe(self.play_event.set)
	
	songs = ["https://www.youtube.com/watch?v=CD-E-LDc384", "https://www.youtube.com/watch?v=94bGzWyHbu0", "https://www.youtube.com/watch?v=zUzd9KyIDrM", "https://www.youtube.com/watch?v=3L4YrGaR8E4"]
	@commands.command(pass_context=True)
	async def add_song_remote(self, ctx):
		if self.voice_state == None:
			self.voice_state = await self.bot.join_voice_channel(ctx.message.author.voice_channel)
		for i in self.songs:
			info = (ctx.message.author.voice_channel, i)
			await self.queue.put(info)
	
	@commands.command(pass_context=True)
	async def add(self, ctx, url : str):
		info = (ctx.message.author.voice_channel, url)
		if self.voice_state == None:
			self.voice_state = await self.bot.join_voice_channel(info[0])
		print("Adding song to playlist on voice channel {} with url: {}".format(ctx.message.author.voice_channel, url))
		await self.queue.put(info)

	@commands.command()
	async def kill(self):
		if self.player != None:
			self.player.stop()
	
	async def play(self):
		while True:
			self.play_event.clear()
			info = await self.queue.get()
			self.player = await self.voice_state.create_ytdl_player(info[1], after=self.toggle)
			self.player.start()
			await self.play_event.wait()

	@commands.command()
	async def pause(self):
		if self.player != None:
			self.player.pause()
	
	@commands.command()
	async def resume(self):
		if self.player != None:
			self.player.resume()
	
@bot.event
async def on_ready():
	"""
		Called on script start
	"""
	print("Logged in as: ", bot.user.name)

@bot.command()
async def v(vol : float):
	global plr
	if plr != None:
		plr.volume = vol
	else:
		print("what the fuck")

@bot.command()
async def scared():
	await bot.say("https://i.imgur.com/Dqbyu3x.gifv")

bot.add_cog(Playlist(bot))
bot.run('NDI2NTI0MDg0MDA0NzE2NTU3.DZXPBA.h7B44TMwKXmD-PWbgF5_LK8bZj4')
