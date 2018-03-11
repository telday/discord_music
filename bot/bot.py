"""
	file: bot.py
	author: Ellis Wright/Brian Shaw
	language: python 3.6
	description: Bot with few functionalities for discord
"""
#NOTE: DEPENDENCY: python3 discord module
#https://discordapp.com/api/oauth2/authorize?client_id=375689285690589186&scope=bot&permissions=0
import discord
from discord.ext import commands
from queue import Queue
from threading import Thread, Lock, Condition

bot = commands.Bot(command_prefix=":", description="Test Bot")
lock = Lock()
condition = Condition(lock)

class Player(Thread):
	voice_state = None
	
	def __init__(self, bot):
		Thread.__init__(self, daemon=True)
		self.bot = bot
		self.queue = Queue()
	
	async def join_channel(self, channel):
		self.voice_state =  await bot.join_voice_channel(channel)
		
	async def create_player(self, url):
		player = await self.voice_state.create_ytdl_player(url)
		player.start()
	
	
	def run(self):
		global condition
		while True:
			if self.queue.empty():
				condition.acquire()
				condition.wait()
				condition.release()
				
			info = self.queue.get()
			try:
				self.join_channel(info[0])
			except Exception:
				pass
			
			self.create_player(info[1])
		
		
		
class Playlist:
	OPUS_LIBS = ['libopus-0.x86.dll', 'libopus-0.x64.dll', 'libopus-0.dll', 'libopus.so.0', 'libopus.0.dylib']
	voice_channel = None

	def __init__(self, bot):
		self.load_opus_lib()
		self.bot = bot
		self.player = Player(self.bot)
		self.player.start()

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

	@commands.command(pass_context=True)
	async def add(self, ctx, url : str):
		global condition
		info = (ctx.message.author.voice_channel, url)
		self.player.queue.put(info)
		
		condition.acquire()
		condition.notify()
		condition.release()
		

@bot.event
async def on_ready():
	"""
		Called on script start
	"""
	print("Logged in as: ", bot.user.name)


@bot.command(pass_context=True, description="Play a yt link")
async def yt(ctx, url : str):
	"""
		Takes in a youtube link and plays the video
	"""
	global plr
	#Get the voice channel the author who sent the command is in
	author = ctx.message.author
	voice_channel = author.voice_channel

	await plr.play_link(bot, voice_channel, url)

@bot.command()
async def v(vol : float):
	global plr
	if plr != None:
		plr.volume = vol
	else:
		print("what the fuck")


bot.add_cog(Playlist(bot))
bot.run('Mzc1Njg5Mjg1NjkwNTg5MTg2.DNzfkw.SaEXRWDODM5NaeBh0sOnxy6j6ok')
