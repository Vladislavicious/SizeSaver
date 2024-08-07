import unittest
from datetime import datetime
from Misc.codes import ResultCodes
from DataWorker.converter import DataConverter, get_correct_headers, get_refined_headers
from typing import List

import pandas as pd

class TestDataConverter(unittest.TestCase):
  def common_BaseInit(self, df: pd.DataFrame) -> DataConverter:
    saver = DataConverter()
    saver.Initialize(df)
    return saver

  def common_Reshape(self, headers: List[str],
                     values: List[int | str | pd.Timestamp]) -> DataConverter:
    data = dict(zip(headers, values))
    df = pd.DataFrame.from_dict(data)

    saver = self.common_BaseInit(df)
    result, description = saver.CheckDataCorectness()
    self.assertEqual(result, ResultCodes.OK, description)

    newDf = saver.Reshape()
    self.assertEqual(type(newDf), pd.DataFrame)

    headers = pd.Index(get_refined_headers())
    given_headers = newDf.columns
    self.assertTrue(given_headers.equals(headers), f"{given_headers} != {headers}")
    self.assertTrue( type(newDf.loc[0, "last modified"]) is pd.Timestamp )
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
    result, description = saver.CheckDataCorectness()
    self.assertEqual(result, ResultCodes.BAD_DATA, description)

  def test_RefineGoodDf(self):
    time = pd.Timestamp( datetime.today() )

    headers = get_correct_headers()
    values = [[1 * 1024], [2 * 1024], [3 * 1024], [4 * 1024], [5 * 1024], ["some/path/to/file"], time]
    data = dict(zip(headers, values))
    df = pd.DataFrame.from_dict(data)

    saver = self.common_BaseInit(df)
    result, description = saver.CheckDataCorectness()
    self.assertEqual(result, ResultCodes.OK, description)

  def test_RefineBadDf(self):
    time = pd.Timestamp( datetime.today() )

    headers = ["a", "b", "c", "d", "e", "f", "g"]
    values = [[1 * 1024], [2 * 1024], [3 * 1024], [4 * 1024], [5 * 1024], ["some/path/to/file"], time]
    data = dict(zip(headers, values))
    df = pd.DataFrame.from_dict(data)

    saver = self.common_BaseInit(df)

    result, description = saver.CheckDataCorectness()
    self.assertEqual(result, ResultCodes.BAD_FILE_FORMAT, description)

  def test_ReshapeGoodDf(self):
    time = pd.Timestamp( datetime.today() )
    headers = get_correct_headers()
    values = [[1 * 1024], [2 * 1024], [3 * 1024], [4 * 1024], [5 * 1024], ["some/path/to/file"], time]

    saver = self.common_Reshape(headers, values)

  def test_ReshapeGoodDfNoneTime(self):
    headers = get_correct_headers()
    values = [[1 * 1024], [2 * 1024], [3 * 1024], [4 * 1024], [5 * 1024], ["some/path/to/file"], None]

    saver = self.common_Reshape(headers, values)

  def test_processGoodDf(self):
    time = pd.Timestamp( datetime.today() )
    headers = get_correct_headers()
    values = [[1 * 1024], [2 * 1024], [3 * 1024], [4 * 1024], [5 * 1024], ["some/path/to/file"], time]

    saver = self.common_Reshape(headers, values)
    expectedDf = saver.getData()

    unprocessedDf = pd.DataFrame.from_dict(dict(zip(get_correct_headers(), values)))
    newSaver = DataConverter()
    result, description = newSaver.ProcessDf(unprocessedDf)
    self.assertEqual(result, ResultCodes.OK, description)
    processedDf = newSaver.getData()
    self.assertTrue(processedDf.equals(expectedDf), f"{processedDf} \n!=\n {expectedDf}")
