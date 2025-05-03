import sys
import os

# Add the root path (one level up from 'backtester') to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import time
import unittest
from data_collector import stream


class TestPriceStream(unittest.TestCase):
    def test_price_window_populates(self):
        stream.start_price_stream()
        time.sleep(10)  # Wait a few seconds for some prices to stream in

        self.assertGreater(
            len(stream.price_window), 0, "No prices received in price_window"
        )
        print(f"Received {len(stream.price_window)} prices")


if __name__ == "__main__":
    unittest.main()
