""" 前端入口 """

from pathlib import Path

import flet as ft

from scene import SceneManager
from login_scene import LoginScene
from main_scene import MainScene

CWD = Path(__file__).parent


async def main(page: ft.Page) -> None:
    """前端主函数"""
    page.title = "Fantas 元件仓储管理器"
    page.window.min_height = 450
    page.window.min_width = 800

    login_scene = LoginScene()
    main_scene = MainScene()

    SceneManager.init(page)
    SceneManager.set_scene_route(login_scene, "login_success", main_scene)
    SceneManager.set_scene_route(main_scene, "logout", login_scene)

    SceneManager.switch_scene(login_scene)


if __name__ == "__main__":
    ft.run(main)
