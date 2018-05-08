"""
	file: logger.py
	author: Ellis Wright
	language: python3.6
	description: Simple asynchronous logging application to log all messages
	sent in the server
"""
from time import strftime
from asyncio import Queue

class Logger:
	def __init__(self):
		self.file_ = "log/" + strftime("%m.%d.%Y") + ".lg"
		self.queue = Queue()
		self.is_logging = True
	
	async def log_event(self, event:str):
		"""
			Adds an event to the logger's queue
		"""
		#TODO Add capabilities for logging file/media uploads
		await self.queue.put(event)
	
	async def run(self):
		"""
			Main loop for getting items from the queue and printing them
		"""
		while self.is_logging or self.queue.qsize() != 0:
			fle = open(self.file_, 'a')
			event = await self.queue.get()
			fle.write(event)
			fle.close()
