from typing import Callable


class Scene:
	def __init__(self, updateCallback: Callable[[], None], renderCallback: Callable[[], None]):
		self.updateCallback = updateCallback
		self.renderCallback = renderCallback


class SceneManager:
	currentScene: str = ""
	scenes: dict[str, Scene]
	
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

