class SmoothTransitionState:
    def __init__(self, x_src: int, x_dst: int, y_src: int, y_dst: int, steps: int):
        self.steps_total = steps
        self.current_step = 0
        self.x_src = x_src
        self.x_dst = x_dst
        self.y_src = y_src
        self.y_dst = y_dst
        self.x_current = x_src
        self.y_current = y_src

    def next_step(self):
        if not self.is_done():
            self.current_step = self.current_step + 1
        self.x_current = int(self.interpolate(self.x_src, self.x_dst))
        self.y_current = int(self.interpolate(self.y_src, self.y_dst))
        return self.x_current, self.y_current

    def interpolate(self, src, dst):
        if self.current_step == 0:
            return src
        if self.current_step == self.steps_total:
            return dst
        delta = dst - src
        return src + (self.current_step / self.steps_total) * delta

    def is_done(self):
        return self.current_step >= self.steps_total