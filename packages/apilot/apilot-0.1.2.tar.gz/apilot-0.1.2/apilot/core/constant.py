"""
APilot quantitative trading platform constant definitions.

This module contains all enumerations used throughout the platform.
"""

# Standard library imports
from datetime import timedelta
from enum import Enum


class Direction(Enum):
    LONG = "LONG"
    SHORT = "SHORT"


class Status(Enum):
    SUBMITTING = "SUBMITTING"
    NOTTRADED = "NOT_TRADED"
    PARTTRADED = "PARTIALLY_TRADED"
    ALLTRADED = "FULLY_TRADED"
    CANCELLED = "CANCELLED"
    REJECTED = "REJECTED"


class Product(Enum):
    SPOT = "SPOT"
    FUTURES = "FUTURES"
    MARGIN = "MARGIN"
    OPTION = "OPTION"


class OrderType(Enum):
    LIMIT = "LIMIT"
    MARKET = "MARKET"
    STOP = "STOP"
    STOP_LIMIT = "STOP_LIMIT"


class Interval(Enum):
    MINUTE = "1m"
    MINUTE3 = "3m"
    MINUTE5 = "5m"
    MINUTE15 = "15m"
    MINUTE30 = "30m"
    HOUR = "1h"
    HOUR4 = "4h"
    DAILY = "d"
    WEEKLY = "w"


class EngineType(Enum):
    LIVE = "LIVE"
    BACKTESTING = "BACKTESTING"


class AlgoStatus(Enum):
    RUNNING = "RUNNING"
    PAUSED = "PAUSED"
    STOPPED = "STOPPED"
    FINISHED = "FINISHED"


INTERVAL_DELTA_MAP: dict[Interval, timedelta] = {
    Interval.MINUTE: timedelta(minutes=1),
    Interval.HOUR: timedelta(hours=1),
    Interval.DAILY: timedelta(days=1),
}
