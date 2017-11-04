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
from random import choice
from discord.ext import commands

bot = commands.Bot(command_prefix=":", description="Test Bot")


@bot.event
async def on_ready():
	"""
		Called on script start
	"""
	print("Logged in as: ", bot.user.name)

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


@bot.command(description="Rolls a die Format: \":roll_die arg\"")
async def roll_die(maximum : int):
	"""
		Int -> int
		Takes in an integer as the max number on the die and prints a
		random selection to the chat
	"""
	await bot.say(choice(range(1, maximum)))

bot.run('Mzc1Njg5Mjg1NjkwNTg5MTg2.DNzfkw.SaEXRWDODM5NaeBh0sOnxy6j6ok')
