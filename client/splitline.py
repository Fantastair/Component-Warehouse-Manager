""" 分割线UI """

from typing import Callable

import fantas

import color


class SplitLine(fantas.Label):  # type: ignore[misc]
    """分割线UI组件，支持水平和垂直两种模式，允许用户通过拖动调整布局"""

    def __init__(self, rect: fantas.Rect, axis: str, boundary: list[int]):
        style = fantas.LabelStyle(
            bgcolor=color.WHITE,
        )
        super().__init__(rect, style)
        self.axis = axis
        self.boundary = boundary
        self.dragging = False
        self.mouse_hovered = False
        self.drag_offset = 0
        self.dragged_callback: Callable[[fantas.Rect], None] | None = None
        self.drag_bar = fantas.Label(
            fantas.Rect(
                0,
                0,
                (self.rect.width // 2 - 1) if axis == "v" else (self.rect.width // 10),
                (
                    (self.rect.height // 2 - 1)
                    if axis == "h"
                    else (self.rect.height // 10)
                ),
            ),
            fantas.LabelStyle(
                bgcolor=color.GRAY,
                border_radius=min(self.rect.width, self.rect.height) // 4,
            ),
        )
        self.append(self.drag_bar)
        self.drag_bar.rect.center = (self.rect.width // 2, self.rect.height // 2)

    def clamp(self) -> None:
        """将分割线位置限制在边界范围内，适用于意外超出边界后复位"""
        if self.axis == "v":
            self.rect.centerx = fantas.math.clamp(
                self.rect.centerx, self.boundary[0], self.boundary[1]
            )
        else:
            self.rect.centery = fantas.math.clamp(
                self.rect.centery, self.boundary[0], self.boundary[1]
            )

    def on_mouse_entered(self, event: fantas.Event) -> bool:
        """鼠标进入分割线区域，改变鼠标样式"""
        if event.ui is self:
            self.mouse_hovered = True
            if self.axis == "v":
                fantas.set_cursor("-")
            else:
                fantas.set_cursor("|")
            return True
        return False

    def on_mouse_leaved(self, event: fantas.Event) -> bool:
        """鼠标离开分割线区域，恢复鼠标样式"""
        if event.ui is self:
            self.mouse_hovered = False
            if not self.dragging:
                fantas.set_cursor("^")
            return True
        return False

    def on_mouse_button_down(self, event: fantas.Event) -> bool:
        """鼠标按下分割线，开始拖动"""
        self.dragging = True
        self.label_style.border_width = 2
        if self.axis == "v":
            self.label_style.border_radius = self.rect.width // 2
            self.drag_offset = event.pos[0] - self.rect.centerx
        else:
            self.label_style.border_radius = self.rect.height // 2
            self.drag_offset = event.pos[1] - self.rect.centery
        return True

    def on_mouse_button_up(self, _: fantas.Event) -> bool:
        """鼠标释放分割线，停止拖动"""
        if self.dragging:
            self.dragging = False
            self.label_style.border_width = 0
            self.label_style.border_radius = 0
            fantas.set_cursor("^")
            return True
        return False

    def on_mouse_motion(self, event: fantas.Event) -> bool:
        """鼠标移动时，如果正在拖动分割线，调整分割线位置"""
        if self.dragging:
            if self.axis == "v":
                new_centerx = event.pos[0] - self.drag_offset
                new_centerx = fantas.math.clamp(
                    new_centerx, self.boundary[0], self.boundary[1]
                )
                self.rect.centerx = new_centerx
            else:
                new_centery = event.pos[1] - self.drag_offset
                new_centery = fantas.math.clamp(
                    new_centery, self.boundary[0], self.boundary[1]
                )
                self.rect.centery = new_centery
            if self.dragged_callback is not None:
                self.dragged_callback(self.rect)
            return True
        return False

    def add_event_listeners(self, window: fantas.Window) -> None:
        """添加必要的事件监听器到窗口"""
        window.add_event_listener(
            fantas.MOUSEENTERED, self, False, self.on_mouse_entered
        )
        window.add_event_listener(fantas.MOUSELEAVED, self, False, self.on_mouse_leaved)
        window.add_event_listener(
            fantas.MOUSEBUTTONDOWN, self, False, self.on_mouse_button_down
        )
        window.add_event_listener(
            fantas.MOUSEBUTTONUP, self.father, False, self.on_mouse_button_up
        )
        window.add_event_listener(
            fantas.MOUSEMOTION, self.father, False, self.on_mouse_motion
        )
