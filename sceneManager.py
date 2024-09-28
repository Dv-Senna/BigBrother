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

	currentTransition = ""
	oldCurrentScene: str = ""
	oldDoorScreen: pg.Surface = pg.Surface((config.WINDOW_WIDTH, config.WINDOW_HEIGHT))
	newDoorScreen: pg.Surface = pg.Surface((config.WINDOW_WIDTH, config.WINDOW_HEIGHT))
	oldDoorScreenRect: pg.Rect = pg.Rect(0, 0, config.WINDOW_WIDTH, config.WINDOW_HEIGHT)
	newDoorScreenRect: pg.Rect = pg.Rect(0, 0, config.WINDOW_WIDTH, config.WINDOW_HEIGHT)
	newDoorIndex: int = -1
	oldDoorIndex: int = -1

	

	@staticmethod
	def setCurrentScene(sceneName: str):
		if sceneName == SceneManager.currentScene:
			return

		if sceneName not in SceneManager.scenes:
			print(f"\033[31mYou try to set scene '{sceneName}' as the current scene, but it does not exist\033[m")
			return

		SceneManager.targetScene = sceneName
		if SceneManager.currentScene[:-1] == "doorScene" and SceneManager.targetScene[:-1] == "doorScene":
			SceneManager.oldCurrentScene = SceneManager.currentScene
			SceneManager.currentScene = SceneManager.targetScene
			SceneManager.currentTransition = "slide"

			SceneManager.oldDoorIndex = int(SceneManager.oldCurrentScene[-1])
			SceneManager.newDoorIndex = int(SceneManager.currentScene[-1])

		else:
			SceneManager.currentTransition = "black"

	@staticmethod
	def update(dt: int):

		if SceneManager.targetScene == "":
			return

		if SceneManager.transitionTimer == 0:
			if SceneManager.currentScene != "":
				SceneManager.scenes[SceneManager.currentScene].unmount()

		SceneManager.transitionTimer += dt



		if SceneManager.currentTransition == "slide":
			SceneManager.oldDoorScreenRect.x = int(- SceneManager.transitionTimer / config.SLIDE_TRANSITION_TIME * config.WINDOW_WIDTH)
			SceneManager.newDoorScreenRect.x = int(config.WINDOW_WIDTH - SceneManager.transitionTimer / config.SLIDE_TRANSITION_TIME * config.WINDOW_WIDTH)

			if SceneManager.oldDoorIndex > SceneManager.newDoorIndex:
				SceneManager.oldDoorScreenRect.x *= -1
				SceneManager.newDoorScreenRect.x *= -1

			if SceneManager.transitionTimer < config.SLIDE_TRANSITION_TIME:
				return

			SceneManager.targetScene = ""
			SceneManager.scenes[SceneManager.currentScene].mount()
			SceneManager.transitionTimer = 0
			SceneManager.oldDoorScreenRect.x = 0
			SceneManager.newDoorScreenRect.x = 0
			SceneManager.currentTransition = ""

		else:
			if SceneManager.transitionTimer < config.BLACK_FADE_TRANSITION_TIME / 2:
				SceneManager.blackScreenOpacity = SceneManager.transitionTimer / config.BLACK_FADE_TRANSITION_TIME * 255 * 2
			else:
				SceneManager.currentScene = SceneManager.targetScene
				SceneManager.blackScreenOpacity = 255 - (SceneManager.transitionTimer - config.BLACK_FADE_TRANSITION_TIME / 2) / config.BLACK_FADE_TRANSITION_TIME * 255 * 2

			if SceneManager.transitionTimer < config.BLACK_FADE_TRANSITION_TIME:
				return
			
			SceneManager.currentScene = SceneManager.targetScene
			SceneManager.targetScene = ""
			SceneManager.scenes[SceneManager.currentScene].mount()
			SceneManager.transitionTimer = 0
			SceneManager.currentTransition = ""




	@staticmethod
	def render(window: pg.Surface):
		if SceneManager.currentScene != "":
			if SceneManager.currentTransition == "slide":
				SceneManager.scenes[SceneManager.oldCurrentScene].render(SceneManager.oldDoorScreen)
				SceneManager.scenes[SceneManager.currentScene].render(SceneManager.newDoorScreen)
				window.blit(SceneManager.oldDoorScreen, SceneManager.oldDoorScreenRect)
				window.blit(SceneManager.newDoorScreen, SceneManager.newDoorScreenRect)

			else:
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

