import abc
import pandas as pd
import os.path
import re, math, json
import openpyxl


class sheet_data:
    """
    工作表数据类，用于处理Excel工作表的数据。

    参数:
    - sheet_obj: 工作表对象
    - all_agents: 所有代理的字典

    方法:
    - parse_colstr: 解析列字符串
    - set: 设置单元格的值
    """

    def __init__(self, sheet_obj):
        self.sheet_obj = sheet_obj
        self.column_names = []
        self.column_name_index = {}
        self.excel_column_names = []
        self.rows = []

        for col_name in sheet_obj.columns.tolist():
            self.column_names.append(col_name)
            excel_col_name = openpyxl.utils.get_column_letter(sheet_obj.columns.get_loc(col_name) + 1)
            self.excel_column_names.append(excel_col_name)


        for idx, row in sheet_obj.iterrows():
            cur_row = []
            for c_idx in self.column_names:
                cur_row.append(row[c_idx])
            self.rows.append(cur_row)

        self.column_name_index = {colname: idx for idx, colname in enumerate(self.column_names)}

    def set(self, row_index, col_name, value):
        """
        设置单元格的值。

        参数:
        - row_index: 行索引
        - col_name: 列名
        - value: 要设置的值
        """
        target_col_name = ""
        if col_name in self.column_name_index:
            target_col_name = col_name
        else:
            target_col_name = self.column_names[self.excel_column_names.index(col_name)]
        self.sheet_obj.at[row_index, target_col_name] = value
        col_index = self.column_name_index[target_col_name]
        self.rows[row_index][col_index] = value
        pass


class excel_utils:
    def __init__(self, path):
        self.path = path
        self.all_sheets = {}

        xls = pd.ExcelFile(self.path)
        for sheet in xls.sheet_names:
            sheet_content = sheet_data(xls.parse(sheet))
            self.all_sheets[sheet] = sheet_content
