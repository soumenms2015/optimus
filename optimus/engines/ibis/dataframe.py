from optimus.engines.base.basedataframe import BaseDataFrame
from optimus.engines.pandas.dataframe import PandasDataFrame


class IbisDataFrame(BaseDataFrame):

    @property
    def rows(self):
        from optimus.engines.ibis.rows import Rows
        return Rows(self)

    @property
    def cols(self):
        from optimus.engines.ibis.columns import Cols
        return Cols(self)

    @property
    def functions(self):
        from optimus.engines.ibis.functions import IbisFunctions
        return IbisFunctions(self)

    @staticmethod
    def sample(n=10, random=False):
        pass

    @staticmethod
    def melt(id_vars, value_vars, var_name="variable", value_name="value", data_type="str"):
        pass

    @staticmethod
    def query(sql_expression):
        pass

    @staticmethod
    def partitions():
        pass

    @staticmethod
    def partitioner():
        pass

    def repartition(self, n=None, *args, **kwargs):
        return self.root

    @staticmethod
    def show():
        pass

    @staticmethod
    def debug():
        pass

    def compile(self):
        # return str(ibis.impala.compiler(self.parent.data))
        return str(self.root.data.compile())

    def to_pandas(self):
        return self.root.data.execute()

    def to_optimus_dataframe(self):
        return

    def to_optimus_pandas(self):
        return PandasDataFrame(self.root.data.execute(), op=self.op)