import unittest
from unittest.mock import patch
import threading
import time
from autoport import log_event, check_port_status, open_port, close_port, scheduled_port

class TestAutoport(unittest.TestCase):
    def test_log_event(self):
        result = log_event("Test log")
        self.assertIsNone(result)

    @patch('subprocess.run')
    def test_check_port_status(self, mock_subprocess):
        mock_subprocess.return_value.stdout = "8080"
        self.assertTrue(check_port_status(8080))

    @patch('subprocess.run')
    def test_open_port(self, mock_subprocess):
        result = open_port(8080)
        self.assertIsNone(result)

    @patch('subprocess.run')
    def test_close_port(self, mock_subprocess):
        result = close_port(8080)
        self.assertIsNone(result)

    def test_performance(self):
        start_time = time.time()
        for port in range(8000, 8010):
            open_port(port)
            close_port(port)
        end_time = time.time()
        print(f"10 port işlemi toplam süre: {end_time - start_time:.2f} saniye")

if __name__ == '__main__':
    unittest.main()
