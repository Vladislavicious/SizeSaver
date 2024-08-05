from typing import Tuple

from Parser.parser import myFileParser, myStrParser
from Misc.codes import ResultCodes
class OptionsHandler:
  def __init__(self, optionStr: str) -> None:
    self.__optionStr = optionStr
    self.__parser = None

  def parse(self) -> Tuple[ResultCodes, str]:
    self.__parser = myFileParser(self.__optionStr)
    result, description = self.__parser.parse_raw()
    if result != ResultCodes.NO_FILE:
      return (result, description)

    stroka = self.__optionStr.split()

    if len(stroka) != 0:
      if stroka[0].find("/") != -1:
        return (ResultCodes.NO_FILE, "No Such File")
    self.__parser = myStrParser(self.__optionStr)
    result, description = self.__parser.parse_raw()

    return (result, description)

  def parse_df(self) -> Tuple[ResultCodes, str]:
    return self.__parser.refine()
