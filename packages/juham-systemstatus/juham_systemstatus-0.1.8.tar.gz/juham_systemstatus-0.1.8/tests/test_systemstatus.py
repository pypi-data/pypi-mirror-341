import unittest

from juham_systemstatus.systemstatus import SystemStatus


class TestSystemstatus(unittest.TestCase):
    """Unit tests for `SystemStatus`."""

    def test_get_classid(self):
        """Assert that the meta-class driven class initialization works."""
        classid = SystemStatus.get_class_id()
        self.assertEqual("SystemStatus", classid)


if __name__ == "__main__":
    unittest.main()
