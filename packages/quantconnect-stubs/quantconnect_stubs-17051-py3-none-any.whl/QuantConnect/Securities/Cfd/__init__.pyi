from typing import overload
from enum import Enum
import typing

import QuantConnect
import QuantConnect.Data
import QuantConnect.Securities
import QuantConnect.Securities.Cfd


class Cfd(QuantConnect.Securities.Security):
    """CFD Security Object Implementation for CFD Assets"""

    @property
    def contract_multiplier(self) -> float:
        """Gets the contract multiplier for this CFD security"""
        ...

    @property
    def minimum_price_variation(self) -> float:
        """Gets the minimum price variation for this CFD security"""
        ...

    @overload
    def __init__(self, exchangeHours: QuantConnect.Securities.SecurityExchangeHours, quoteCurrency: QuantConnect.Securities.Cash, config: QuantConnect.Data.SubscriptionDataConfig, symbolProperties: QuantConnect.Securities.SymbolProperties, currencyConverter: QuantConnect.Securities.ICurrencyConverter, registeredTypes: QuantConnect.Securities.IRegisteredSecurityDataTypesProvider) -> None:
        """
        Constructor for the CFD security
        
        :param exchangeHours: Defines the hours this exchange is open
        :param quoteCurrency: The cash object that represent the quote currency
        :param config: The subscription configuration for this security
        :param symbolProperties: The symbol properties for this security
        :param currencyConverter: Currency converter used to convert CashAmount instances into units of the account currency
        :param registeredTypes: Provides all data types registered in the algorithm
        """
        ...

    @overload
    def __init__(self, symbol: typing.Union[QuantConnect.Symbol, str], exchangeHours: QuantConnect.Securities.SecurityExchangeHours, quoteCurrency: QuantConnect.Securities.Cash, symbolProperties: QuantConnect.Securities.SymbolProperties, currencyConverter: QuantConnect.Securities.ICurrencyConverter, registeredTypes: QuantConnect.Securities.IRegisteredSecurityDataTypesProvider, securityCache: QuantConnect.Securities.SecurityCache) -> None:
        """
        Constructor for the CFD security
        
        :param symbol: The security's symbol
        :param exchangeHours: Defines the hours this exchange is open
        :param quoteCurrency: The cash object that represent the quote currency
        :param symbolProperties: The symbol properties for this security
        :param currencyConverter: Currency converter used to convert CashAmount instances into units of the account currency
        :param registeredTypes: Provides all data types registered in the algorithm
        :param securityCache: Cache for storing Security data
        """
        ...

    @staticmethod
    def decompose_currency_pair(symbol: typing.Union[QuantConnect.Symbol, str], symbol_properties: QuantConnect.Securities.SymbolProperties, base_currency: typing.Optional[str], quote_currency: typing.Optional[str]) -> typing.Tuple[None, str, str]:
        """
        Decomposes the specified currency pair into a base and quote currency provided as out parameters
        
        :param symbol: The input symbol to be decomposed
        :param symbol_properties: The symbol properties for this security
        :param base_currency: The output base currency
        :param quote_currency: The output quote currency
        """
        ...


class CfdDataFilter(QuantConnect.Securities.SecurityDataFilter):
    """CFD packet by packet data filtering mechanism for dynamically detecting bad ticks."""


class CfdHolding(QuantConnect.Securities.SecurityHolding):
    """CFD holdings implementation of the base securities class"""

    def __init__(self, security: QuantConnect.Securities.Cfd.Cfd, currencyConverter: QuantConnect.Securities.ICurrencyConverter) -> None:
        """
        CFD Holding Class constructor
        
        :param security: The CFD security being held
        :param currencyConverter: A currency converter instance
        """
        ...


class CfdCache(QuantConnect.Securities.SecurityCache):
    """CFD specific caching support"""


class CfdExchange(QuantConnect.Securities.SecurityExchange):
    """CFD exchange class - information and helper tools for CFD exchange properties"""

    @property
    def trading_days_per_year(self) -> int:
        """Number of trading days per year for this security, used for performance statistics."""
        ...

    def __init__(self, exchangeHours: QuantConnect.Securities.SecurityExchangeHours) -> None:
        """
        Initializes a new instance of the CfdExchange class using the specified
        exchange hours to determine open/close times
        
        :param exchangeHours: Contains the weekly exchange schedule plus holidays
        """
        ...


