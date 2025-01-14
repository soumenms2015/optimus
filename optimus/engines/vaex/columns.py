from optimus.engines.base.dataframe.columns import DataFrameBaseColumns


# @vaex.register_dataframe_accessor('cols', override=True)
class Cols(DataFrameBaseColumns):
    def __init__(self, df):
        super().__init__(df)

    def _map(self, df, input_col, output_col, func, *args):
        return df.apply(func, arguments=(df[input_col], *args,), vectorize=False)

    def _names(self):
        return self.root.data.get_column_names(strings=True)

    def append(self, dfs):
        pass

    @staticmethod
    def impute(input_cols, data_type="continuous", strategy="mean", fill_value=None, output_cols=None):
        pass

    @staticmethod
    def string_to_index(cols=None, output_cols=None):
        pass

    @staticmethod
    def index_to_string(cols=None, output_cols=None):
        pass
