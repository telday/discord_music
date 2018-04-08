"""
	file: command_writer.py
	author: Ellis Wright
	language: python 3.6
	description: Adds implementation for the bot to add custom commands
	within the discord UI (not in code)
"""
from discord.ext import commands
import discord


class CommandWriter:
	def __init__(self, bot):
		self.bot = bot

	def process_command(self, command):
		print()
