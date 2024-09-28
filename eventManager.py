from typing import Callable
import pygame as pg



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