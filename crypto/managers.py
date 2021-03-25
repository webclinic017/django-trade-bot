import pytz
from datetime import date
from binance.client import Client
from binance.exceptions import *
from trade_bot.settings import BINANCE_SECRETKEY, BINANCE_KEY

from .symbols import SYMBOLS, TRADEABLE_SYMBOLS

LIMIT = 500

class BinanceManager():
    
    def __init__(self):
        super().__init__()
        client = Client(BINANCE_KEY, BINANCE_SECRETKEY)
        self.client = client
    
    def get_symbols(self):
        return SYMBOLS 
    def get_tradeable_symbols(self):
        return TRADEABLE_SYMBOLS 

    def get_coins_info(self):
        info = self.client.get_account_status()
        return info

    def get_exchange_info(self):
        '''Exchange information and coin list'''
        info = self.client.get_exchange_info()
        
        currStamp = (int(info['serverTime']) / 1000) # milliseconds to seconds
        info['serverTime'] = date.fromtimestamp(currStamp) # django timestamp
        return info

    def create_deposit(self, asset: str="ETH", email: str=None):
        '''Create deposit address for trading account'''
        
        if email:
            address = self.client.get_subaccount_deposit_address(email=email, coin=asset)
            return address

        address = self.client.get_deposit_address(asset=asset)

        return address

    def get_balance(self):
        self.client.get_asset_balance()

    def create_withdraw(self, asset: str="ETH", address: str=None, amount: float=0.1):
        '''Create withdraw endpoint for given coin, address & amount
        
        :param asset required
        :type asset str
        
        '''
        try:
            result = self.client.withdraw(
                asset=asset,
                address=address,
                amount=amount)
        except BinanceWithdrawException as e:
            print(e)
            return {'error': e.message}
        except BinanceAPIException as e:
            print(e)
            return {'error': e}

        return result

    def get_withdrawal_history(self):
        '''Get complete history of withdrawings from trading account'''

        withdraws = self.client.get_withdraw_history()
        return withdraws

    def get_order_history(self, asset: str=None):
        ''' '''
        orders = self.client.get_order_book(asset)
        return orders

    def get_sub_accounts(self, email:str=None, startTime: int=None, endTime: int=None):
        '''
            View sub trading accounts by email and by time.
            :param email optional
            :type email str | Email for accounts

            :param startTime: optional
            :type startTime: int

            :param endTime: optional
            :type endTime: int
        '''
        sub_accounts = self.client.get_sub_account_list()
        return sub_accounts
        
    def get_subaccount_withdraws(self, email: str, startTime: int=None, endTime: int=None):
        '''View sub account transfer history

            :param email required
            :type email str | Email for accounts

        '''
        
        transfers = self.client.get_sub_account_transfer_history(email=email, startTime=startTime, endTime=endTime)

        return transfers
    def get_subaccount_deposits(self, email: str):
        '''
            View sub trading account deposit history by email
            :param email required
            :type email str | Email for sub accounts

        '''
        try:
            self.client.create_isolated_margin_account()

            deposits = self.client.get_subaccount_deposit_history(email=email)
        except BinanceAPIException as e:
            return {'error': e}
        
        return deposits

    
    def get_prices(self):
        '''Create trading prices of all coins'''
        #address = self.client.get_symbol_info("BTCUSDT")
        tickers = self.client.get_all_tickers()
        return tickers

    def get_kline_history(self, coin: str='BNBBTC', date: str="1 day ago UTC", end_date: str=None):
        '''get analytical KLine data from BTC or otherwise specified coin'''

        klines = self.client.get_historical_klines(coin, Client.KLINE_INTERVAL_1MINUTE, date, limit=LIMIT)
        return klines
