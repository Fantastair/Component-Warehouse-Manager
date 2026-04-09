""" 登录窗口模块 """

import fantas

import server

login_window_config = fantas.WindowConfig(
    title="登录 - Fantas元件仓储管理器",
    window_size=(400, 300),
    # borderless=True,
    resizable=False,
)

def login() -> bool:
    """ 显示登录窗口 """
    login_window = fantas.Window(login_window_config)
    login_window.mainloop()
