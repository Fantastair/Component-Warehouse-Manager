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

split_line_1 = splitline.SplitLine(
    fantas.Rect(280, 0, 10, window.size[1]),
    axis="v",
    boundary=[200, window.size[0] // 2],
)
window.append(split_line_1)
split_line_1.add_event_listeners(window)


split_line_2 = splitline.SplitLine(
    fantas.Rect(
        split_line_1.rect.right, 200, window.size[0] - split_line_1.rect.right, 10
    ),
    axis="h",
    boundary=[100, window.size[1] - 100],
)
window.append(split_line_2)
split_line_2.add_event_listeners(window)


def split_line_1_dragged_callback(rect: fantas.Rect) -> None:
    """分割线被拖动时的回调，调整相关UI布局"""
    host_text.rect.width = rect.left - 20
    split_line_2.rect.left = rect.right
    split_line_2.rect.width = window.size[0] - split_line_2.rect.left
    split_line_2.drag_bar.rect.center = (
        split_line_2.rect.width // 2,
        split_line_2.rect.height // 2,
    )


split_line_1.dragged_callback = split_line_1_dragged_callback


host_text_style = fantas.TextStyle(
    font=fantas.fonts.DEFAULTSYSFONT,
    size=18,
    fgcolor=color.WHITE,
)
host_text = fantas.Text(
    f"服务器：{server.HTTP_HOST}:{server.HTTP_PORT}",
    fantas.Rect(10, 10, split_line_1.rect.left - 20, 60),
    text_style=host_text_style,
    align_mode=fantas.AlignMode.TOPLEFT,
)
window.append(host_text)

window.mainloop()
