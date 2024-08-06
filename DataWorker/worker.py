import os.path
from typing import Optional, Tuple

import pandas as pd

from Misc.codes import ResultCodes

STANDARD_FILENAME = "size_data.csv"

class FileDataWorker:
  def __init__(self, filename: str | None) -> None:
    if filename is None:
      self.__CreateStandardFile()
      self.__filename = STANDARD_FILENAME

    else:
      self.__filename = filename

  def __CreateStandardFile(self):
    if os.path.exists(STANDARD_FILENAME):
      return
    with open(STANDARD_FILENAME, "w", encoding="utf-8") as file:
      return

  def CheckFile(self) -> Tuple[ResultCodes, str]:
    if not self.__filename.endswith(".csv"):
      return (ResultCodes.BAD_FILE_FORMAT, "Bad file format")

    if os.path.exists(self.__filename):
      return (ResultCodes.OK, "All ok")
    else:
      return (ResultCodes.NO_FILE, f"No such file {self.__filename}")

  def WriteDfToFile(self, df: pd.DataFrame):
    if self.__isFileEmpty() is True:
      df.to_csv(self.__filename, mode="a",
                index=False)
    else:
      df.to_csv(self.__filename, mode="a",
                header=False, index=False)

    return (ResultCodes.OK, "All ok")

  def ReadDfFromFile(self) -> pd.DataFrame:
    df = pd.read_csv(self.__filename)
    return df

  def getFilename(self) -> str:
    return self.__filename

  def __isFileEmpty(self) -> bool:
    with open(self.__filename, "r", encoding="utf-8") as file:
      read = file.read(1)
      if read == "":
        return True
      else:
        return False
