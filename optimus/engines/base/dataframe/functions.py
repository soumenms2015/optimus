import numpy as np

from optimus.engines.base.commons.functions import word_tokenize
from sklearn.preprocessing import MinMaxScaler, MaxAbsScaler, StandardScaler

from optimus.engines.base.functions import BaseFunctions


class DataFrameBaseFunctions(BaseFunctions):

    @staticmethod
    def map_partitions(dfd_or_series, func, *args, **kwargs):
        result = dfd_or_series.map_partitions(func, *args, **kwargs)
        result.index = dfd_or_series.index
        return result

    @staticmethod
    def all(series):
        return series.all()

    @staticmethod
    def not_all(series):
        return not series.all()

    @staticmethod
    def any(series):
        return series.any()
    
    @staticmethod
    def not_any(series):
        return not series.any()

    def reverse(self, series):
        return self.to_string(series).map(lambda v: v[::-1])

    def word_tokenize(self, series):
        return self.to_string(series).map(word_tokenize, na_action=None)

    def standard_scaler(self, series):
        return StandardScaler().fit_transform(self.to_float(series).values.reshape(-1, 1))

    def max_abs_scaler(self, series):
        return MaxAbsScaler().fit_transform(self.to_float(series).values.reshape(-1, 1))

    def min_max_scaler(self, series):
        return MinMaxScaler().fit_transform(self.to_float(series).values.reshape(-1, 1))

    @staticmethod
    def heatmap(df, bins):
        heatmap, xedges, yedges = np.histogram2d(df['x'].values, df['y'].values, bins=bins)
        return heatmap, xedges, yedges
