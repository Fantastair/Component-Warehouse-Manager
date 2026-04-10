""" 前端入口 """

import sys
from pathlib import Path

import fantas

import color
import login_window
import splitline

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

split_line = splitline.SplitLine(
    fantas.Rect(280, 0, 10, window.size[1]),
    axis="v",
    boundary=[200, window.size[0] - 200],
)
window.append(split_line)
split_line.add_event_listeners(window)


def split_line_dragged_callback(rect: fantas.Rect) -> None:
    """ 分割线被拖动时的回调，调整相关UI布局 """
    host_text.rect.width = rect.left - 20
    host_text_shadow.rect.width = rect.left - 20
split_line.dragged_callback = split_line_dragged_callback


host_text_style = fantas.TextStyle(
    font=fantas.fonts.DEFAULTSYSFONT,
    size=18,
    fgcolor=color.WHITE,
)
host_text = fantas.Text(
    f"服务器：{server.HTTP_HOST}:{server.HTTP_PORT}",
    fantas.Rect(10, 10, split_line.rect.left - 20, 60),
    text_style=host_text_style,
    align_mode=fantas.AlignMode.TOPLEFT,
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
