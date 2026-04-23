"""轻量信息通知"""

# pylint: disable=unexpected-keyword-arg

import flet as ft

snack_bar = ft.SnackBar(
    "Fantastair",
    show_close_icon=True,
    duration=1000,
)

page: ft.Page


def init(page_: ft.Page) -> None:
    """初始化轻量信息通知"""
    global page
    page = page_


def show_message(message: str, bgcolor: ft.ColorValue | None = None) -> None:
    """显示轻量信息通知"""
    snack_bar.content = message
    if bgcolor is not None:
        snack_bar.bgcolor = bgcolor
    try:
        page.show_dialog(snack_bar)
    except RuntimeError:
        pass
