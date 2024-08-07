import argparse
from typing import Tuple, List, Optional
import pandas as pd
from Misc.codes import ResultCodes
from DataWorker.worker import FileDataWorker, STANDARD_FILENAME
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
                             default=None,
                             help=f'path to file where processed\
                                  data will be stored, by default\
                                  it is "{STANDARD_FILENAME}"')

    self.__df = None
    self.__refined_df = None

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

    self.__df = parser.getDataFrame()

    converter = DataConverter()
    result, description = converter.ProcessDf(self.__df)

    if result is not ResultCodes.OK:
      return (result, description)

    self.__refined_df = converter.getData()

    dataWorker = FileDataWorker(self.__args["save"])

    result, description = dataWorker.CheckFile()
    if result is not ResultCodes.OK:
      return (result, description)

    result, description = dataWorker.WriteDfToFile(self.__refined_df)
    if result is not ResultCodes.OK:
      return (result, description)

    return (ResultCodes.OK, "All ok")

  def getRefinedData(self) -> Optional[pd.DataFrame]:
    return self.__refined_df

  def printHelp(self):
    self.parser.print_help()
