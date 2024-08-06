import unittest
from datetime import datetime
from Misc.codes import ResultCodes
from DataWorker.converter import DataConverter, get_correct_headers

import pandas as pd

class TestDataConverter(unittest.TestCase):
  def common_BaseInit(self, df: pd.DataFrame) -> DataConverter:
    saver = DataConverter()
    date = datetime.today()
    saver.Initialize(df, date)
    return saver

  def test_InitializeDataConverter(self):
    saver = DataConverter()
    self.assertEqual(type(saver), DataConverter)

  def test_TakesCorrectData(self):
    df = pd.DataFrame()
    saver = self.common_BaseInit(df)
    result = df.equals(saver.getData())
    self.assertTrue(result)

  def test_RefineNoDf(self):
    saver = self.common_BaseInit(pd.DataFrame())
    result, description = saver.Refine()
    self.assertEqual(result, ResultCodes.BAD_DATA, description)

  def test_RefineGoodDf(self):
    headers = get_correct_headers()
    values = [[1 * 1024], [2 * 1024], [3 * 1024], [4 * 1024], [5 * 1024], ["some/path/to/file"]]
    data = dict(zip(headers, values))
    df = pd.DataFrame.from_dict(data)

    saver = self.common_BaseInit(df)
    result, description = saver.Refine()
    self.assertEqual(result, ResultCodes.OK, description)

  def test_RefineBadDf(self):
    headers = ["a", "b", "c", "d", "e", "f"]
    values = [[1 * 1024], [2 * 1024], [3 * 1024], [4 * 1024], [5 * 1024], ["some/path/to/file"]]
    data = dict(zip(headers, values))
    df = pd.DataFrame.from_dict(data)

    saver = self.common_BaseInit(df)

    result, description = saver.Refine()
    self.assertEqual(result, ResultCodes.BAD_FILE_FORMAT, description)

  def test_ReshapeGoodDf(self):
    headers = get_correct_headers()
    values = [[1 * 1024], [2 * 1024], [3 * 1024], [4 * 1024], [5 * 1024], ["some/path/to/file"]]
    data = dict(zip(headers, values))
    df = pd.DataFrame.from_dict(data)

    saver = self.common_BaseInit(df)
    result, description = saver.Refine()
    self.assertEqual(result, ResultCodes.OK, description)

    newDf = saver.Reshape()
    self.assertEqual(type(newDf), pd.DataFrame)
