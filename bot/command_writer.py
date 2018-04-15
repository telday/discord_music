"""
	file: command_writer.py
	author: Ellis Wright
	language: python 3.6
	description: Adds implementation for the bot to add custom commands
	within the discord UI (not in code)
"""
from discord.ext import commands
import discord

#TODO add a command to remove commands from the bot. They will have to be removed from the file as well

class CommandWriter:
	'''
		Class allows users to add their own custom commands to the bot. Allowing
		the bot to say things whenever they want so those commands don't need
		to be hard programmed in
	'''
	def __init__(self, bot):
		"""
			Initialize the commands

			bot: The bot this command writer is running on
		"""
		self.bot = bot
		self.commands = self.load_commands()
	
	def load_commands(self):
		"""
			load the commands this bot has from the commands file and return
			them as a dictionary
		"""
		commands = {}
		try:
			file_ = open("commands", 'r')
			for line in file_.readlines():
				if line == "":
					continue
				commands[line.split("::")[0]] = line.split("::")[1].strip()
		except OSError as e:
			print("Something bad has happenned")
			file_ = open("commands", 'w')
		finally:
			file_.close()
			return commands

	def save_command(self, command:str):
		"""
			Saves a command to the commands file. Must be used because there is no 
			"on_stop" method for the discord.py api wrapper
		"""
		file_ = open("commands", 'a')
		file_.write(command + "::" + self.commands[command] + "\n")
		file_.close()
	
	@commands.command()
	async def add_command(self, command:str, output:str):
		"""
			Actual bot command for adding a new command to the bot

			command: The commands name
			output: What the bot should reply to the command
		"""
		if not command in self.commands.keys():
			self.commands[command] = output
			await self.bot.say("Command added to the bot. {}::{}".format(command, output))
			print(command + "::" + output)
			self.save_command(command)
		else:
			await self.bot.say("Sorry the bot already has that command.")

		
	async def process_command(self, channel, command):
		"""
			Used to process the commands by the main bot file.

			channel: The discord.py Channel obj to write to
			command: The command passed
		"""
		if command in self.commands.keys():
			await self.bot.send_message(channel, self.commands[command])
