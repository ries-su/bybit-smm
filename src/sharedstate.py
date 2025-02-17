import asyncio
import numpy as np
import yaml
from numpy_ringbuffer import RingBuffer

from src.exchanges.binance.websockets.handlers.orderbook import OrderBookBinance
from src.exchanges.bybit.websockets.handlers.orderbook import OrderBookBybit
from collections import deque


class SharedState:
    CONFIG_DIR = ""  # Put the bybit.yaml file directory here
    PARAM_DIR = ""  # Put the parameters.yaml file directory here

    def __init__(self) -> None:
        self.load_config()
        self.load_initial_settings()

        # Binance attributes
        self.binance_trades = RingBuffer(capacity=1000, dtype=(float, 4))
        self.binance_bba = np.zeros((2, 2))  # [Bid[P, Q], Ask[P, Q]]
        self.binance_book = OrderBookBinance()
        self.binance_last_price = 0.0

        # Bybit attributes
        self.bybit_trades = RingBuffer(capacity=1000, dtype=(float, 4))
        self.bybit_bba = np.zeros((2, 2))  # [Bid[P, Q], Ask[P, Q]]
        self.bybit_book = OrderBookBybit()
        self.bybit_mark_price = 0.0
        self.bybit_klines = deque(maxlen=100)
        # Other attributes
        self.current_orders = {}
        self.execution_feed = deque(maxlen=100)
        self.volatility_value = 0.0
        self.alpha_value = 0.0
        self.inventory_delta = 0.0

    def load_config(self):
        with open(self.CONFIG_DIR, "r") as f:
            config = yaml.safe_load(f)
            self.api_key = config["api_key"]
            self.api_secret = config["api_secret"]

    def load_settings(self, settings):
        self.binance_symbol = settings["binance_symbol"]
        self.bybit_symbol = settings["bybit_symbol"]
        self.binance_tick_size = float(settings["binance_tick_size"])
        self.binance_lot_size = float(settings["binance_lot_size"])
        self.bybit_tick_size = float(settings["bybit_tick_size"])
        self.bybit_lot_size = float(settings["bybit_lot_size"])
        self.account_size = float(settings["account_size"])
        self.primary_data_feed = str(settings["primary_data_feed"]).upper()
        self.buffer = float(settings["buffer"]) * self.bybit_tick_size
        self.bb_length = int(settings["bollinger_band_length"])
        self.bb_std = int(settings["bollinger_band_std"])
        self.quote_offset = float(settings["quote_offset"])
        self.size_offset = float(settings["size_offset"])
        self.volatility_offset = float(settings["volatility_offset"])
        self.target_spread = float(settings["target_spread"])
        self.num_orders = int(settings["number_of_orders"])
        self.minimum_order_size = float(settings["minimum_order_size"])
        self.maximum_order_size = float(settings["maximum_order_size"])
        self.inventory_extreme = float(settings["inventory_extreme"])

    def load_initial_settings(self):
        with open(self.PARAM_DIR, "r") as f:
            settings = yaml.safe_load(f)
            self.load_settings(settings)

    async def refresh_parameters(self):
        while True:
            with open(self.PARAM_DIR, "r") as f:
                settings = yaml.safe_load(f)
                self.load_settings(settings)
            await asyncio.sleep(60)

    @property
    def binance_mid_price(self):
        return self.calculate_mid_price(self.binance_bba)

    @property
    def binance_weighted_mid_price(self):
        return self.calculate_weighted_mid_price(self.binance_bba)

    @property
    def bybit_mid_price(self):
        return self.calculate_mid_price(self.bybit_bba)

    @property
    def bybit_weighted_mid_price(self):
        return self.calculate_weighted_mid_price(self.bybit_bba)

    @staticmethod
    def calculate_mid_price(bba):
        best_bid, best_ask = bba[0][0], bba[1][0]
        return (best_ask - best_bid) + best_bid

    @staticmethod
    def calculate_weighted_mid_price(bba):
        imb = bba[0][1] / (bba[0][1] + bba[1][1])
        return bba[1][0] * imb + bba[0][0] * (1 - imb)
