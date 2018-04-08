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
		self.queue.put(event)
	
	def stop_logging(self):
		self.is_logging = False

	def run(self):
		while self.is_logging or self.queue.qsize() != 0:
			fle = open(self.file_, 'a')
			event = self.queue.get()
			fle.write(event)
			fle.close()
