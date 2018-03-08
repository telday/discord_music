"""
	file: Playlist.py
	description: class for a playlist for the music bot to use
	
	author: Ellis Wright
	language: python3.6
"""
import discord
from discord.ext import commands


class Playlist:
	#List of all the libraries opus needs
	OPUS_LIBS = ['libopus-0.x86.dll', 'libopus-0.x64.dll', 'libopus-0.dll', 'libopus.so.0', 'libopus.0.dylib']
	player = None
	voice_channel = None
	
	def __init__(self, bot):
		self.load_opus_lib()
		self.bot = bot
	
	
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

	
	async def play_link(self, bot, voice_channel, url):
		"""
			Plays the given link on the given bot in the given voice channel.
		"""
		if self.player != None and not self.player.is_done():
			self.player.stop()
		
		try:
			self.voice_channel = await bot.join_voice_channel(voice_channel)
		except Exception:
			pass
		
		self.player = await self.voice_channel.create_ytdl_player(url)
		self.player.start()
	
	@commands.command(description="Sets the volume of the youtube player")
	async def set_volume(self, vol : float):
		if (vol >= 0 and vol <= 1):
			if (self.player != None and self.player.is_playing()):
				self.player.volume = vol