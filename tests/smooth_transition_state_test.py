import unittest

from smooth_transition_state import SmoothTransitionState


class SmoothTransitionStateTest(unittest.TestCase):

    def test_transition(self):
        sts = SmoothTransitionState(10, 20, 20, 40, 10)
        x, y = sts.next_step()
        self.assertEqual(11, x, "x1")
        self.assertEqual(22, y, "y1")
        x, y = sts.next_step()
        x, y = sts.next_step()
        x, y = sts.next_step()
        x, y = sts.next_step()
        self.assertEqual(15, x, "x1")
        self.assertEqual(30, y, "y1")
        x, y = sts.next_step()
        x, y = sts.next_step()
        x, y = sts.next_step()
        x, y = sts.next_step()
        self.assertFalse(sts.is_done())
        x, y = sts.next_step()
        self.assertTrue(sts.is_done())
        self.assertEqual(20, x, "x1")
        self.assertEqual(40, y, "y1")
        x, y = sts.next_step()
        self.assertTrue(sts.is_done())
        self.assertEqual(20, x, "x1")
        self.assertEqual(40, y, "y1")


if __name__ == '__main__':
    unittest.main()
