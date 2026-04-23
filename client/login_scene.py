"""登录场景"""

# pylint: disable=unexpected-keyword-arg

import flet as ft

import serverapi
import lite_message
from scene import Scene, SceneManager


@ft.control
class LoginScene(ft.Container, Scene):
    """登录场景"""

    def __init__(self) -> None:
        """初始化登录场景"""
        ft.Container.__init__(self, expand=True, alignment=ft.Alignment.CENTER)
        Scene.__init__(self)

        self.page: ft.Page
        self.title = ft.Row(
            [
                ft.Icon(ft.Icons.VERIFIED_USER_ROUNDED, size=30),
                ft.Text("身份验证", weight=ft.FontWeight.BOLD, size=20),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            tight=True,
        )
        self.host_input = ft.TextField(label="服务器地址", value=serverapi.HTTP_HOST)
        self.port_input = ft.TextField(
            label="服务器端口", value=str(serverapi.HTTP_PORT)
        )
        self.token_input = ft.TextField(
            label="访问令牌",
            value=serverapi.API_TOKEN if serverapi.API_TOKEN is not None else "",
            password=True,
            can_reveal_password=True,
        )
        self.logining_ring = ft.ProgressRing(
            visible=False,
            width=16,
            height=16,
            color=ft.Colors.BLUE_300,
            stroke_width=3,
            stroke_cap=ft.StrokeCap.ROUND,
        )
        self.login_button = ft.Button(
            content=ft.Row(
                [
                    ft.Text("登录", size=20),
                    self.logining_ring,
                ],
                tight=True,
            ),
            icon=ft.Icons.LOGIN_ROUNDED,
            bgcolor=ft.Colors.BLUE_100,
            on_click=self.on_login_button_click,
            autofocus=True,
        )

        self.login_card = ft.Card(
            ft.Container(
                content=ft.Column(
                    [
                        self.title,
                        self.host_input,
                        self.port_input,
                        self.token_input,
                        self.login_button,
                        self.logining_ring,
                    ],
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    alignment=ft.MainAxisAlignment.CENTER,
                    spacing=20,
                ),
                padding=20,
                alignment=ft.Alignment.CENTER,
            ),
            elevation=5,
            width=400,
            height=400,
        )

        self.content = self.login_card

        self.login_request_uid: int | None = None

    def show_page(self, page: ft.Page) -> None:
        page.title = "登录 - Fantas 元件仓储管理器"
        return super().show_page(page)

    def close_page(self, page: ft.Page) -> None:
        page.title = "Fantas 元件仓储管理器"
        return super().close_page(page)

    def on_login_button_click(self) -> None:
        """登录按钮点击事件"""
        self.page.run_task(self.login)

    async def login(self) -> None:
        """执行登录操作"""
        self.logining_ring.visible = True  # 显示加载动画
        self.login_button.disabled = True  # 禁用登录按钮
        self.update()

        try:
            result = await serverapi.verify_token(
                self.host_input.value, self.port_input.value, self.token_input.value
            )
            if result:
                lite_message.show_message("身份验证成功！", ft.Colors.GREEN_400)
                SceneManager.walk(self, "login_success")
            else:
                lite_message.show_message("身份验证失败！", ft.Colors.RED_400)
        finally:
            self.logining_ring.visible = False  # 隐藏加载动画
            self.login_button.disabled = False  # 启用登录按钮
            self.update()
