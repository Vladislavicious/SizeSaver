from typing import List, Tuple

import plotly.express as px
import pandas as pd

from Misc.codes import ResultCodes
from DataWorker.converter import get_refined_headers

class Visualizer:
  @classmethod
  def GetAvailableTypes(cls) -> List[str]:
    return ["full", "code", "constants", "variables"]

  def __init__(self, df: pd.DataFrame) -> None:
    self.__df = df

  def getColumnName(self, name: str) -> str:
    for header_name in get_refined_headers():
      if header_name.find(name) != -1:
        return header_name

    return ""
  def show(self, type: str = None) -> Tuple[ResultCodes, str]:
    if type is None or type == "":
      return (ResultCodes.OK, "All ok")
    if type not in set( Visualizer.GetAvailableTypes() ):
      return (ResultCodes.BAD_VIEW_OPTION, f"no such option: {type}")
    # plotting the line chart

    y_column_name = self.getColumnName(type)
    fig = px.line(self.__df, y=y_column_name, x="last modified",
                  markers=True)
    # showing the plot
    fig.show()

    return (ResultCodes.OK, "All ok")
