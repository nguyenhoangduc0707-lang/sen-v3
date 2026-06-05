import unittest
from unittest.mock import Mock, patch

from affiliate.fetcher import filter_campaigns, init_db, save_campaigns


class TestAffiliateFetcher(unittest.TestCase):
    def test_filter_campaigns(self):
        campaigns = [
            {"id": "1", "commission": 10, "category": "thời trang"},
            {"id": "2", "commission": 3, "category": "thời trang"},
            {"id": "3", "commission": 8, "category": "sách"},
        ]
        filtered = filter_campaigns(campaigns)
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0]["id"], "1")

    @patch("affiliate.fetcher.psycopg2.connect")
    def test_init_db(self, mock_connect):
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor

        init_db()

        mock_cursor.execute.assert_called_once()
        mock_conn.commit.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()

    @patch("affiliate.fetcher.execute_values")
    @patch("affiliate.fetcher.psycopg2.connect")
    def test_save_campaigns(self, mock_connect, mock_execute_values):
        mock_conn = Mock()
        mock_cursor = Mock()
        mock_connect.return_value = mock_conn
        mock_conn.cursor.return_value = mock_cursor
        campaigns = [{"id": "1", "name": "Test", "commission": 10, "category": "thời trang"}]

        save_campaigns(campaigns)

        mock_execute_values.assert_called_once()
        mock_conn.commit.assert_called_once()
        mock_cursor.close.assert_called_once()
        mock_conn.close.assert_called_once()


if __name__ == "__main__":
    unittest.main()
