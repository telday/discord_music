"""
	file: d_bot.py
	author: Ellis Wright/Brian Shaw
	language: python 3.6
	description: Bot with few functionalities for discord
"""
#NOTE: DEPENDENCY: python3 discord module
#https://discordapp.com/api/oauth2/authorize?client_id=375689285690589186&scope=bot&permissions=0
import discord
import roast_adam
from time import time
import uptime
from random import choice
from discord.ext import commands
import simple_commands

bot = commands.Bot(command_prefix=":", description="Test Bot")
start_time = 0

@bot.event
async def on_ready():
	"""
		Called on script start
	"""
	global start_time
	print("Logged in as: ", bot.user.name)
	start_time = time()

#NOTE: Only works on messages cached after the bot starts running
@bot.event
async def on_message_delete(message):
	"""
		String
		Takes in the message object, uses a formatter to grab text
		and prints to the chat.
		Note: The author and deletor can also be derived from the message obj
	"""
	#Corrects for infinitely recursing bot messages
	if message.author.name == "test-bot":
		return
	fmt = 'Why would you delete a message as beautiful as:\n{0.content}'
	await bot.send_message(message.channel, fmt.format(message))

@bot.command(description="Flips a coin?")
async def flip_coin():
	"""
		Really?
	"""
	await bot.say(choice(["Heads", "Tails"]))

@bot.command(description="How salty is Adam?")
async def adam_salt():
	"""
		No input
		Return a random String
	"""
	await bot.say(roast_adam.salty_status())


@bot.command(description="Rolls a die")
async def roll_die(minimum : int, maximum : int):
	"""
		NatNum * NatNum -> NatNum
		Takes in an integer as the min and max number on the die and prints a
		random selection to the chat.
	"""
	await bot.say(simple_commands.roll_die_l(minimum, maximum))

@bot.command(description="Gets the uptime of the bot")
async def uptime():
	global start_time
	await bot.say("{0:.2f}".format(time() - start_time) + " seconds")

bot.run('Mzc1Njg5Mjg1NjkwNTg5MTg2.DNzfkw.SaEXRWDODM5NaeBh0sOnxy6j6ok')
