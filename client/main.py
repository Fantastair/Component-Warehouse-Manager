""" 前端入口 """

import sys

import fantas

import color
import login_window

if not login_window.login():
    sys.exit(0)

window_config = fantas.WindowConfig(
    title="Fantas元件仓储管理器",
    window_size=(1280, 720),
    resizable=True,
    allow_high_dpi=False,
)

window = fantas.Window(window_config)

linear_gradient = fantas.LinearGradientLabel(
    fantas.Rect((0, 0), window.size),
    color.SPOT_PALETTE[0],
    color.SPOT_PALETTE[-1],
    start_pos=(0, 0),
    end_pos=window.size,
)
window.append(linear_gradient)


def redraw_background(_: fantas.Event) -> bool:
    """重绘背景"""
    linear_gradient.rect.size = window.size
    linear_gradient.start_pos = (0, 0)
    linear_gradient.end_pos = window.size
    linear_gradient.mark_dirty()
    return True


window.add_event_listener(
    fantas.WINDOWRESIZED, window.root_ui, False, redraw_background
)

window.mainloop()
