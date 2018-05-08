"""
	file: voice_state.py
	author: Ellis Wright
	language: python 3.6
	description: contains class to manage the bot user which joins and
	plays music in different channels.
"""
import discord
from discord.ext import commands


class VoiceState:
	"""
		Class representing a bot in one of the voice channel
	"""
	def __init__(self, bot):
		self.voice_channel = None
		self.bot = bot
		self.voice_state = None
	
	def is_active(self):
		"""
			Tells if the bot is currently in one of the channels
		"""
		return self.voice_state != None
	
	@commands.command(pass_context=True)
	async def summon(self, ctx):
		"""
			Summons the bot to the channel of the author of the message
		"""
		voice = ctx.message.author.voice_channel
		if self.voice_channel != voice:
			self.voice_channel = voice
			if self.voice_state != None:
				await self.voice_state.move_to(voice)
			else:
				self.voice_channel = voice
				self.voice_state = await self.bot.join_voice_channel(voice)
	
	async def join(self, voice_channel):
		"""
			Helper function to move the bot between voice channels from outside the class
		"""
		self.voice_channel = voice_channel
		self.voice_state = await self.bot.join_voice_channel(voice_channel)