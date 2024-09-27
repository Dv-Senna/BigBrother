from typing import Callable
import pygame as pg


class Scene:
	def __init__(self):
		pass

	def update(self):
		pass

	def render(self, window: pg.Surface):
		pass


class SceneManager:
	currentScene: str = ""
	scenes: dict[str, Scene] = {}
	
	@staticmethod
	def setCurrentScene(sceneName: str):
		SceneManager.currentScene = sceneName

	@staticmethod
	def getCurrentScene():
		return SceneManager.scenes[SceneManager.currentScene]

	@staticmethod
	def getCurrentSceneName():
		return SceneManager.currentScene
	
	@staticmethod
	def addScene(sceneName: str, scene: Scene):
		SceneManager.scenes[sceneName] = scene

