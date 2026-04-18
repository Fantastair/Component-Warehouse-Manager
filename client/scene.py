"""场景管理模块"""

import uuid
from abc import ABC
from dataclasses import dataclass

import flet as ft


class Scene(ABC):
    """场景基类"""

    def __init__(self) -> None:
        """初始化场景"""
        self.uid = uuid.uuid4()

    def show_page(self, page: ft.Page) -> None:
        """显示场景"""
        page.add(self)  # type: ignore[arg-type]
        page.update()

    def close_page(self, page: ft.Page) -> None:
        """关闭场景"""
        page.remove(self)  # type: ignore[arg-type]
        page.update()


@dataclass(slots=True, frozen=True)
class SceneRoute:
    """场景路线"""

    scene_uid: uuid.UUID  # 当前场景的唯一标识符
    route: str  # 切换路径标识


class SceneManager:
    """场景管理器"""

    page: ft.Page
    current_scene: Scene | None = None
    scene_routes: dict[SceneRoute, Scene] = {}

    @classmethod
    def init(cls, page: ft.Page) -> None:
        """初始化场景管理器"""
        cls.page = page

    @classmethod
    def switch_scene(cls, new_scene: Scene) -> None:
        """切换场景"""
        if cls.current_scene is not None:
            cls.current_scene.close_page(cls.page)
        new_scene.show_page(cls.page)
        cls.current_scene = new_scene

    @classmethod
    def set_scene_route(
        cls, current_scene: Scene, route: str, new_scene: Scene
    ) -> None:
        """设置场景路线"""
        cls.scene_routes[SceneRoute(current_scene.uid, route)] = new_scene

    @classmethod
    def walk(cls, scene: Scene, route: str) -> None:
        """按照路线切换场景"""
        new_scene = cls.scene_routes.get(SceneRoute(scene.uid, route))
        if new_scene is not None:
            cls.switch_scene(new_scene)
