# These function can return and Column Expression or a list of columns expression
# Must return None if the data type can not be handle

import dask.array as da
from dask.array import stats
from dask.dataframe.core import DataFrame


class Functions:

    @staticmethod
    def min(columns, args):
        def dataframe_min_(df):
            return {"min": df[columns].min()}

        return dataframe_min_

    @staticmethod
    def max(columns, args):
        def dataframe_max_(df):
            return {"max": df[columns].max()}

        return dataframe_max_

    @staticmethod
    def stddev(columns, args):
        def dataframe_stddev_(df):
            return {"max": df[columns].std()}

        return dataframe_stddev_

    @staticmethod
    def mean(columns, args):
        def dataframe_mean_(df):
            return {"mean": df[columns].mean()}

        return dataframe_mean_

    @staticmethod
    def variance(columns, args):
        def dataframe_var_(df):
            return {"var": df[columns].var()}

        return dataframe_var_

    @staticmethod
    def sum(columns, args):

        def dataframe_sum_(df):
            return {"sum": df[columns].sum()}

        return dataframe_sum_

    @staticmethod
    def percentile_agg(columns, args):
        values = args[1]

        def _percentile(df):
            return {"percentile": df[columns].quantile(values)}

        return _percentile
    # @staticmethod
    # def min(col_name, args):
    #     def min_(serie):
    #         return {"min": serie[col_name].min()}
    #
    #     return min_
    #
    # @staticmethod
    # def max(col_name, args):
    #     def max_(serie):
    #         return {"max": serie[col_name].max()}
    #
    #     return max_
    #
    # @staticmethod
    # def stddev(col_name, args):
    #     def std_(serie):
    #         return {"stddev": serie[col_name].max()}
    #
    #     return std_
    # @staticmethod
    # def mean(col_name, args):
    #     def _mean(serie):
    #         return {"mean": serie[col_name].mean()}
    #
    #     return _mean
    #
    # @staticmethod
    # def sum(col_name, args):
    #     def std_(serie):
    #         return {"sum": serie[col_name].sum()}
    #
    #     return std_
    #
    # @staticmethod
    # def variance(col_name, args):
    #     def var_(serie):
    #         return {"variance": serie[col_name].var()}
    #
    #     return var_

    @staticmethod
    def zeros_agg(col_name, args):

        def zeros_(serie):
            result = {"zeros": (serie[col_name].values == 0).sum()}
            return result

        return zeros_

    @staticmethod
    def count_na_agg(col_name, args):
        # estimate = args[0]

        def count_na_(serie):
            result = {"count_na": serie[col_name].isnull().sum()}
            return result

        return count_na_

    @staticmethod
    def hist_agg(col_name, args):
        df = args[0]
        bins = args[1]
        range = args[2]

        def hist_agg_(serie):
            return {
                "hist_agg": list(da.histogram(serie[col_name], bins=bins, range=[range["min"], range["max"]])[0])}

        return hist_agg_

    @staticmethod
    def kurtosis(col_name, args):
        def _kurtoris(serie):
            result = {"kurtosis": float(stats.kurtosis(serie[col_name]))}
            return result

        return _kurtoris

    @staticmethod
    def skewness(col_name, args):
        def _skewness(serie):
            result = {"skewness": float(stats.skew(serie[col_name]))}
            return result

        return _skewness



    @staticmethod
    def count_uniques_agg(col_name, args):
        estimate = args[0]

        def _count_uniques_agg(serie):
            if estimate is True:
                result = {"count_uniques": serie[col_name].nunique_approx()}
            else:
                result = {"count_uniques": serie[col_name].nunique()}
            return result

        return _count_uniques_agg

    @staticmethod
    def mad_agg(col_name, args):
        more = args[0]

        def _mad_agg(serie):
            median_value = serie[col_name].quantile(0.5)
            mad_value = (serie[col_name] - median_value).abs().quantile(0.5)

            _mad = {}
            if more:
                result = {"mad": mad_value, "median": median_value}
            else:
                result = {"mad": mad_value}

            return result

        return _mad_agg


