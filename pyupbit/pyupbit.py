# -*- coding: utf-8 -*-
import json
import time

import requests
import jwt
import logging
from urllib.parse import urlencode

class PyUpbit():
    """
    Upbit API document
    https://docs.upbit.com
    """
    BASE_URL = 'https://api.upbit.com/v1'

    def __init__(self, access_key=None, secret_key=None):

        self.access_key = access_key
        self.secret_key = secret_key
        self.markets = self._load_markets()

    ###################
    ## QUOTATION API ##
    ###################

    def get_market_all(self):
        '''
        마켓 코드 조회
        https://api.upbit.com/v1/market/all

        Args:
            None

        Returns:
            json array
        '''
        URL = PyUpbit.BASE_URL  + '/market/all'
        return self._get(URL)
    
    def get_minutes_candles(self, unit, market, to=None, count=None):
        '''
        Minute 캔들
        https://docs.upbit.com/v1.0/reference#%EB%B6%84minute-%EC%BA%94%EB%93%A4-1
        
        Args:
            unit (int): 분 단위. 가능한 값 : 1, 3, 5, 15, 10, 30, 60, 240 
            market (str): 마켓 코드 (ex. KRW-BTC, BTC-BCC) 
            to (str): 마지막 캔들 시각(exclusive). 포맷: yyyy-MM-dd'T'HH:mm:ssXXX
            count (int): 캔들 개수(최대 200개까지 요청 가능)

        Returns:
            json array
        '''
        URL = PyUpbit.BASE_URL + '/candles/minutes/%s' % str(unit)
        if unit not in [1, 3, 5, 10, 15, 30, 60, 240]:
            logging.error('invalid unit: %s' % str(unit))
            raise Exception('invalid unit: %s' % str(unit))
        if market not in self.markets:
            logging.error('invalid market: %s' % market)
            raise Exception('invalid market: %s' % market)

        params = {'market': market}
        if to is not None:
            params['to'] = to
        if count is not None:
            params['count'] = count
        return self._get(URL, params=params)
    
    def get_days_candles(self, market, to=None, count=None, convertingPriceUnit=None):
        '''
        Day 캔들
        https://docs.upbit.com/v1.0/reference#%EC%9D%BCday-%EC%BA%94%EB%93%A4-1

        Args:
            market (str): 마켓 코드 (ex. KRW-BTC, BTC-BCC)
            to (str): 마지막 캔들 시각 (exclusive). 포맷 : yyyy-MM-dd'T'HH:mm:ssXXX. 비워서 요청시 가장 최근 캔들
            count (int): 캔들 개수
            convertingPriceUnit (str): 종가 환산 화폐 단위 (생략 가능, KRW로 명시할 시 원화 환산 가격을 반환.)

        Returns:
            json array
        '''
        URL = PyUpbit.BASE_URL + '/candles/days'
        if market not in self.markets:
            logging.error('invalid market: %s' % market)
            raise Exception('invalid market: %s' % market)

        params = {'market':market}
        if to is not None:
            params['to'] = to
        if count is not None:
            params['count'] = count
        return self._get(URL, params=params)

    
    def get_weeks_candles(self, market, to=None, count=None):
        
        '''
        Week 캔들
        https://docs.upbit.com/v1.0/reference#%EC%A3%BCweek-%EC%BA%94%EB%93%A4-1
        
        Args:
            market (str): 마켓 코드 (ex. KRW-BTC, BTC-BCC)
            to (str): 마지막 캔들 시각 (exclusive). 포맷 : yyyy-MM-dd'T'HH:mm:ssXXX. 비워서 요청시 가장 최근 캔들
            count (int): 캔들 개수
        
        Returns:
            json array
        '''
        URL = PyUpbit.BASE_URL + '/candles/weeks'

        if market not in self.markets:
            logging.error('invalid market: %s' % market)
            raise Exception('invalid market: %s' % market)
        
        params = {'market': market}
        if to is not None:
            params['to'] = to
        if count is not None:
            params['count'] = count
        return self._get(URL, params=params)


    def get_months_candles(self, market, to=None, count=None):
    
        '''
        Month 캔들
        https://docs.upbit.com/v1.0/reference#%EC%9B%94month-%EC%BA%94%EB%93%A4-1

        Args:
            market (str): 마켓 코드 (ex. KRW-BTC, BTC-BCC)
            to (str): 마지막 캔들 시각 (exclusive). 포맷 : yyyy-MM-dd'T'HH:mm:ssXXX. 비워서 요청시 가장 최근 캔들
            count (int): 캔들 개수

        Returns:
            json array
        '''
        URL = PyUpbit.BASE_URL + '/candles/months'
        if market not in self.markets:
            logging.error('invalid market: %s' % market)
            raise Exception('invalid market: %s' % market)
        
        params = {'market': market}
        if to is not None:
            params['to'] = to
        if count is not None:
            params['count'] = count
        return self._get(URL, params=params)


    def get_trades_ticks(self, market, to=None, count=None, cursor=None):
        '''
        당일 채결 내역
        https://docs.upbit.com/v1.0/reference#%EB%8B%B9%EC%9D%BC-%EC%B2%B4%EA%B2%B0-%EB%82%B4%EC%97%AD
        
        Args:
            market (str): 마켓 코드 (ex. KRW-BTC, BTC-BCC)
            to (str): 마지막 체결 시각. 형식 : [HHmmss 또는 HH:mm:ss]. 비워서 요청시 가장 최근 데이터
            count (int): 채결 개수
            cursor (str): 페이지네이션 커서 (sequentialId)

        Returns:
            json array
        '''
        URL = PyUpbit.BASE_URL + '/trades/ticks'
        if market not in self.markets:
            logging.error('invalid market: %s' % market)
            raise Exception('invalid market: %s' % market)
        
        params = {'market': market}
        if to is not None:
            params['to'] = to
        if count is not None:
            params['count'] = count
        if cursor is not None:
            params['cursor'] = cursor
        return self._get(URL, params=params)


    def get_ticker(self, markets):

        '''
        현재가 정보
        요청 당시 종목의 스냅샷을 반환한다.
        https://docs.upbit.com/v1.0/reference#ticker%ED%98%84%EC%9E%AC%EA%B0%80-%EB%82%B4%EC%97%AD
        
        Args:
            markets (str[]): 마켓 코드 리스트 (ex. KRW-BTC, BTC-BCC)
       
        Returns:
            json array
        '''
        URL = PyUpbit.BASE_URL + '/ticker'

        if not isinstance(markets, list):
            logging.error('invalid parameter: markets should be list')
            raise Exception('invalid parameter: markets should be list')

        if len(markets) == 0:
            logging.error('invalid parameter: no markets')
            raise Exception('invalid parameter: no markets')

        for market in markets:
            if market not in self.markets:
                logging.error('invalid market: %s' % market)
                raise Exception('invalid market: %s' % market)


        markets_data = ', '.join(markets)
        params = {'markets': markets_data}
        return self._get(URL, params=params)

    
    ############################################################################################

    def _get(self, URL, headers=None, data=None, params=None):
        
        response = requests.get(URL, headers=headers, data=data, params=params)

        if response.status_code not in [200, 201]:
            logging.error('get(%s) failed' % (url, response.status_code))
            
            if response.text is not None:
                logging.error('response : %s' % response.text)
                raise Exception('requests.get() failed(%s)' % response.text)

            raise Exception('requests.get() failed(status_code:%d)' % response.status_code)
    
        return json.loads(response.text)

    def _load_markets(self):
        
        try:
            market_all = self.get_market_all()
            
            if market_all is None:
                logging.error('No possible market')
                return
            markets = [market['market'] for market in market_all]
            
            return markets
        
        except Exception as e:
            logging.error(e)
            raise Exception(e)
