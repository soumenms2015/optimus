from optimus.engines.base.dataframe.dataframe import DataFrameBaseDataFrame
from optimus.engines.base.pandas.dataframe import PandasBaseDataFrame
# from optimus.engines.dask.dataframe import DaskDataFrame
from optimus.engines.pandas.io.save import Save


class PandasDataFrame(PandasBaseDataFrame, DataFrameBaseDataFrame):

    def _assign(self, kw_columns: dict):
        kw_columns = {str(key): kw_column for key, kw_column in kw_columns.items()}
        return self.root.data.assign(**kw_columns)

    def _base_to_dfd(self, pdf, n_partitions):
        pass

    @property
    def rows(self):
        from optimus.engines.pandas.rows import Rows
        return Rows(self)

    @property
    def cols(self):
        from optimus.engines.pandas.columns import Cols
        return Cols(self)

    @property
    def save(self):
        return Save(self)

    @property
    def functions(self):
        from optimus.engines.pandas.functions import PandasFunctions
        return PandasFunctions(self)

    @property
    def mask(self):
        from optimus.engines.pandas.mask import PandasMask
        return PandasMask(self)

    @property
    def ml(self):
        from optimus.engines.pandas.ml.models import ML
        return ML(self)

    @property
    def constants(self):
        from optimus.engines.pandas.constants import Constants
        return Constants()

    @property
    def encoding(self):
        from optimus.engines.pandas.ml.encoding import Encoding
        return Encoding(self)

    def _create_buffer_df(self, input_cols, n):
        pass

    def _buffer_window(self, input_cols, lower_bound, upper_bound):
        return PandasDataFrame(self.data[input_cols][lower_bound: upper_bound], op=self.op, label_encoder=self.le)

    def set_buffer(self, columns="*", n=None):
        return True

    def get_buffer(self):
        return self

    def to_optimus_pandas(self):
        return self.root

    def to_pandas(self):
        return self.root.data
