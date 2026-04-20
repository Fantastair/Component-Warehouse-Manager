"""主界面场景"""

# pylint: disable=unexpected-keyword-arg

import flet as ft

from scene import Scene


@ft.control
class MainScene(ft.Row, Scene):
    """主界面场景"""

    LEFT_CARD_WIDTH = 180  # 左侧卡片宽度
    LEFT_CARD_WIDTH_MIN = 150  # 左侧卡片最小宽度
    BOTTOM_RIGHT_HEIGHT = 220  # 右下卡片固定高度
    BOTTOM_RIGHT_HEIGHT_MIN = 200  # 右下卡片最小高度
    CARD_SPACING = 10  # 卡片间距

    def __init__(self) -> None:
        """初始化主界面场景"""
        ft.Row.__init__(self)
        Scene.__init__(self)

        self.expand = True
        self.spacing = 0

        self.left_card = ft.Card(
            ft.Container(
                ft.Column(
                    [
                        ft.Icon(ft.Icons.DASHBOARD, size=40, color=ft.Colors.BLUE),
                        ft.Text("左侧区域", size=20, weight=ft.FontWeight.BOLD),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                padding=20,
                alignment=ft.Alignment.CENTER,
            ),
            width=self.LEFT_CARD_WIDTH,
            elevation=5,
        )

        self.topright_card = ft.Card(
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Icon(ft.Icons.ANALYTICS, size=40, color=ft.Colors.GREEN),
                        ft.Text("右上区域", size=20, weight=ft.FontWeight.BOLD),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                alignment=ft.Alignment.CENTER,
                padding=20,
            ),
            expand=True,
            elevation=5,
        )

        self.bottomright_card = ft.Card(
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Icon(ft.Icons.SETTINGS, size=40, color=ft.Colors.ORANGE),
                        ft.Text("右下区域", size=20, weight=ft.FontWeight.BOLD),
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                alignment=ft.Alignment.CENTER,
                padding=20,
            ),
            height=self.BOTTOM_RIGHT_HEIGHT,
            elevation=5,
        )

        self.vertical_divider = ft.GestureDetector(
            ft.VerticalDivider(
                width=self.CARD_SPACING,
                thickness=self.CARD_SPACING,
                color=ft.Colors.TRANSPARENT,
            ),
            mouse_cursor=ft.MouseCursor.RESIZE_LEFT_RIGHT,
            drag_interval=12,
            on_pan_update=self.move_vertical_divider,
        )
        self.horizontal_divider = ft.GestureDetector(
            ft.Divider(
                height=self.CARD_SPACING,
                thickness=self.CARD_SPACING,
                color=ft.Colors.TRANSPARENT,
            ),
            mouse_cursor=ft.MouseCursor.RESIZE_UP_DOWN,
            drag_interval=12,
            on_pan_update=self.move_horizontal_divider,
        )

        self.right_column = ft.Column(
            [
                self.topright_card,
                self.horizontal_divider,
                self.bottomright_card,
            ],
            expand=True,
            spacing=0,
        )

        self.controls = [
            self.left_card,
            self.vertical_divider,
            self.right_column,
        ]

    def show_page(self, page: ft.Page) -> None:
        """显示页面时，设置窗口标题并绑定窗口大小变化事件"""
        super().show_page(page)
        page.on_resize = self.resize

    def close_page(self, page: ft.Page) -> None:
        """关闭页面时，重置窗口标题并解绑窗口大小变化事件"""
        super().close_page(page)
        page.on_resize = None

    def move_vertical_divider(self, e: ft.DragUpdateEvent) -> None:
        """移动垂直分割线，调整左右卡片宽度"""
        if (
            self.left_card.width is None
            or e.local_delta is None
            or self.page.width is None
        ):
            return
        new_left_width = self.left_card.width + e.local_delta.x
        if not (
            self.LEFT_CARD_WIDTH_MIN
            <= new_left_width
            <= self.page.width - self.LEFT_CARD_WIDTH_MIN - self.CARD_SPACING
        ):
            return
        self.left_card.width = new_left_width
        self.left_card.update()

    def move_horizontal_divider(self, e: ft.DragUpdateEvent) -> None:
        """移动水平分割线，调整右上右下卡片高度"""
        if (
            self.bottomright_card.height is None
            or e.local_delta is None
            or self.page.height is None
        ):
            return
        new_bottom_height = self.bottomright_card.height - e.local_delta.y
        if not (
            self.BOTTOM_RIGHT_HEIGHT_MIN
            <= new_bottom_height
            <= self.page.height - self.BOTTOM_RIGHT_HEIGHT_MIN - self.CARD_SPACING
        ):
            return
        self.bottomright_card.height = new_bottom_height
        self.bottomright_card.update()

    def resize(self, e: ft.PageResizeEvent) -> None:
        """窗口大小变化时，自动限制卡片尺寸，避免超出窗口"""
        if self.left_card.width is None or self.bottomright_card.height is None:
            return

        max_left_width = e.width - self.LEFT_CARD_WIDTH_MIN - self.CARD_SPACING
        if self.left_card.width > max_left_width:
            self.left_card.width = max_left_width
            self.left_card.update()

        max_bottom_height = e.height - self.BOTTOM_RIGHT_HEIGHT_MIN - self.CARD_SPACING
        if self.bottomright_card.height > max_bottom_height:
            self.bottomright_card.height = max_bottom_height
            self.bottomright_card.update()
