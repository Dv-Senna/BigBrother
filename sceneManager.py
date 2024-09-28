import pygame as pg
import config


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
	transitionTimer: int = 0
	blackScreenOpacity: int = 0
	

	@staticmethod
	def setCurrentScene(sceneName: str):
		if sceneName == SceneManager.currentScene:
			return

		if sceneName not in SceneManager.scenes:
			print(f"\033[31mYou try to set scene '{sceneName}' as the current scene, but it does not exist\033[m")
			return

		SceneManager.targetScene = sceneName

	@staticmethod
	def update(dt: int):
		if SceneManager.currentScene != "":
			SceneManager.scenes[SceneManager.currentScene].update(dt)

		if SceneManager.targetScene == "":
			return

		if SceneManager.transitionTimer == 0:
			if SceneManager.currentScene != "":
				SceneManager.scenes[SceneManager.currentScene].unmount()


		SceneManager.transitionTimer += dt
		if SceneManager.currentScene[:-1] == "doorScene":
			if SceneManager.transitionTimer < config.BLACK_FADE_TRANSITION_TIME / 2:
				SceneManager.blackScreenOpacity = SceneManager.transitionTimer / config.BLACK_FADE_TRANSITION_TIME * 255 * 2
			else:
				SceneManager.currentScene = SceneManager.targetScene
				SceneManager.blackScreenOpacity = 255 - (SceneManager.transitionTimer - config.BLACK_FADE_TRANSITION_TIME / 2) / config.BLACK_FADE_TRANSITION_TIME * 255 * 2

		else:
			pass

		if SceneManager.transitionTimer < config.BLACK_FADE_TRANSITION_TIME:
			return
		
		SceneManager.currentScene = SceneManager.targetScene
		SceneManager.targetScene = ""
		SceneManager.scenes[SceneManager.currentScene].mount()
		SceneManager.transitionTimer = 0

	@staticmethod
	def render(window: pg.Surface):
		if SceneManager.currentScene != "":
			SceneManager.scenes[SceneManager.currentScene].render(window)

	@staticmethod
	def getCurrentScene():
		return SceneManager.scenes[SceneManager.currentScene]

	@staticmethod
	def getCurrentSceneName():
		return SceneManager.currentScene
	
	@staticmethod
	def addScene(sceneName: str, scene: Scene):
		SceneManager.scenes[sceneName] = scene

