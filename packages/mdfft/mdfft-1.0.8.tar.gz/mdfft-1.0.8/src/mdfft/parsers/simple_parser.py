import re
from datetime import datetime
import dataclasses
from .raw_candle import RawCandle


@dataclasses.dataclass
class SimpleParser:
    __file = None
    __line_re = re.compile(
        r'^(\d?)(\d\d)(\d\d)(\d\d) (\d?\d)(\d\d) '+
        r'([\d\.]+) ([\d\.]+) ([\d\.]+) ([\d\.]+)\s*$')
    __candles = []

    def __init__(self, file):
        if file is None:
            raise ValueError('No file')
        self.__file = file

    def __clear_candles(self):
        self.__candles = []

    def __parse_line(self, line):
        mr = self.__line_re.match(line)
        if mr is None:
            raise ValueError('Unknown line - ' + line)

        start_year = 0
        if mr.group(1) == '1':
            start_year = 2000
        elif mr.group(1) == '':
            start_year = 1900
        else:
            raise ValueError('Wrong year - ' + mr.group(1))

        self.__candles.append(RawCandle(
            dt=datetime(
                year=int(mr.group(2)) + start_year,
                month=int(mr.group(3)),
                day=int(mr.group(4)),
                hour=int(mr.group(5)),
                minute=int(mr.group(6))
            ),
            o=float(mr.group(7)),
            h=float(mr.group(8)),
            l=float(mr.group(9)),
            c=float(mr.group(10))
        ))

    def parse(self):
        self.__clear_candles()
        with open(self.__file, encoding="utf-8") as fh:
            for line in fh:
                self.__parse_line(line)
            fh.close()
        return self.__candles
