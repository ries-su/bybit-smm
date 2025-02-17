Bybit Simple Market Maker
===================

This is a sample market making bot for [Bybit](https://www.bybit.com/en-US/).


Getting Started
---------------

1. Assuming you already have a Bybit account, generate API keys and secrets using [this guide](https://learn.bybit.com/bybit-guide/how-to-create-a-bybit-api-key/)
2. Swap your key/secret into the config file found in /config/bybit.yaml/
3. Install all packages required by running 'pip install -r requirements.txt' 
4. Input the contract details in the parameters.yaml file (tick size/lot size) according to the symbol you want to make
5. Alter the spreads, order sizes, offsets (any setting in the .yaml file!) as you wish, even whilst the bot is live!

** Note, changing the primary data feed between Binance <-> Bybit will require a restart to the script **


Strategy Design/Overview
---------------

1. Prices from Bybit (and optionally Binance) are streamed into a common shared class
2. A market maker function generates quotes, with bias based on price based features
  * The price based feature (more can be added!) works on comparing a benchmark (fair) price to the current price
  * Prices and quantities are generated, with prices within a volatility range, and min/max quantity defined manually
  * The above is skewed using various features, leading to behaviour shown in examples below:
    * (Ex) If binance price is lower than then bybit price -> skew is negative -> asks are more concentrated near mid price than bids
    * (Ex) If binance price is higher than then bybit price -> skew is positive -> bids have more qty than asks
    * (Ex) If inventory is extremely long, quotes are killed on the long side to try neutralize the position
3. Orders are sent to the exchange
  

New upgrades
---------------

- Fast local orderbooks for both Binance & Bybit, useful for creating [orderbook based features](https://twitter.com/BeatzXBT/status/1680152557388197888)
- Highly abstracted code (add/remove features with ease)
- Access to Binance data feeds (LOB/Trades) 


Fixes/Improvements Required
---------------

- Sanity checks for market/private websockets and clients {High Priority}
- Simpler execution and order feed handlers (reworked for time-based and orderId based indexing) {Medium Priority}
- Customized rounding for [bid/ask](https://twitter.com/kursatcalk/status/1686685226028666880) {Low Priority}


Upcoming upgrades
---------------

- Optional TWAP to reduce inventory (alongside purging quotes)
- Improved inventory management system (reaching neutral position faster and cheaper)
- Avellaneda and Stoikov's basic market making model 

---------------

If you have any questions or suggestions regarding the repo, or just want to have a chat, my handles are below 👇🏼

Twitter: [@beatzXBT](https://twitter.com/BeatzXBT) | Discord: gamingbeatz
