""" 前端入口 """

import sys
from pathlib import Path

import fantas

import color
import login_window

import server

CWD = Path(__file__).parent

fantas.fonts.load(CWD / "assets" / "fonts" / "iconfont.ttf")

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

host_text_style = fantas.TextStyle(
    font=fantas.fonts.DEFAULTSYSFONT,
    size=18,
    fgcolor=color.WHITE,
)
host_text = fantas.Text(
    f"服务器：{server.HTTP_HOST}:{server.HTTP_PORT}",
    fantas.Rect(10, 10, 300, 30),
    text_style=host_text_style,
    align_mode=fantas.AlignMode.CENTER,
)
host_text_shadow = fantas.Text(
    host_text.text,
    host_text.rect.move(2, 2),
    text_style=host_text_style.copy(),
    align_mode=host_text.align_mode,
)
host_text_shadow.text_style.fgcolor = color.GRAY
window.append(host_text_shadow)
window.append(host_text)

window.mainloop()
