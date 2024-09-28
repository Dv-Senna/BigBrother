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
	targetScene: str = ""
	scenes: dict[str, Scene] = {}
	
	@staticmethod
	def setCurrentScene(sceneName: str):
		if sceneName == SceneManager.currentScene:
			return

		if sceneName not in SceneManager.scenes:
			print(f"\033[31mYou try to set scene '{sceneName}' as the current scene, but it does not exist\033[m")
			return

		SceneManager.targetScene = sceneName

	@staticmethod
	def update():
		if SceneManager.targetScene == "":
			return

		SceneManager.currentScene = SceneManager.targetScene
		SceneManager.targetScene = ""
		if SceneManager.currentScene != "":
			SceneManager.scenes[SceneManager.currentScene].unmount()
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

