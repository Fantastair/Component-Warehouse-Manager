""" 前端入口 """

import sys

import fantas

import login_window

if not login_window.login():
    sys.exit(0)

window_config = fantas.WindowConfig(
    title="Fantas元件仓储管理器",
    window_size=(1280, 720),
    resizable=True,
)

window = fantas.Window(window_config)

window.mainloop()
