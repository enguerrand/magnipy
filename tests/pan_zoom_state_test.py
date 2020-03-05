import unittest

from pan_zoom_state import PanZoomState


class PanZoomStateTest(unittest.TestCase):
    def test_initial_zoom(self):
        pzs = PanZoomState(640, 480, 10, 1920, 1080)
        self.assertEqual(1, pzs.min_zoom_level)
        self.assertEqual(pzs.min_zoom_level, pzs.zoom_level)

    def test_initial_pos_zoomed(self):
        pzs = PanZoomState(640, 480, 10, 1280, 960)
        self.assertEqual(320, pzs.pos_x, "wrong x")
        self.assertEqual(240, pzs.pos_y, "wrong y")

    def test_min_zoom(self):
        pzs = PanZoomState(640, 480, 10, 1920, 1080)
        pzs.zoom(-1.1)
        self.assertEqual(pzs.min_zoom_level, pzs.zoom_level)

    def test_max_zoom(self):
        pzs = PanZoomState(640, 480, 10, 1920, 1080)
        pzs.zoom(20)
        self.assertEqual(10, pzs.zoom_level)

    def test_pan_unzoomed(self):
        pzs = PanZoomState(640, 480, 10, 640, 640)
        pzs.pan(100, 100)
        self.assertLessEqual(320, pzs.pos_x, "wrong x")
        self.assertLessEqual(240, pzs.pos_y, "wrong y")

    def test_pan(self):
        pzs = PanZoomState(640, 480, 10, 1280, 960)
        pzs.zoom(1)
        pzs.pan(40, 20)
        self.assertEqual(340, pzs.pos_x, "wrong x")
        self.assertEqual(250, pzs.pos_y, "wrong y")

    def test_pan_beyond_right_limit(self):
        pzs = PanZoomState(640, 480, 10, 1280, 960)
        pzs.zoom(1)
        pzs.pan(330, 0)
        self.assertEqual(480, pzs.pos_x, "wrong x")
        self.assertEqual(240, pzs.pos_y, "wrong y")

    def test_pan_beyond_left_limit(self):
        pzs = PanZoomState(640, 480, 10, 1280, 960)
        pzs.zoom(1)
        pzs.pan(-330, 0)
        self.assertEqual(160, pzs.pos_x, "wrong x")
        self.assertEqual(240, pzs.pos_y, "wrong y")

    def test_pan_beyond_bottom_limit(self):
        pzs = PanZoomState(640, 480, 10, 1280, 960)
        pzs.zoom(1)
        pzs.pan(0, 250)
        self.assertEqual(320, pzs.pos_x, "wrong x")
        self.assertEqual(360, pzs.pos_y, "wrong y")

    def test_pan_beyond_top_limit(self):
        pzs = PanZoomState(640, 480, 10, 1280, 960)
        pzs.zoom(1)
        pzs.pan(0, -250)
        self.assertEqual(320, pzs.pos_x, "wrong x")
        self.assertEqual(120, pzs.pos_y, "wrong y")


if __name__ == '__main__':
    unittest.main()
