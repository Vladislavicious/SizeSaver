import unittest
from datetime import datetime
from Parser.parser import myFileParser
from Parser.parser import ResultCodes

import pandas as pd

      # Создание пустого класса
      # Передача несуществующего файла
      # Передача пустого файла
      # Передача существующего файла
      # Передача файла с корректными значениями
      # Передача файла с некорректными значениями
      # Считывание времени последнего изменения файла
      # Получение DataFram'а с нужными значениями

class TestParserFunctions(unittest.TestCase):
  def test_createParser(self):
    parser = myFileParser("")

  def common_TryParseRaw(self, filename: str,
                         expected_result_code: ResultCodes) -> myFileParser:
    parser = myFileParser(filename)

    result, description = parser.parse_raw()

    self.assertEqual(result, expected_result_code)
    return parser

  def common_TryParseRefined(self, filename: str,
                             expected_result_code: ResultCodes,
                             expected_values) -> myFileParser:
    parser = self.common_TryParseRaw(filename, ResultCodes.OK)
    result, description = parser.refine()

    self.assertEqual(result, expected_result_code)

    values_list = parser.getValues()

    self.assertListEqual(values_list, expected_values)
    return parser

  def test_NoFile(self):
    parser = self.common_TryParseRaw("noSuchFile.txt", ResultCodes.NO_FILE)

  def test_emptyFile(self):
    parser = self.common_TryParseRaw("Tests/Files/EmptyFile.txt",
                                     ResultCodes.EMPTY_FILE)

  def test_regularFile(self):
    parser = self.common_TryParseRaw("Tests/Files/TestFile1.txt",
                                     ResultCodes.OK)


  def test_readCorrectValues(self):
    parser = self.common_TryParseRaw("Tests/Files/TestFile1.txt",
                                     ResultCodes.OK)

    expected_values = ["648", "0", "15", "663", "297", "./bin/uno/FirstProject/FirstProject_.elf"]
    values_list = parser.getValues()

    expected_column_names = ['text', 'data', 'bss', 'dec', 'hex', 'filename']
    column_names = parser.getColumnNames()

    self.assertListEqual(values_list, expected_values)
    self.assertListEqual(column_names, expected_column_names)

  def test_refineValues(self):
    expected_values = [648, 0, 15, 663, 297, "./bin/uno/FirstProject/FirstProject_.elf"]
    parser = self.common_TryParseRefined("Tests/Files/TestFile1.txt",
                                         ResultCodes.OK,
                                         expected_values)

  def test_BadData(self):
    parser = self.common_TryParseRaw("Tests/Files/TestFileBadData.txt",
                                     ResultCodes.OK)


    result, description = parser.refine()
    self.assertEqual(result, ResultCodes.BAD_DATA)

  def test_HexData(self):
    expected_values = [648, 0, 15, 663, 295, "./bin/uno/FirstProject/FirstProject_.elf"]
    parser = self.common_TryParseRefined("Tests/Files/TestFileHexValue.txt",
                                        ResultCodes.OK,
                                        expected_values)
  def test_GetLastModifiedTimeWithNoElfFile(self):
    parser = self.common_TryParseRaw("Tests/Files/TestFile1.txt",
                                     ResultCodes.OK)

    time = parser.GetLastModifiedTime()
    self.assertEqual(time, None)

  def test_GetLastModifiedTime(self):
    parser = self.common_TryParseRaw("Tests/Files/TestFile2.txt",
                                     ResultCodes.OK)

    time = parser.GetLastModifiedTime()
    self.assertEqual(type(time), pd.Timestamp)

  def test_GetFullDataFrame(self):
    parser = myFileParser("Tests/Files/TestFile2.txt")

    result, description = parser.parse_dataframe()
    self.assertEqual(result, ResultCodes.OK)

    df = parser.getDataFrame()
    time = parser.GetLastModifiedTime()

    self.assertEqual(type(df), pd.DataFrame)
    expected_column_names = ['text', 'data', 'bss', 'dec', 'hex', 'filename', 'last modified']
    expected_values = [516, 0, 8, 524, 524, "./Tests/Files/EmptyFile.txt", time]
    expected_df = pd.DataFrame(columns=expected_column_names)
    expected_df.loc[0] = expected_values
    expected_df["last modified"] = [ time ]

    self.assertTrue(df.equals(expected_df))
