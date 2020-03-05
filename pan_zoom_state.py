from common_equality_mixin import CommonEqualityMixin


class Bounds:
    def __init__(self, dx: int, dy: int, width: int, height: int):
        self.dx = dx
        self.dy = dy
        self.width = width
        self.height = height


class PanZoomState(CommonEqualityMixin):
    def __init__(
            self,
            width: int,
            height: int,
            max_zoom_level: int,
            display_width: int,
            display_height: int
    ):
        self.orig_width = width
        self.orig_height = height
        self.display_width = display_width
        self.display_height = display_height
        self.aspect_ratio = display_width / display_height
        self.min_zoom_level = 1
        self.max_zoom_level = max_zoom_level
        self.zoom_level = self.min_zoom_level
        self.pos_x = int(width / 2)
        self.pos_y = int(height / 2)

    def zoom(self, delta):
        self.zoom_level = self.zoom_level + delta
        if self.zoom_level > self.max_zoom_level:
            self.zoom_level = self.max_zoom_level
        elif self.zoom_level < self.min_zoom_level:
            self.zoom_level = self.min_zoom_level
        self.ensure_full_overlap()

    def pan(self, delta_x=0, delta_y=0):
        self.pos_x = self.pos_x + int(delta_x/self.zoom_level)
        self.pos_y = self.pos_y + int(delta_y/self.zoom_level)
        self.ensure_full_overlap()

    def compute_bounds(self) -> Bounds:
        width = self.orig_width / self.zoom_level
        height = self.orig_height / self.zoom_level
        zoomed_aspect_ratio = width / height
        if zoomed_aspect_ratio > self.aspect_ratio:
            width = int(width * zoomed_aspect_ratio / self.aspect_ratio)
        elif zoomed_aspect_ratio < self.aspect_ratio:
            height = int(height * zoomed_aspect_ratio / self.aspect_ratio)
        dx = self.pos_x - int(width / 2)
        dy = self.pos_y - int(height / 2)
        return Bounds(dx, dy, int(width), int(height))

    def ensure_full_overlap(self):
        bounds = self.compute_bounds()
        if bounds.dx < 0:
            self.pos_x = int(bounds.width / 2)
        if bounds.dy < 0:
            self.pos_y = int(bounds.height / 2)
        if bounds.dx + bounds.width > self.orig_width:
            self.pos_x = self.orig_width - int(bounds.width / 2)
        if bounds.dy + bounds.height > self.orig_height:
            self.pos_y = self.orig_height - int(bounds.height / 2)
