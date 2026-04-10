""" 分割线UI """

import fantas

import color

class SplitLine(fantas.Label):
    def __init__(self, rect: fantas.Rect, axis: str, boundary: list[int]):
        style = fantas.LabelStyle(
            bgcolor=color.WHITE,
        )
        super().__init__(rect, style)
        self.axis = axis
        self.boundary = boundary
        self.dragging = False
        self.mouse_hovered = False
        self.drag_offset = 0
        self.dragged_callback = None
        self.append(
            fantas.Label(
                fantas.Rect(
                    0,
                    0,
                    (self.rect.width // 2 - 1) if axis == "v" else (self.rect.width // 10),
                    (self.rect.height // 2 - 1) if axis == "h" else (self.rect.height // 10)
                ),
                fantas.LabelStyle(
                    bgcolor=color.GRAY,
                    border_radius=min(self.rect.width, self.rect.height) // 4,
                )
            )
        )
        self.children[0].rect.center = (self.rect.width // 2, self.rect.height // 2)

    def on_mouse_entered(self, event: fantas.Event) -> bool:
        if event.ui is self:
            self.mouse_hovered = True
            if self.axis == "v":
                fantas.set_cursor("-")
            else:
                fantas.set_cursor("|")
            return True
        return False

    def on_mouse_leaved(self, event: fantas.Event) -> bool:
        if event.ui is self:
            self.mouse_hovered = False
            if not self.dragging:
                fantas.set_cursor("^")
            return True
        return False
    
    def on_mouse_button_down(self, event: fantas.Event) -> bool:
        self.dragging = True
        self.label_style.border_width = 2
        if self.axis == "v":
            self.label_style.border_radius = self.rect.width // 2
            self.drag_offset = event.pos[0] - self.rect.left
        else:
            self.label_style.border_radius = self.rect.height // 2
            self.drag_offset = event.pos[1] - self.rect.top
        return True
    
    def on_mouse_button_up(self, event: fantas.Event) -> bool:
        self.dragging = False
        self.label_style.border_width = 0
        self.label_style.border_radius = 0
        if not self.mouse_hovered:
            fantas.set_cursor("^")
        return True
    
    def on_mouse_motion(self, event: fantas.Event) -> bool:
        if self.dragging:
            if self.axis == "v":
                new_left = event.pos[0] - self.drag_offset
                new_left = max(self.boundary[0], min(new_left, self.boundary[1] - self.rect.width))
                self.rect.left = new_left
            else:
                new_top = event.pos[1] - self.drag_offset
                new_top = max(self.boundary[0], min(new_top, self.boundary[1] - self.rect.height))
                self.rect.top = new_top
            if self.dragged_callback is not None:
                self.dragged_callback(self.rect)
            return True
        return False
    
    def add_event_listeners(self, window: fantas.Window) -> None:
        window.add_event_listener(fantas.MOUSEENTERED, self, False, self.on_mouse_entered)
        window.add_event_listener(fantas.MOUSELEAVED, self, False, self.on_mouse_leaved)
        window.add_event_listener(fantas.MOUSEBUTTONDOWN, self, False, self.on_mouse_button_down)
        window.add_event_listener(fantas.MOUSEBUTTONUP, self.father, False, self.on_mouse_button_up)
        window.add_event_listener(fantas.MOUSEMOTION, self.father, False, self.on_mouse_motion)
