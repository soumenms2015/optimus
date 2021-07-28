from abc import abstractmethod, ABC
from typing import Tuple
from optimus.helpers.types import DataFrameType, DataFrameTypeList, InternalDataFrameType

from multipledispatch import dispatch

from optimus.engines.base.meta import Meta
# This implementation works for Spark, Dask, dask_cudf
from optimus.helpers.columns import parse_columns
from optimus.helpers.constants import Actions
from optimus.helpers.core import one_list_to_val, val_to_list
from optimus.helpers.raiseit import RaiseIt
from optimus.infer import is_str, is_list_of_str_or_int


class BaseRows(ABC):
    """Base class for all Rows implementations"""

    def __init__(self, root: DataFrameType):
        self.root = root

    @staticmethod
    @abstractmethod
    def _sort(df, col_name, ascending) -> DataFrameType:
        pass

    def _sort_multiple(self, dfd, meta, col_sort) -> Tuple[InternalDataFrameType, dict]:
        """
        Sort rows taking into account multiple columns
        :param col_sort: column and sort type combination (col_name, "asc")
        :type col_sort: list of tuples
        """

        for cs in col_sort:
            col_name = one_list_to_val(cs[0])
            order = cs[1]

            if order != "asc" and order != "desc":
                RaiseIt.value_error(order, ["asc", "desc"])

            dfd = self._sort(dfd, col_name, True if order == "asc" else False)
            meta = Meta.action(meta, Actions.SORT_ROW.value, col_name)

        return dfd, meta

    def _reverse(self, dfd) -> InternalDataFrameType:
        return dfd[::-1]

    @staticmethod
    @abstractmethod
    def create_id(column="id"):
        pass

    @abstractmethod
    def append(self, dfs: DataFrameTypeList, cols_map) -> DataFrameType:
        pass

    def apply(self, func, args=None, output_cols=None) -> DataFrameType:
        """
        This will aimed to handle vectorized and not vectorized operations
        :param output_cols:
        :param func:
        :return:
        """
        df = self.root
        dfd = self.root.data
        kw_columns = {}

        for output_col in output_cols:
            result = func(dfd, *args)
            kw_columns = {output_col: result}

        return df.cols.assign(kw_columns)

    def select(self, expr=None, contains=None, case=None, flags=0, na=False, regex=False) -> DataFrameType:
        """
        :param expr: Expression used, For Ex: (df["A"] > 3) & (df["A"] <= 1000) or Column name "A"
        :param contains: List of string
        :param case:
        :param flags:
        :param na:
        :param regex:
        :return:
        """

        df = self.root
        dfd = df.data

        if is_str(expr):
            if expr in df.cols.names():
                if contains is not None:
                    expr = df.mask.contains(expr, value=contains, case=case, flags=flags, na=na, regex=regex)
                else:
                    expr = df[expr]
            else:
                expr = eval(expr)
        elif expr:
            expr = expr.get_series()
        dfd = dfd[expr]
        meta = Meta.action(df.meta, Actions.SELECT_ROW.value, df.cols.names())

        df = self.root.new(dfd, meta=meta)
        return df

    def _count(self, compute=True) -> int:
        return len(self.root.data.index)

    def count(self, compute=True) -> int:
        """
        Count dataframe rows
        """
        df = self.root
        dfd = df.data
        # TODO: Be sure that we need the compute param
        if compute is True:
            result = self._count(compute)
        else:
            result = df.functions.delayed(len)(dfd)
        return result

    def to_list(self, input_cols) -> list:
        """

        :param input_cols:
        :return:
        """
        df = self.root
        input_cols = parse_columns(df, input_cols)
        value = df.cols.select(input_cols).to_pandas().values.tolist()

        return value

    @dispatch(str)
    def sort(self, input_col) -> DataFrameType:
        df = self.root
        input_col = parse_columns(df, input_col)
        return df.rows.sort([(input_col, "desc",)])

    @dispatch(str, bool)
    def sort(self, input_col, asc=False) -> DataFrameType:
        df = self.root
        input_col = parse_columns(df, input_col)
        return df.rows.sort([(input_col, "asc" if asc else "desc",)])

    @dispatch(str, str)
    def sort(self, input_col, order="desc") -> DataFrameType:
        df = self.root
        input_col = parse_columns(df, input_col)
        return df.rows.sort([(input_col, order,)])

    @dispatch(dict)
    def sort(self, col_sort) -> DataFrameType:
        df = self.root
        return df.rows.sort([(k, v) for k, v in col_sort.items()])

    @dispatch(list, bool)
    def sort(self, input_col, asc=False) -> DataFrameType:
        df = self.root
        return df.rows.sort(input_col, "asc" if asc else "desc")

    @dispatch(list)
    def sort(self, input_col) -> DataFrameType:
        df = self.root
        return df.rows.sort(input_col)

    @dispatch(list, str)
    def sort(self, input_col, order="desc") -> DataFrameType:
        """
        Sort rows taking into account multiple columns
        :param input_col: column and sort type combination (col_name, "asc")
        :type input_col: list of tuples
        """
        # If a list of columns names are given order this by desc. If you need to specify the order of every
        # column use a list of tuples (col_name, "asc")
        df = self.root
        dfd = df.data
        meta = df.meta

        if is_list_of_str_or_int(input_col):
            t = []
            for col_name in input_col:
                t.append(tuple([col_name, order]))
            input_col = t

        dfd, meta = self._sort_multiple(dfd, meta, input_col)

        return self.root.new(dfd, meta=meta)

    def reverse(self) -> DataFrameType:
        """

        :return:
        """
        dfd = self._reverse(self.root.data)
        return self.root.new(dfd)

    def drop(self, where) -> DataFrameType:
        """
        Drop rows depending on a mask or an expression
        :param where: Mask, expression or name of the column to be taken as mask
        :return: Optimus Dataframe
        """
        df = self.root
        dfd = df.data

        if is_str(where):
            if where in df.cols.names():
                where = df[where]
            else:
                where = eval(where)
        dfd = dfd[where.get_series()==0]
        meta = Meta.action(df.meta, Actions.DROP_ROW.value, df.cols.names())
        return self.root.new(dfd, meta=meta)

    def between_index(self, cols="*", lower_bound=None, upper_bound=None):
        """

        :param columns:
        :param lower_bound:
        :param upper_bound:
        :return:
        """
        dfd = self.root.data
        cols = val_to_list(parse_columns(dfd, cols))
        return self.root.new(dfd[lower_bound: upper_bound][cols])

    def limit(self, count=10) -> DataFrameType:
        """
        Limit the number of rows
        :param count:
        :return:
        """
        return self.root.new(self.root.data[:count])

    @staticmethod
    @abstractmethod
    def unnest(input_cols) -> DataFrameType:
        pass

    def approx_count(self) -> DataFrameType:
        """
        Aprox count
        :return:
        """
        return self.root.rows.count()

    def _mask(self, cols, method, drop=False, how="any", *args, **kwargs) -> DataFrameType:

        df = self.root
        mask = getattr(df.mask, method)(cols=cols, *args, **kwargs)

        if how=="any":
            mask = mask.mask.any()
        elif how=="all":
            mask = mask.mask.all()
        else:
            RaiseIt.value_error(how, ["any", "all"])

        if drop:
            mask = ~mask

        df = df.rows.select(mask)

        return df


    def str(self, cols="*", drop=False, how="any") -> DataFrameType:
        return self._mask(cols, method="str", drop=drop, how=how)

    def int(self, cols="*", drop=False, how="any") -> DataFrameType:
        return self._mask(cols, method="int", drop=drop, how=how)

    def float(self, cols="*", drop=False, how="any") -> DataFrameType:
        return self._mask(cols, method="float", drop=drop, how=how)

    def numeric(self, cols="*", drop=False, how="any") -> DataFrameType:
        return self._mask(cols, method="numeric", drop=drop, how=how)

    def between(self, cols="*", lower_bound=None, upper_bound=None, equal=True, bounds=None, drop=False, how="any") -> DataFrameType:
        return self._mask(cols, method="between", drop=drop, how=how, lower_bound=lower_bound, upper_bound=upper_bound, equal=equal, bounds=bounds)

    def greater_than_equal(self, cols="*", value=None, drop=False, how="any") -> DataFrameType:
        return self._mask(cols, method="greater_than_equal", drop=drop, value=value, how=how)

    def greater_than(self, cols="*", value=None, drop=False, how="any") -> DataFrameType:
        return self._mask(cols, method="greater_than", drop=drop, value=value, how=how)

    def less_than(self, cols="*", value=None, drop=False, how="any") -> DataFrameType:
        return self._mask(cols, method="less_than", drop=drop, value=value, how=how)

    def less_than_equal(self, cols="*", value=None, drop=False, how="any") -> DataFrameType:
        return self._mask(cols, method="less_than_equal", drop=drop, value=value, how=how)

    def equal(self, cols="*", value=None, drop=False, how="any") -> DataFrameType:
        return self._mask(cols, method="equal", drop=drop, value=value, how=how)

    def not_equal(self, cols="*", value=None, drop=False, how="any") -> DataFrameType:
        return self._mask(cols, method="not_equal", drop=drop, value=value, how=how)

    def missing(self, cols="*", drop=False, how="any") -> DataFrameType:
        return self._mask(cols, method="missing", drop=drop, how=how)

    def null(self, cols="*", drop=False, how="any") -> DataFrameType:
        return self._mask(cols, method="null", drop=drop, how=how)

    def none(self, cols="*", drop=False, how="any") -> DataFrameType:
        return self._mask(cols, method="none", drop=drop, how=how)

    def nan(self, cols="*", drop=False, how="any") -> DataFrameType:
        return self._mask(cols, method="nan", drop=drop, how=how)

    def empty(self, cols="*", drop=False, how="any") -> DataFrameType:
        return self._mask(cols, method="empty", drop=drop, how=how)

    def duplicated(self, cols="*", keep="first", drop=False, how="any") -> DataFrameType:
        return self._mask(cols, method="duplicated", drop=drop, keep=keep, how=how)

    def unique(self, cols="*", keep="first", drop=False, how="any") -> DataFrameType:
        return self._mask(cols, method="unique", drop=drop, keep=keep, how=how)

    def mismatch(self, cols="*", data_type=None, drop=False, how="any") -> DataFrameType:
        return self._mask(cols, method="mismatch", drop=drop, data_type=data_type, how=how)

    def match(self, cols="*", regex=None, data_type=None, drop=False, how="any") -> DataFrameType:
        return self._mask(cols, method="match", drop=drop, regex=regex, data_type=data_type, how=how)

    def match_regex(self, cols="*", regex=None, drop=False, how="any") -> DataFrameType:
        return self._mask(cols, method="match_regex", drop=drop, regex=regex, how=how)

    def match_data_type(self, cols="*", data_type=None, drop=False, how="any") -> DataFrameType:
        return self._mask(cols, method="match_data_type", drop=drop, data_type=data_type, how=how)

    def value_in(self, cols="*", values=None, drop=False, how="any") -> DataFrameType:
        return self._mask(cols, method="value_in", drop=drop, values=values, how=how)

    def pattern(self, cols="*", pattern=None, drop=False, how="any") -> DataFrameType:
        return self._mask(cols, method="pattern", drop=drop, pattern=pattern, how=how)

    def starts_with(self, cols="*", value=None, drop=False, how="any") -> DataFrameType:
        return self._mask(cols, method="starts_with", drop=drop, value=value, how=how)

    def ends_with(self, cols="*", value=None, drop=False, how="any") -> DataFrameType:
        return self._mask(cols, method="ends_with", drop=drop, value=value, how=how)

    def contains(self, cols="*", value=None, drop=False, how="any") -> DataFrameType:
        return self._mask(cols, method="contains", drop=drop, value=value, how=how)

    def find(self, cols="*", value=None, drop=False, how="any") -> DataFrameType:
        return self._mask(cols, method="find", drop=drop, value=value, how=how)

    def email(self, cols="*", drop=False, how="any") -> DataFrameType:
        return self._mask(cols, method="email", drop=drop, how=how)

    def ip(self, cols="*", drop=False, how="any") -> DataFrameType:
        return self._mask(cols, method="ip", drop=drop, how=how)

    def url(self, cols="*", drop=False, how="any") -> DataFrameType:
        return self._mask(cols, method="url", drop=drop, how=how)

    def gender(self, cols="*", drop=False, how="any") -> DataFrameType:
        return self._mask(cols, method="gender", drop=drop, how=how)

    def boolean(self, cols="*", drop=False, how="any") -> DataFrameType:
        return self._mask(cols, method="boolean", drop=drop, how=how)

    def zip_code(self, cols="*", drop=False, how="any") -> DataFrameType:
        return self._mask(cols, method="zip_code", drop=drop, how=how)

    def credit_card_number(self, cols="*", drop=False, how="any") -> DataFrameType:
        return self._mask(cols, method="credit_card_number", drop=drop, how=how)

    def datetime(self, cols="*", drop=False, how="any") -> DataFrameType:
        return self._mask(cols, method="datetime", drop=drop, how=how)

    def object(self, cols="*", drop=False, how="any") -> DataFrameType:
        return self._mask(cols, method="object", drop=drop, how=how)

    def array(self, cols="*", drop=False, how="any") -> DataFrameType:
        return self._mask(cols, method="array", drop=drop, how=how)

    def phone_number(self, cols="*", drop=False, how="any") -> DataFrameType:
        return self._mask(cols, method="phone_number", drop=drop, how=how)

    def social_security_number(self, cols="*", drop=False, how="any") -> DataFrameType:
        return self._mask(cols, method="social_security_number", drop=drop, how=how)

    def http_code(self, cols="*", drop=False, how="any") -> DataFrameType:
        return self._mask(cols, method="http_code", drop=drop, how=how)

    def expression(self, where=None, cols="*", drop=False, how="any") -> DataFrameType:
        return self._mask(cols, method="expression", drop=drop, how=how, where=where)

    # drop functions

    def drop_str(self, cols="*", how="any") -> DataFrameType:
        return self._mask(cols, method="str", drop=True, how=how)

    def drop_int(self, cols="*", how="any") -> DataFrameType:
        return self._mask(cols, method="int", drop=True, how=how)

    def drop_float(self, cols="*", how="any") -> DataFrameType:
        return self._mask(cols, method="float", drop=True, how=how)

    def drop_numeric(self, cols="*", how="any") -> DataFrameType:
        return self._mask(cols, method="numeric", drop=True, how=how)

    def drop_greater_than_equal(self, cols="*", value=None, how="any") -> DataFrameType:
        return self._mask(cols, method="greater_than_equal", drop=True, value=value, how=how)

    def drop_greater_than(self, cols="*", value=None, how="any") -> DataFrameType:
        return self._mask(cols, method="greater_than", drop=True, value=value, how=how)

    def drop_less_than_equal(self, cols="*", value=None, how="any") -> DataFrameType:
        return self._mask(cols, method="less_than_equal", drop=True, value=value, how=how)

    def drop_less_than(self, cols="*", value=None, how="any") -> DataFrameType:
        return self._mask(cols, method="less_than", drop=True, value=value, how=how)

    def drop_between(self, cols="*", lower_bound=None, upper_bound=None, equal=True, bounds=None, how="any") -> DataFrameType:
        return self._mask(cols, method="between", drop=True, how=how, lower_bound=lower_bound, upper_bound=upper_bound, equal=equal, bounds=bounds)

    def drop_equal(self, cols="*", value=None, how="any") -> DataFrameType:
        return self._mask(cols, method="equal", drop=True, value=value, how=how)

    def drop_not_equal(self, cols="*", value=None, how="any") -> DataFrameType:
        return self._mask(cols, method="not_equal", drop=True, value=value, how=how)

    def drop_missings(self, cols="*", how="any") -> DataFrameType:
        return self._mask(cols, method="missing", drop=True, how=how)

    def drop_nulls(self, cols="*", how="any") -> DataFrameType:
        return self._mask(cols, method="null", drop=True, how=how)

    def drop_none(self, cols="*", how="any") -> DataFrameType:
        return self._mask(cols, method="none", drop=True, how=how)

    def drop_nan(self, cols="*", how="any") -> DataFrameType:
        return self._mask(cols, method="nan", drop=True, how=how)

    def drop_empty(self, cols="*", how="any") -> DataFrameType:
        return self._mask(cols, method="empty", drop=True, how=how)

    def drop_duplicated(self, cols="*", keep="first", how="any") -> DataFrameType:
        return self._mask(cols, method="duplicated", drop=True, keep=keep, how=how)

    def drop_uniques(self, cols="*", keep="first", how="any") -> DataFrameType:
        """
        Drops first (passed to keep) matches of duplicates and unique values.
        :param cols: 
        :param keep: 
        :param how: 
        :return: Dataframe
        """
        return self._mask(cols, method="unique", drop=True, keep=keep, how=how)

    def drop_mismatch(self, cols="*", data_type=None, how="any") -> DataFrameType:
        return self._mask(cols, method="mismatch", drop=True, data_type=data_type, how=how)

    def drop_match(self, cols="*", regex=None, data_type=None, how="any") -> DataFrameType:
        return self._mask(cols, method="match", drop=True, regex=regex, data_type=data_type, how=how)

    def drop_by_regex(self, cols="*", regex=None, how="any") -> DataFrameType:
        return self._mask(cols, method="match_regex", drop=True, regex=regex, how=how)

    def drop_by_data_type(self, cols="*", data_type=None, how="any") -> DataFrameType:
        return self._mask(cols, method="match_data_type", drop=True, data_type=data_type, how=how)

    def drop_value_in(self, cols="*", values=None, how="any") -> DataFrameType:
        return self._mask(cols, method="value_in", drop=True, values=values, how=how)

    def drop_pattern(self, cols="*", pattern=None, how="any") -> DataFrameType:
        return self._mask(cols, method="pattern", drop=True, pattern=pattern, how=how)

    def drop_starts_with(self, cols="*", value=None, how="any") -> DataFrameType:
        return self._mask(cols, method="starts_with", drop=True, value=value, how=how)

    def drop_ends_with(self, cols="*", value=None, how="any") -> DataFrameType:
        return self._mask(cols, method="ends_with", drop=True, value=value, how=how)

    def drop_contains(self, cols="*", value=None, how="any") -> DataFrameType:
        return self._mask(cols, method="contains", drop=True, value=value, how=how)

    def drop_find(self, cols="*", value=None, how="any") -> DataFrameType:
        return self._mask(cols, method="find", drop=True, value=value, how=how)

    def drop_emails(self, cols="*", how="any") -> DataFrameType:
        return self._mask(cols, method="email", drop=True, how=how)

    def drop_ips(self, cols="*", how="any") -> DataFrameType:
        return self._mask(cols, method="ip", drop=True, how=how)

    def drop_urls(self, cols="*", how="any") -> DataFrameType:
        return self._mask(cols, method="url", drop=True, how=how)

    def drop_genders(self, cols="*", how="any") -> DataFrameType:
        return self._mask(cols, method="gender", drop=True, how=how)

    def drop_booleans(self, cols="*", how="any") -> DataFrameType:
        return self._mask(cols, method="boolean", drop=True, how=how)

    def drop_zip_codes(self, cols="*", how="any") -> DataFrameType:
        return self._mask(cols, method="zip_code", drop=True, how=how)

    def drop_credit_card_numbers(self, cols="*", how="any") -> DataFrameType:
        return self._mask(cols, method="credit_card_number", drop=True, how=how)

    def drop_datetimes(self, cols="*", how="any") -> DataFrameType:
        return self._mask(cols, method="datetime", drop=True, how=how)

    def drop_objects(self, cols="*", how="any") -> DataFrameType:
        return self._mask(cols, method="object", drop=True, how=how)

    def drop_arrays(self, cols="*", how="any") -> DataFrameType:
        return self._mask(cols, method="array", drop=True, how=how)

    def drop_phone_numbers(self, cols="*", how="any") -> DataFrameType:
        return self._mask(cols, method="phone_number", drop=True, how=how)

    def drop_social_security_numbers(self, cols="*", how="any") -> DataFrameType:
        return self._mask(cols, method="social_security_number", drop=True, how=how)

    def drop_http_codes(self, cols="*", how="any") -> DataFrameType:
        return self._mask(cols, method="http_code", drop=True, how=how)

    def drop_by_expression(self, where=None, cols="*", how="any") -> DataFrameType:
        return self._mask(cols, method="expression", drop=True, how=how, where=where)
