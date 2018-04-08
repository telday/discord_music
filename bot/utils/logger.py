"""
	file: logger.py
	author: Ellis Wright
	language: python3.6
	description: Simple threaded logging application to log all messages
	sent in the server
"""
from threading import Thread
from time import strftime
from queue import Queue

class Logger(Thread):
	def __init__(self, daemon=True):
		Thread.__init__(self, daemon=True)
		self.file_ = "log/" + strftime("%m.%d.%Y") + ".lg"
		self.queue = Queue()
		self.is_logging = True
	
	def log_event(self, event:str):
		"""
			Adds an event to the logger's queue
		"""
		#TODO Add capabilities for logging file/media uploads
		self.queue.put(event)
	
	def stop_logging(self):
		"""
			Toggles the logging feature
		"""
		self.is_logging = not self.is_logging

	def run(self):
		"""
			Main loop for getting items from the queue and printing them
		"""
		while self.is_logging or self.queue.qsize() != 0:
			fle = open(self.file_, 'a')
			event = self.queue.get()
			fle.write(event)
			fle.close()
