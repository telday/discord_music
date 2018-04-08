import discord
OPUS_LIBS = ['libopus-0.x86.dll', 'libopus-0.x64.dll', 'libopus-0.dll', 'libopus.so.0', 'libopus.0.dylib']

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