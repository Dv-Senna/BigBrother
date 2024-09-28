from typing import Callable
import pygame as pg

from log_manager import Typewriter

class EventManager:
	eventTypes: dict[str, Callable[[pg.event.Event], bool]] = {}
	eventCallbacks: dict[str, dict[int, Callable[[], None]]] = {}
	lastHandlerID: int = -1


	@staticmethod
	def update() -> bool:
		for event in pg.event.get():
			if event.type == pg.QUIT:
				return False
			if event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE:
				return False

			for type in EventManager.eventTypes:
				if EventManager.eventTypes[type](event):
					for callback in EventManager.eventCallbacks[type]:
						EventManager.eventCallbacks[type][callback]()
		return True
	

	@staticmethod
	def addEventType(typeName: str, filter: Callable[[pg.event.Event], bool]) -> None:
		EventManager.eventTypes[typeName] = filter
	
	@staticmethod
	def removeEventType(typeName: str) -> None:
		EventManager.eventTypes.pop(typeName, None)
		EventManager.eventCallbacks.pop(typeName, None)

	@staticmethod
	def registerCallback(typeName: str, callback: Callable[[], None]) -> int:
		if typeName not in EventManager.eventTypes:
			print(f"\033[31mPossible typos in EventManager.registerCallback's typeName '{typeName}'\033[m")
			return -1		
		if typeName not in EventManager.eventCallbacks:
			EventManager.eventCallbacks[typeName] = {}

		EventManager.lastHandlerID += 1
		EventManager.eventCallbacks[typeName][EventManager.lastHandlerID] = callback
		return EventManager.lastHandlerID
	
	@staticmethod
	def removeCallback(typeName: str, callbackHandler: int) -> None:
		if typeName not in EventManager.eventTypes:
			print(f"\033[31mPossible typos in EventManager.removeCallback's typeName '{typeName}'\033[m")
			return
		if typeName not in EventManager.eventCallbacks:
			print(f"\033[31mType '{typeName}' has no callback set to it, so you can't remove {callbackHandler}\033[m")
			return
		
		EventManager.eventCallbacks[typeName].pop(callbackHandler, None)


# example

def leftArrowEventFilter(event: pg.event.Event):
	if event.type == pg.MOUSEBUTTONDOWN:
		return True		
	return False

def leftArrowHandler():
	print("LEFT ARROW")

def startLogHandler(typewriters, texts, font):
	for i, writer in enumerate(typewriters):
		writer.silent = True
		writer.speed = 50 - 15 * (2 - i / len(typewriters))
	typewriters.append(Typewriter(
		texts[len(typewriters)], 
		font, 
		(300, 70 + 20 * len(typewriters)), 
		speed=50,
		wait_before_start = 0))
	
def displayAllLogs(typewriters, texts, font, delay_between_each_line=5000):
	index_with_noise = 0 # get the longest sentence
	for i, text in enumerate(texts):
		if len(text) > len(texts[index_with_noise]):
			index_with_noise = i
	print(index_with_noise)
	for i, text in enumerate(texts):
		typewriters.append(Typewriter(
			text, 
			font, 
			(300, 70 + 20 * len(typewriters)), 
			#speed=50 - i / len(texts),
			silent=i != index_with_noise,
			wait_before_start = i * delay_between_each_line)),
if __name__ == "__main__":
	pg.init()

	EventManager.addEventType("left_arrow", leftArrowEventFilter)

	callbackHandler = EventManager.registerCallback("left_arrow", leftArrowHandler)

	# call this line in the mainloop. Here we just build a dummy event for test purposes
	dummyEvent = pg.event.Event(pg.MOUSEBUTTONDOWN)
	pg.event.post(dummyEvent)

	EventManager.update()

	EventManager.removeCallback("left_arrow", callbackHandler)

	dummyEvent = pg.event.Event(pg.MOUSEBUTTONDOWN)
	pg.event.post(dummyEvent)

	EventManager.update()