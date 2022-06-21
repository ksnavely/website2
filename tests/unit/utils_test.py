"""
_utils_tests_

Unit tests coverage for website.utils.
"""
import unittest
from unittest import mock

import arrow

from website.server import utils


class UtilsTests(unittest.TestCase):
    """
    Tests for utility functions.
    """

    @mock.patch("arrow.now")
    def archive_dates_test(self, m_now):
        """
        Check the archive dates calculation functionality.
        """
        faux_now = arrow.get("2017-01-29T09:11:17.713880-05:00")
        m_now.return_value = faux_now

        expected = [
            ("2016", "03", "March"),
            ("2016", "04", "April"),
            ("2016", "05", "May"),
            ("2016", "06", "June"),
            ("2016", "07", "July"),
            ("2016", "08", "August"),
            ("2016", "09", "September"),
            ("2016", "10", "October"),
            ("2016", "11", "November"),
            ("2016", "12", "December"),
            ("2017", "01", "January"),
        ]
        self.assertEqual(expected, utils.archive_dates())
