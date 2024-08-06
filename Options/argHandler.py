import argparse
from typing import Tuple, List

from Misc.codes import ResultCodes
from DataWorker.worker import STANDARD_FILENAME
from DataWorker.converter import DataConverter

from Parser.parser import myStrParser, myFileParser

class ArgumentHandler:
  def __init__(self) -> None:
    self.__args = dict()
    self.parser = argparse.ArgumentParser(
                          description='tool to save gcc-size \
                                       output for processing')

    self.parser.add_argument('--filepath', action='store',
                             nargs='?', default="",
                             help='path to file where the \
                                  gcc-size output is stored')
    self.parser.add_argument('string', action='store', nargs='?',
                             default="", help='gcc-size output string')
    self.parser.add_argument('--save', action='store', nargs='?',
                             default=STANDARD_FILENAME,
                             help=f'path to file where processed\
                                  data will be stored, by default\
                                  it is "{STANDARD_FILENAME}"')

  def parse(self, arguments: List[str] | None):
    arg_list = None
    if arguments is not None and arguments != "":
      arg_list = arguments
    args = self.parser.parse_args(arg_list)
    self.__args = vars(args)
    return self.__args

  def __getParser(self) -> myStrParser:
    string = self.__args["string"]
    filename = self.__args["filepath"]

    if string != "":
      parser = myStrParser(string)
    else:
      parser = myFileParser(filename)
    return parser

  def react(self) -> Tuple[ResultCodes, str]:
    if self.__args["string"] != "" and \
       self.__args["filepath"] != "":
      return (ResultCodes.SIMULTUNANEOUS_OPTIONS,
              "can't have string and filepath definded at the same time")

    parser = self.__getParser()
    result, description = parser.parse_dataframe()

    if result is not ResultCodes.OK:
      return (result, description)

    converter = DataConverter()
    # converter.Initialize(
    # Нужно удалить time из converter'a
    # Поправить соответствующие тесты
    # добавить в метод refine исправление None в поле с временем
    # добавить сохранение в файл
    # добавить опцию для визуализации
    return (ResultCodes.OK, "All ok")

  def printHelp(self):
    self.parser.print_help()
