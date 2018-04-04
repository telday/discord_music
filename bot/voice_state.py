import discord
from discord.ext import commands


class VoiceState:
	
	def __init__(self, bot):
		self.voice_channel = None
		self.bot = bot
		self.voice_state = None
	
	def is_active(self):
		return self.voice_state != None
	
	@commands.command(pass_context=True)
	async def summon(self, ctx):
		voice = ctx.message.author.voice_channel
		if self.voice_channel != voice:
			self.voice_channel = voice
			if self.voice_state != None:
				await self.voice_state.move_to(voice)
			else:
				self.voice_channel = voice
				self.voice_state = await self.bot.join_voice_channel(voice)
	
	async def join(self, voice_channel):
		self.voice_channel = voice_channel
		self.voice_state = await self.bot.join_voice_channel(voice_channel)