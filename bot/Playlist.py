"""
	file: Playlist.py
	description: class for a playlist for the music bot to use

	author: Ellis Wright
	language: python3.6
"""
import discord
from discord.ext import commands
from voice import *

class Playlist:
	#List of all the libraries opus needs
	OPUS_LIBS = ['libopus-0.x86.dll', 'libopus-0.x64.dll', 'libopus-0.dll', 'libopus.so.0', 'libopus.0.dylib']
	voice_channel = None

	def __init__(self, bot):
		self.load_opus_lib()
		self.bot = bot
		self.voice_player = VoicePlayer(self.bot, None)

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
		state = None
		try:
			state = await self.voice_player.player.join_voice_channel(voice_channel)
		except:
			pass

		self.voice_player.set_voice_state(state)
		await self.voice_player.add_song(url)

	@commands.command(pass_context=True)
	async def join(self, ctx):
		channel = ctx.message.author.voice_channel
		self.voice_player.join_channel(channel)

	@commands.command(description="Sets the volume of the youtube player")
	async def set_volume(self, vol : float):
		self.voice_player.player.volume = vol
