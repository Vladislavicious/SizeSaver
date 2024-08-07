import unittest

import pandas as pd

from Visualise.visualizer import Visualizer
from Parser.parser import myFileParser
from Parser.parser import ResultCodes

class TestVisualizer(unittest.TestCase):
  def test_createVisualizer(self):
    vis = Visualizer(pd.DataFrame())
    self.assertEqual(type(vis), Visualizer)

  def test_GetColumnByCorrectType(self):
    vis = Visualizer(pd.DataFrame())
    typeName = "code"
    columnName = vis.getColumnName(typeName)
    self.assertEqual(columnName, "code(text)")

    typeName = "cod"
    columnName = vis.getColumnName(typeName)
    self.assertEqual(columnName, "code(text)")

  def test_GetColumnByInCorrectType(self):
    vis = Visualizer(pd.DataFrame())
    typeName = "cle"
    columnName = vis.getColumnName(typeName)
    self.assertEqual(columnName, "")
