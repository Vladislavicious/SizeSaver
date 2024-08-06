from datetime import datetime
import pandas as pd
from typing import Tuple, List

from Misc.codes import ResultCodes

def get_correct_headers() -> List[str]:
  return ["text", "data", "bss", "dec", "hex", "filename"]

def get_refined_headers() -> List[str]:
  return ["code(text)", "constants(data)", "variables(bss)",
          "full(dec)", "last modified", "filename"]

def reduce_ints_to_kb(value):
  if type(value) is not str:
    return value / 1024
  else:
    return value

class DataConverter:
  def __init__(self) -> None:
    self.__df = pd.DataFrame()

  def Initialize(self, df: pd.DataFrame, date: datetime) -> Tuple[ResultCodes, str]:
    self.__df = df.copy(True)
    self.__date = date
    return (ResultCodes.OK, "All ok")

  def Refine(self) -> Tuple[ResultCodes, str]:
    if pd.DataFrame().equals(self.__df):
      return (ResultCodes.BAD_DATA, "Bad data given")

    headers = pd.Index(get_correct_headers())
    given_headers = self.__df.columns
    if given_headers.equals(headers) is True:
      return (ResultCodes.OK, "All ok")

    return (ResultCodes.BAD_FILE_FORMAT, f"Bad Header: {given_headers}")

  def Reshape(self) -> pd.DataFrame:
    newNames = dict(zip(get_correct_headers(), get_refined_headers()))
    self.__df.rename(columns=newNames, inplace=True)

    self.__df = self.__df.map(reduce_ints_to_kb)

    # self.__df['last modified'] = pd.Series(self.__df['last modified'], dtype="datetime64[m]")
    # data = pd.to_datetime( self.__date )
    # self.__df.loc[0, 'last modified'] = data

    return self.__df

  def getData(self) -> pd.DataFrame:
    return self.__df
