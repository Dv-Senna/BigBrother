import pygame as pg


class Scene:
	def __init__(self):
		pass

	def update(self, dt: int):
		pass

	def render(self, window: pg.Surface):
		pass

	def mount(self):
		pass

	def unmount(self):
		pass


class SceneManager:
	currentScene: str = ""
	scenes: dict[str, Scene] = {}
	
	@staticmethod
	def setCurrentScene(sceneName: str):
		if sceneName == SceneManager.currentScene:
			return

		if SceneManager.currentScene != "":
			SceneManager.scenes[SceneManager.currentScene].unmount()
		SceneManager.currentScene = sceneName
		SceneManager.scenes[SceneManager.currentScene].mount()

	@staticmethod
	def getCurrentScene():
		return SceneManager.scenes[SceneManager.currentScene]

	@staticmethod
	def getCurrentSceneName():
		return SceneManager.currentScene
	
	@staticmethod
	def addScene(sceneName: str, scene: Scene):
		SceneManager.scenes[sceneName] = scene

