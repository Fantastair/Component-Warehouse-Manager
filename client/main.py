import fantas

import login_window

login_window.login()

window_config = fantas.WindowConfig(
    title="Fantas元件仓储管理器",
    window_size=(1280, 720),
    resizable=True,
)

window = fantas.Window(window_config)

window.mainloop()
