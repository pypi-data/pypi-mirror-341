import unittest

from pgmpy import config


class TestConfig(unittest.TestCase):
    def test_defaults(self):
        self.assertEqual(config.BACKEND, "numpy")
        self.assertEqual(config.get_backend(), "numpy")

        self.assertEqual(config.DTYPE, "float64")
        self.assertEqual(config.get_dtype(), "float64")

        self.assertEqual(config.DEVICE, None)
        self.assertEqual(config.get_device(), None)

        self.assertEqual(config.SHOW_PROGRESS, True)
        self.assertEqual(config.get_show_progress(), True)

    def test_no_progress(self):
        config.set_show_progress(show_progress=False)

        self.assertEqual(config.BACKEND, "numpy")
        self.assertEqual(config.get_backend(), "numpy")

        self.assertEqual(config.DTYPE, "float64")
        self.assertEqual(config.get_dtype(), "float64")

        self.assertEqual(config.DEVICE, None)
        self.assertEqual(config.get_device(), None)

        self.assertEqual(config.SHOW_PROGRESS, False)
        self.assertEqual(config.get_show_progress(), False)

    def tearDown(self):
        config.set_backend("numpy")
        config.set_show_progress(show_progress=True)
