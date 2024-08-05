import os.path
from datetime import datetime
from time import ctime

from typing import Tuple, Optional
from enum import Enum

import pandas as pd
from Misc.codes import ResultCodes

def intTryParse(value):
    try:
        return int(value)
    except ValueError:
        try:
          return int(value, 16)
        except ValueError:
          return None

class myStrParser:
  def __init__(self, str: str) -> None:
    self._text = str
    self.__columnNames = list()
    self.__values = list()

  def _parseLines(self) -> Tuple[str, str]:
    lines = self._text.split("\n")
    if( len(lines) < 2 ):
      return ("", "")

    return (lines[0], lines[1])

  def _on_empty_line(self) -> Tuple[ResultCodes, str]:
    return (ResultCodes.NO_OPTIONS, f"Passed no options")

  def parse_raw(self) -> Tuple[ResultCodes, str]:
    firstLine, secondLine = self._parseLines()
    if len(firstLine) == 0:
      return self._on_empty_line()

    columns = firstLine.split()
    values = secondLine.split()

    self.__columnNames = list( columns )
    self.__values = list( values )
    return (ResultCodes.OK, "All ok")

  def refine(self) -> Tuple[ResultCodes, str]:
    for i in range(0, 5):
      value = self.__values[i]
      readValue = intTryParse(value)
      if readValue is None:
        return (ResultCodes.BAD_DATA, f"Bad data on {self.__columnNames[i]}")

      self.__values[i] = readValue

    return (ResultCodes.OK, "All ok")

  def GetLastModifiedTime(self) -> Optional[pd.Timestamp]:
    filename = self.__values[-1]

    if os.path.exists(filename) is not True:
      return None

    rawTime = os.path.getmtime(filename)
    time = pd.Timestamp(rawTime)

    return time

  def parse_dataframe(self) -> Optional[pd.DataFrame]:
    result, description = self.parse_raw()
    if result != ResultCodes.OK:
      print(description)
      return None

    result, description = self.refine()
    if result != ResultCodes.OK:
      print(description)
      return None

    df = pd.DataFrame(columns=self.__columnNames)
    df.loc[0] = self.__values

    df["timemodified"] = [ self.GetLastModifiedTime() ]
    return df

  def getValues(self):
    return self.__values

  def getColumnNames(self):
    return self.__columnNames

class myFileParser(myStrParser):
  def __init__(self, filename: str) -> None:
    super().__init__("")

    self.__filename = filename

  def __is_file_exist(self) -> bool:
    return os.path.exists(self.__filename)

  def _on_empty_line(self) -> Tuple[ResultCodes, str]:
    return (ResultCodes.EMPTY_FILE, f"Passed empty file")

  def _parseLines(self):
    with open(self.__filename, "r") as file:
      firstLine = file.readline()

      secondLine = file.readline()

      return (firstLine, secondLine)

  # Возвращает результат и описание, если ошибка
  def parse_raw(self) -> Tuple[ResultCodes, str]:
    if self.__is_file_exist() is False:
      return (ResultCodes.NO_FILE, f"No such file {self.__filename}")

    return super().parse_raw()
