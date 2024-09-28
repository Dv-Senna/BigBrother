import json
from typing import List


class StoryManager:
	currentPerson = ""
	currentDialogID = ""
	dialogs = {}
	logs = {}
	alreadyPlayedDialog: dict[str, List[str]] = {}
	alreadyPlayedLog: dict[str, List[str]] = {}

	def setup():
		with open("assets/dialogs.json", "r") as dialogsFile:
			StoryManager.dialogs = json.load(dialogsFile)
		with open("assets/log.json", "r") as logFile:
			StoryManager.logs = json.load(logFile)

	def selectPerson(person: str):
		if person not in StoryManager.dialogs:
			print(f"\033[31mInvalid person id '{person}'\033[m")
			return
		StoryManager.currentPerson = person

	def selectDialog(dialog: str):
		StoryManager.currentDialogID = dialog
		return

	def getAvailableLogs():
		return StoryManager.logs[StoryManager.currentPerson]

	def selectLog(log: str):
		for logObject in StoryManager.logs[StoryManager.currentPerson]:
			if logObject["id"] != log:
				continue
			if logObject["dialog"] == "":
				return
			StoryManager.selectDialog(logObject["dialog"])
			return
	

	def getCurrentDialog():
		for dialog in StoryManager.dialogs[StoryManager.currentPerson]:
			if dialog["id"] != StoryManager.currentDialogID:
				continue

			return dialog
		return {}
	
	def getLog():
		return StoryManager.logs[StoryManager.currentPerson]