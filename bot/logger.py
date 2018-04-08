from threading import Thread
from time import strftime
from queue import Queue

class Logger(Thread):
	def __init__(self):
		super.__init__(self)
		self.file_ = open(strftime("%m.%d.%Y", 'w')
		self.queue = Queue()
		self.logging = True
	
	def log_event(self, event:str):
		self.queue.put(event)
	
	def stop_logging(self):
		self.is_logging = False
		self.file_.close()

	def run(self):
		while self.is_logging:
			event = self.queue.get()
			self.file_.write(event)
