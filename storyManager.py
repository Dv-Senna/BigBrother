import json
from typing import List


class StoryManager:
	def __init__(self):
		self.currentPerson = ""
		self.currentDialogID = ""
		self.story = {}
		self.dialogs = {}
		self.logs = {}
		self.alreadyPlayedDialog: dict[str, List[str]] = {}
		self.alreadyPlayedLog: dict[str, List[str]] = {}

	def setup(self):
		with open("assets/story.json", "r") as storyFile:
			self.story = json.load(storyFile)
		with open("assets/dialogs.json", "r") as dialogsFile:
			self.dialogs = json.load(dialogsFile)

	def selectPerson(self, person: str):
		if person not in self.dialogs:
			print(f"\033[31mInvalid person id '{person}'\033[m")
			return
		self.currentPerson = person

	def selectDialog(self, dialog: str):
		for dialogObject in self.dialogs[self.currentPerson]:
			if dialogObject["id"] == dialog:
				self.currentDialogID = dialog
				if self.currentPerson not in self.alreadyPlayedDialog:
					self.alreadyPlayedDialog[self.currentPerson] = []
				self.alreadyPlayedDialog[self.currentPerson].append(self.currentDialogID)
				return

		print(f"\033[31mInvalid dialog id '{dialog}'\033[m")
		return

	def getAvailableLogs(self):
		return self.logs[self.currentPerson]

	def selectLog(self, log: str):
		for logObject in self.logs[self.currentPerson]:
			if logObject["id"] != log:
				continue
			if logObject["dialog"] == "":
				return
			self.selectDialog(logObject["dialog"])
			return
	

	def getCurrentDialog(self):
		for dialog in self.dialogs[self.currentPerson]:
			if dialog["id"] != self.currentDialogID:
				continue

			return dialog
		return {}
	