"""主界面场景"""

# pylint: disable=unexpected-keyword-arg

import flet as ft

from scene import Scene


@ft.control
class MainScene(ft.Row, Scene):
    """主界面场景"""

    LEFT_CARD_WIDTH = 180  # 左侧卡片宽度
    BOTTOM_RIGHT_HEIGHT = 220  # 右下卡片固定高度
    CARD_SPACING = 10  # 卡片间距

    def __init__(self) -> None:
        """初始化主界面场景"""
        ft.Row.__init__(self)
        Scene.__init__(self)

        self.expand = True
        self.spacing = self.CARD_SPACING

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
            # expand=True,
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
            # expand=True,
            elevation=5,
        )

        self.right_column = ft.Column(
            [
                self.topright_card,
                self.bottomright_card,
            ],
            expand=True,
            spacing=self.CARD_SPACING,
            # alignment=ft.MainAxisAlignment.START,
        )

        self.controls = [
            self.left_card,
            self.right_column,
        ]
