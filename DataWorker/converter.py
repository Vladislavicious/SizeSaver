from datetime import datetime
import pandas as pd
from typing import Tuple, List

from Misc.codes import ResultCodes

def get_correct_headers() -> List[str]:
  return ["text", "data", "bss", "dec", "hex", "filename", "last modified"]

def get_refined_headers() -> List[str]:
  return ["code(text)", "constants(data)", "variables(bss)",
          "full(dec)", "filename", "last modified"]

def reduce_ints_to_kb(value):
  if type(value) is not str and type(value) is not pd.Timestamp:
    return value / 1024
  else:
    return value

class DataConverter:
  def __init__(self) -> None:
    self.__df = pd.DataFrame()

  def Initialize(self, df: pd.DataFrame) -> Tuple[ResultCodes, str]:
    self.__df = df
    return (ResultCodes.OK, "All ok")

  def CheckDataCorectness(self) -> Tuple[ResultCodes, str]:
    if pd.DataFrame().equals(self.__df):
      return (ResultCodes.BAD_DATA, "Bad data given")

    headers = pd.Index(get_correct_headers())
    given_headers = self.__df.columns
    if given_headers.equals(headers) is not True:
      return (ResultCodes.BAD_FILE_FORMAT, f"Bad Header: {list(given_headers)}")

    if self.__df.loc[0, "last modified"] is None:
      self.__df.loc[0, "last modified"] = pd.Timestamp( datetime.today() )

    return (ResultCodes.OK, "All ok")

  def Reshape(self) -> pd.DataFrame:
    self.__df = self.__df.drop("hex", axis=1)
    current_headers = list(self.__df.columns)
    newNames = dict(zip(current_headers, get_refined_headers()))

    self.__df.rename(columns=newNames, inplace=True)

    self.__df = self.__df.map(reduce_ints_to_kb)

    return self.__df

  def ProcessDf(self, df: pd.DataFrame) -> Tuple[ResultCodes, str]:
    result, description = self.Initialize(df)
    if result != ResultCodes.OK:
      return (result, description)

    result, description = self.CheckDataCorectness()
    if result != ResultCodes.OK:
      return (result, description)

    self.Reshape()
    return (ResultCodes.OK, "All ok")

  def getData(self) -> pd.DataFrame:
    return self.__df
