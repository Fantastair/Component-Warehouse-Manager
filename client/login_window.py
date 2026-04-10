""" 登录窗口模块 """

import fantas

import color
import server

login_window_config = fantas.WindowConfig(
    title="登录 - Fantas元件仓储管理器",
    window_size=(400, 220),
    borderless=True,
    resizable=False,
    allow_high_dpi=False,
)


def login() -> bool:
    """显示登录窗口"""
    login_window = fantas.Window(login_window_config)

    linear_gradient_background = fantas.LinearGradientLabel(
        fantas.Rect((0, 0), login_window.size),
        color.LINEAR_GRADIENT_COLORS[0],
        color.LINEAR_GRADIENT_COLORS[1],
        (0, 0),
        login_window.size,
    )
    login_window.append(linear_gradient_background)

    title_text_style = fantas.TextStyle(
        font=fantas.fonts.DEFAULTSYSFONT,
        size=24,
        fgcolor=color.WHITE,
    )
    title_text = fantas.Text(
        "Fantas元件仓储管理器",
        fantas.Rect(0, 10, login_window.size[0], 50),
        text_style=title_text_style,
        align_mode=fantas.AlignMode.CENTER,
    )
    title_text_shadow = fantas.Text(
        title_text.text,
        title_text.rect.move(2, 2),
        text_style=title_text_style.copy(),
        align_mode=title_text.align_mode,
    )
    title_text_shadow.text_style.fgcolor = color.GRAY
    linear_gradient_background.append(title_text_shadow)
    linear_gradient_background.append(title_text)

    normal_text_style = title_text_style.copy()
    normal_text_style.size = 20

    info_text = fantas.Text(
        f"服务器地址：{server.HTTP_HOST}\n服务器端口：{server.HTTP_PORT}",
        fantas.Rect(0, title_text.rect.bottom, login_window.size[0], 60),
        text_style=normal_text_style,
        align_mode=fantas.AlignMode.CENTER,
    )
    info_text_shadow = fantas.Text(
        info_text.text,
        info_text.rect.move(2, 2),
        text_style=normal_text_style.copy(),
        align_mode=info_text.align_mode,
    )
    info_text_shadow.text_style.fgcolor = color.GRAY
    linear_gradient_background.append(info_text_shadow)
    linear_gradient_background.append(info_text)

    login_button_style = fantas.LabelStyle(
        bgcolor=None,
        fgcolor=color.WHITE,
        border_width=2,
        border_radius=12,
    )
    login_button = fantas.TextLabel(
        fantas.Rect(100, info_text.rect.bottom + 20, 200, 50),
        "登录",
        text_style=title_text_style,
        label_style=login_button_style,
        align_mode=fantas.AlignMode.CENTER,
        box_mode=fantas.BoxMode.INOUTSIDE,
    )
    linear_gradient_background.append(login_button)

    login_flag = False

    def on_login_click(event: fantas.Event) -> bool:
        nonlocal login_flag
        login_button.text = "正在验证..."
        if event.ui is login_button:
            if server.verify_token():
                login_button.text = "验证成功！"
                login_window.running = False
                login_flag = True
            else:
                login_button.text = "验证失败"
        return True

    login_window.add_event_listener(
        fantas.MOUSECLICKED, login_button, False, on_login_click
    )

    def on_enter_login_button(event: fantas.Event) -> bool:
        if event.ui is login_button:
            login_button.label_style.border_width = 4
            login_button.offset = (0, -2)
        return True

    login_window.add_event_listener(
        fantas.MOUSEENTERED, login_button, False, on_enter_login_button
    )

    def on_leave_login_button(event: fantas.Event) -> bool:
        if event.ui is login_button:
            login_button.label_style.border_width = 2
            login_button.offset = (0, 0)
        return True

    login_window.add_event_listener(
        fantas.MOUSELEAVED, login_button, False, on_leave_login_button
    )

    small_text_style = normal_text_style.copy()
    small_text_style.size = 12

    author_text = fantas.Text(
        "MIT License Fantastair@2026",
        fantas.Rect(0, login_window.size[1] - 20, login_window.size[0], 20),
        text_style=small_text_style,
        align_mode=fantas.AlignMode.BOTTOMRIGHT,
        offset=(-10, 0),
    )
    linear_gradient_background.append(author_text)

    login_window.mainloop()

    return login_flag
