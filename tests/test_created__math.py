import datetime
from optimus.tests.base import TestBase
from optimus.helpers.json import json_encoding
from optimus.helpers.functions import deep_sort, df_dicts_equal, results_equal


def Timestamp(t):
    return datetime.datetime.strptime(t, "%Y-%m-%d %H:%M:%S")


nan = float("nan")
inf = float("inf")


class TestMathPandas(TestBase):
    config = {'engine': 'pandas'}
    dict = {('NullType', 'object'): [None, None, None, None, None, None], ('attributes', 'object'): [[8.5344, 4300.0], [5.334, 2000.0], [7.9248, 4000.0], [3.9624, 1800.0], [None, 5700.0], [91.44, None]], ('date arrival', 'object'): ['1980/04/10', '1980/04/10', '1980/04/10', '1980/04/10', '1980/04/10', '1980/04/10'], ('function(binary)', 'object'): [bytearray(b'Leader'), bytearray(b'Espionage'), bytearray(b'Security'), bytearray(b'First Lieutenant'), bytearray(b'None'), bytearray(b'Battle Station')], ('height(ft)', 'float64'): [-28.0, 17.0, 26.0, 13.0, nan, 300.0], ('japanese name', 'object'): [['Inochi', 'Convoy'], ['Bumble', 'Goldback'], ['Roadbuster'], ['Meister'], ['Megatron'], ['Metroflex']], ('last date seen', 'object'): ['2016/09/10', '2015/08/10', '2014/07/10', '2013/06/10', '2012/05/10', '2011/04/10'], ('last position seen', 'object'): ['19.442735,-99.201111', '10.642707,-71.612534', '37.789563,-122.400356', '33.670666,-117.841553', None, None], ('rank', 'int64'): [10, 7, 7, 8, 10, 8], ('Cybertronian', 'bool'): [True, True, True, True, True, False], ('Date Type', 'datetime64[ns]'): [Timestamp('2016-09-10 00:00:00'), Timestamp('2015-08-10 00:00:00'), Timestamp('2014-06-24 00:00:00'), Timestamp('2013-06-24 00:00:00'), Timestamp('2012-05-10 00:00:00'), Timestamp('2011-04-10 00:00:00')], ('age', 'int64'): [5000000, 5000000, 5000000, 5000000, 5000000, 5000000], ('function', 'object'): ['Leader', 'Espionage', 'Security', 'First Lieutenant', 'None', 'Battle Station'], ('names', 'object'): ['Optimus', 'bumbl#ebéé  ', 'ironhide&', 'Jazz', 'Megatron', 'Metroplex_)^$'], ('timestamp', 'datetime64[ns]'): [Timestamp('2014-06-24 00:00:00'), Timestamp('2014-06-24 00:00:00'), Timestamp('2014-06-24 00:00:00'), Timestamp('2014-06-24 00:00:00'), Timestamp('2014-06-24 00:00:00'), Timestamp('2014-06-24 00:00:00')], ('weight(t)', 'float64'): [4.3, 2.0, 4.0, 1.8, 5.7, nan]}
    maxDiff = None

    def test_cols_add(self):
        df = self.create_dataframe(dict={('add_test1', 'float64'): [nan, nan, -9.0, 10.234, -inf, -42.0], ('add_test2', 'float64'): [nan, 1.0, 9.0, 703.0, inf, -321.0]}, force_data_types=True)
        result = df.cols.add(cols=['add_test1', 'add_test2'])
        expected = self.create_dataframe(dict={('add_test1', 'float64'): [nan, nan, -9.0, 10.234, -inf, -42.0], ('add_test2', 'float64'): [nan, 1.0, 9.0, 703.0, inf, -321.0], ('add_add_test1_add_test2', 'float64'): [nan, nan, 0.0, 713.234, nan, -363.0]}, force_data_types=True)
        self.assertTrue(result.equals(expected, decimal=True, assertion=True))

    def test_cols_add_2_numerics(self):
        df = self.df.cols.select(['height(ft)', 'rank'])
        result = df.cols.add(cols=['height(ft)', 'rank'])
        expected = self.create_dataframe(dict={('height(ft)', 'float64'): [-28.0, 17.0, 26.0, 13.0, nan, 300.0], ('rank', 'int64'): [10, 7, 7, 8, 10, 8], ('add_height(ft)_rank', 'float64'): [-18.0, 24.0, 33.0, 21.0, nan, 308.0]}, force_data_types=True)
        self.assertTrue(result.equals(expected, decimal=True, assertion=True))

    def test_cols_add_2_numerics_with_value(self):
        df = self.df.cols.select(['height(ft)', 'rank'])
        result = df.cols.add(cols=['height(ft)', 'rank'], value='-3')
        expected = self.create_dataframe(dict={('height(ft)', 'float64'): [-31.0, 14.0, 23.0, 10.0, nan, 297.0], ('rank', 'float64'): [7.0, 4.0, 4.0, 5.0, 7.0, 5.0]}, force_data_types=True)
        self.assertTrue(result.equals(expected, decimal=True, assertion=True))

    def test_cols_add_3_numerics(self):
        df = self.df.cols.select(['height(ft)', 'rank', 'age'])
        result = df.cols.add(cols=['height(ft)', 'rank', 'age'])
        expected = self.create_dataframe(dict={('height(ft)', 'float64'): [-28.0, 17.0, 26.0, 13.0, nan, 300.0], ('rank', 'int64'): [10, 7, 7, 8, 10, 8], ('age', 'int64'): [5000000, 5000000, 5000000, 5000000, 5000000, 5000000], ('add_height(ft)_rank_age', 'float64'): [4999982.0, 5000024.0, 5000033.0, 5000021.0, nan, 5000308.0]}, force_data_types=True)
        self.assertTrue(result.equals(expected, decimal=True, assertion=True))

    def test_cols_add_3_numerics_with_value(self):
        df = self.df.cols.select(['height(ft)', 'rank', 'age'])
        result = df.cols.add(cols=['height(ft)', 'rank', 'age'], value=inf)
        expected = self.create_dataframe(dict={('height(ft)', 'float64'): [inf, inf, inf, inf, nan, inf], ('rank', 'float64'): [inf, inf, inf, inf, inf, inf], ('age', 'float64'): [inf, inf, inf, inf, inf, inf]}, force_data_types=True)
        self.assertTrue(result.equals(expected, decimal=True, assertion=True))

    def test_cols_add_all(self):
        df = self.df
        result = df.cols.add(cols='*')
        expected = self.create_dataframe(dict={('NullType', 'object'): [None, None, None, None, None, None], ('attributes', 'object'): [[8.5344, 4300.0], [5.334, 2000.0], [7.9248, 4000.0], [3.9624, 1800.0], [None, 5700.0], [91.44, None]], ('date arrival', 'object'): ['1980/04/10', '1980/04/10', '1980/04/10', '1980/04/10', '1980/04/10', '1980/04/10'], ('function(binary)', 'object'): [bytearray(b'Leader'), bytearray(b'Espionage'), bytearray(b'Security'), bytearray(b'First Lieutenant'), bytearray(b'None'), bytearray(b'Battle Station')], ('height(ft)', 'float64'): [-28.0, 17.0, 26.0, 13.0, nan, 300.0], ('japanese name', 'object'): [['Inochi', 'Convoy'], ['Bumble', 'Goldback'], ['Roadbuster'], ['Meister'], ['Megatron'], ['Metroflex']], ('last date seen', 'object'): ['2016/09/10', '2015/08/10', '2014/07/10', '2013/06/10', '2012/05/10', '2011/04/10'], ('last position seen', 'object'): ['19.442735,-99.201111', '10.642707,-71.612534', '37.789563,-122.400356', '33.670666,-117.841553', None, None], ('rank', 'int64'): [10, 7, 7, 8, 10, 8], ('Cybertronian', 'bool'): [True, True, True, True, True, False], ('Date Type', 'datetime64[ns]'): [Timestamp('2016-09-10 00:00:00'), Timestamp('2015-08-10 00:00:00'), Timestamp('2014-06-24 00:00:00'), Timestamp('2013-06-24 00:00:00'), Timestamp('2012-05-10 00:00:00'), Timestamp('2011-04-10 00:00:00')], ('age', 'int64'): [5000000, 5000000, 5000000, 5000000, 5000000, 5000000], ('function', 'object'): ['Leader', 'Espionage', 'Security', 'First Lieutenant', 'None', 'Battle Station'], ('names', 'object'): ['Optimus', 'bumbl#ebéé  ', 'ironhide&', 'Jazz', 'Megatron', 'Metroplex_)^$'], ('timestamp', 'datetime64[ns]'): [Timestamp('2014-06-24 00:00:00'), Timestamp('2014-06-24 00:00:00'), Timestamp('2014-06-24 00:00:00'), Timestamp('2014-06-24 00:00:00'), Timestamp('2014-06-24 00:00:00'), Timestamp('2014-06-24 00:00:00')], ('weight(t)', 'float64'): [4.3, 2.0, 4.0, 1.8, 5.7, nan], ('add_*', 'float64'): [nan, nan, nan, nan, nan, nan]}, force_data_types=True)
        self.assertTrue(result.equals(expected, decimal=True, assertion=True))

    def test_cols_add_all_numerics(self):
        df = self.df.cols.select(['height(ft)', 'rank', 'age', 'weight(t)'])
        result = df.cols.add(cols=['height(ft)', 'rank', 'age', 'weight(t)'])
        expected = self.create_dataframe(dict={('height(ft)', 'float64'): [-28.0, 17.0, 26.0, 13.0, nan, 300.0], ('rank', 'int64'): [10, 7, 7, 8, 10, 8], ('age', 'int64'): [5000000, 5000000, 5000000, 5000000, 5000000, 5000000], ('weight(t)', 'float64'): [4.3, 2.0, 4.0, 1.8, 5.7, nan], ('add_height(ft)_rank_age_weight(t)', 'float64'): [4999986.3, 5000026.0, 5000037.0, 5000022.8, nan, nan]}, force_data_types=True)
        self.assertTrue(result.equals(expected, decimal=True, assertion=True))

    def test_cols_add_all_numerics_with_value(self):
        df = self.df.cols.select(['height(ft)', 'rank', 'age', 'weight(t)'])
        result = df.cols.add(cols=['height(ft)', 'rank', 'age', 'weight(t)'], value=nan)
        expected = self.create_dataframe(dict={('height(ft)', 'float64'): [nan, nan, nan, nan, nan, nan], ('rank', 'float64'): [nan, nan, nan, nan, nan, nan], ('age', 'float64'): [nan, nan, nan, nan, nan, nan], ('weight(t)', 'float64'): [nan, nan, nan, nan, nan, nan]}, force_data_types=True)
        self.assertTrue(result.equals(expected, decimal=True, assertion=True))

    def test_cols_add_all_with_value(self):
        df = self.df
        result = df.cols.add(cols='*', value=10.0)
        expected = self.create_dataframe(dict={('NullType', 'object'): [None, None, None, None, None, None], ('attributes', 'object'): [[8.5344, 4300.0], [5.334, 2000.0], [7.9248, 4000.0], [3.9624, 1800.0], [None, 5700.0], [91.44, None]], ('date arrival', 'object'): ['1980/04/10', '1980/04/10', '1980/04/10', '1980/04/10', '1980/04/10', '1980/04/10'], ('function(binary)', 'object'): [bytearray(b'Leader'), bytearray(b'Espionage'), bytearray(b'Security'), bytearray(b'First Lieutenant'), bytearray(b'None'), bytearray(b'Battle Station')], ('height(ft)', 'float64'): [-28.0, 17.0, 26.0, 13.0, nan, 300.0], ('japanese name', 'object'): [['Inochi', 'Convoy'], ['Bumble', 'Goldback'], ['Roadbuster'], ['Meister'], ['Megatron'], ['Metroflex']], ('last date seen', 'object'): ['2016/09/10', '2015/08/10', '2014/07/10', '2013/06/10', '2012/05/10', '2011/04/10'], ('last position seen', 'object'): ['19.442735,-99.201111', '10.642707,-71.612534', '37.789563,-122.400356', '33.670666,-117.841553', None, None], ('rank', 'int64'): [10, 7, 7, 8, 10, 8], ('Cybertronian', 'bool'): [True, True, True, True, True, False], ('Date Type', 'datetime64[ns]'): [Timestamp('2016-09-10 00:00:00'), Timestamp('2015-08-10 00:00:00'), Timestamp('2014-06-24 00:00:00'), Timestamp('2013-06-24 00:00:00'), Timestamp('2012-05-10 00:00:00'), Timestamp('2011-04-10 00:00:00')], ('age', 'int64'): [5000000, 5000000, 5000000, 5000000, 5000000, 5000000], ('function', 'object'): ['Leader', 'Espionage', 'Security', 'First Lieutenant', 'None', 'Battle Station'], ('names', 'object'): ['Optimus', 'bumbl#ebéé  ', 'ironhide&', 'Jazz', 'Megatron', 'Metroplex_)^$'], ('timestamp', 'datetime64[ns]'): [Timestamp('2014-06-24 00:00:00'), Timestamp('2014-06-24 00:00:00'), Timestamp('2014-06-24 00:00:00'), Timestamp('2014-06-24 00:00:00'), Timestamp('2014-06-24 00:00:00'), Timestamp('2014-06-24 00:00:00')], ('weight(t)', 'float64'): [4.3, 2.0, 4.0, 1.8, 5.7, nan], ('*', 'float64'): [nan, nan, nan, nan, nan, nan]}, force_data_types=True)
        self.assertTrue(result.equals(expected, decimal=True, assertion=True))

    def test_cols_add_string(self):
        df = self.df.cols.select(['names', 'function'])
        result = df.cols.add(cols=['names', 'function'], output_col='names-function')
        expected = self.create_dataframe(dict={('names', 'object'): ['Optimus', 'bumbl#ebéé  ', 'ironhide&', 'Jazz', 'Megatron', 'Metroplex_)^$'], ('function', 'object'): ['Leader', 'Espionage', 'Security', 'First Lieutenant', 'None', 'Battle Station'], ('names-function', 'float64'): [nan, nan, nan, nan, nan, nan]}, force_data_types=True)
        self.assertTrue(result.equals(expected, decimal=True, assertion=True))

    def test_cols_add_string_with_value(self):
        df = self.df.cols.select(['names', 'function'])
        result = df.cols.add(cols=['names', 'function'], value=103, output_col='names*function')
        expected = self.create_dataframe(dict={('names', 'float64'): [nan, nan, nan, nan, nan, nan], ('function', 'float64'): [nan, nan, nan, nan, nan, nan]}, force_data_types=True)
        self.assertTrue(result.equals(expected, decimal=True, assertion=True))

    def test_cols_add_various_types(self):
        df = self.df
        result = df.cols.add(cols=['NullType', 'weight(t)', 'japanese name'], output_col='nt+wt+jn')
        expected = self.create_dataframe(dict={('NullType', 'object'): [None, None, None, None, None, None], ('attributes', 'object'): [[8.5344, 4300.0], [5.334, 2000.0], [7.9248, 4000.0], [3.9624, 1800.0], [None, 5700.0], [91.44, None]], ('date arrival', 'object'): ['1980/04/10', '1980/04/10', '1980/04/10', '1980/04/10', '1980/04/10', '1980/04/10'], ('function(binary)', 'object'): [bytearray(b'Leader'), bytearray(b'Espionage'), bytearray(b'Security'), bytearray(b'First Lieutenant'), bytearray(b'None'), bytearray(b'Battle Station')], ('height(ft)', 'float64'): [-28.0, 17.0, 26.0, 13.0, nan, 300.0], ('japanese name', 'object'): [['Inochi', 'Convoy'], ['Bumble', 'Goldback'], ['Roadbuster'], ['Meister'], ['Megatron'], ['Metroflex']], ('last date seen', 'object'): ['2016/09/10', '2015/08/10', '2014/07/10', '2013/06/10', '2012/05/10', '2011/04/10'], ('last position seen', 'object'): ['19.442735,-99.201111', '10.642707,-71.612534', '37.789563,-122.400356', '33.670666,-117.841553', None, None], ('rank', 'int64'): [10, 7, 7, 8, 10, 8], ('Cybertronian', 'bool'): [True, True, True, True, True, False], ('Date Type', 'datetime64[ns]'): [Timestamp('2016-09-10 00:00:00'), Timestamp('2015-08-10 00:00:00'), Timestamp('2014-06-24 00:00:00'), Timestamp('2013-06-24 00:00:00'), Timestamp('2012-05-10 00:00:00'), Timestamp('2011-04-10 00:00:00')], ('age', 'int64'): [5000000, 5000000, 5000000, 5000000, 5000000, 5000000], ('function', 'object'): ['Leader', 'Espionage', 'Security', 'First Lieutenant', 'None', 'Battle Station'], ('names', 'object'): ['Optimus', 'bumbl#ebéé  ', 'ironhide&', 'Jazz', 'Megatron', 'Metroplex_)^$'], ('timestamp', 'datetime64[ns]'): [Timestamp('2014-06-24 00:00:00'), Timestamp('2014-06-24 00:00:00'), Timestamp('2014-06-24 00:00:00'), Timestamp('2014-06-24 00:00:00'), Timestamp('2014-06-24 00:00:00'), Timestamp('2014-06-24 00:00:00')], ('weight(t)', 'float64'): [4.3, 2.0, 4.0, 1.8, 5.7, nan], ('nt+wt+jn', 'float64'): [nan, nan, nan, nan, nan, nan]}, force_data_types=True)
        self.assertTrue(result.equals(expected, decimal=True, assertion=True))

    def test_cols_add_various_types_with_value(self):
        df = self.df
        result = df.cols.add(cols=['NullType', 'weight(t)', 'japanese name'], value=23.071, output_col='nt*wt*jn')
        expected = self.create_dataframe(dict={('NullType', 'float64'): [nan, nan, nan, nan, nan, nan], ('attributes', 'object'): [[8.5344, 4300.0], [5.334, 2000.0], [7.9248, 4000.0], [3.9624, 1800.0], [None, 5700.0], [91.44, None]], ('date arrival', 'object'): ['1980/04/10', '1980/04/10', '1980/04/10', '1980/04/10', '1980/04/10', '1980/04/10'], ('function(binary)', 'object'): [bytearray(b'Leader'), bytearray(b'Espionage'), bytearray(b'Security'), bytearray(b'First Lieutenant'), bytearray(b'None'), bytearray(b'Battle Station')], ('height(ft)', 'float64'): [-28.0, 17.0, 26.0, 13.0, nan, 300.0], ('japanese name', 'float64'): [nan, nan, nan, nan, nan, nan], ('last date seen', 'object'): ['2016/09/10', '2015/08/10', '2014/07/10', '2013/06/10', '2012/05/10', '2011/04/10'], ('last position seen', 'object'): ['19.442735,-99.201111', '10.642707,-71.612534', '37.789563,-122.400356', '33.670666,-117.841553', None, None], ('rank', 'int64'): [10, 7, 7, 8, 10, 8], ('Cybertronian', 'bool'): [True, True, True, True, True, False], ('Date Type', 'datetime64[ns]'): [Timestamp('2016-09-10 00:00:00'), Timestamp('2015-08-10 00:00:00'), Timestamp('2014-06-24 00:00:00'), Timestamp('2013-06-24 00:00:00'), Timestamp('2012-05-10 00:00:00'), Timestamp('2011-04-10 00:00:00')], ('age', 'int64'): [5000000, 5000000, 5000000, 5000000, 5000000, 5000000], ('function', 'object'): ['Leader', 'Espionage', 'Security', 'First Lieutenant', 'None', 'Battle Station'], ('names', 'object'): ['Optimus', 'bumbl#ebéé  ', 'ironhide&', 'Jazz', 'Megatron', 'Metroplex_)^$'], ('timestamp', 'datetime64[ns]'): [Timestamp('2014-06-24 00:00:00'), Timestamp('2014-06-24 00:00:00'), Timestamp('2014-06-24 00:00:00'), Timestamp('2014-06-24 00:00:00'), Timestamp('2014-06-24 00:00:00'), Timestamp('2014-06-24 00:00:00')], ('weight(t)', 'float64'): [27.371000000000002, 25.071, 27.071, 24.871000000000002, 28.771, nan]}, force_data_types=True)
        self.assertTrue(result.equals(expected, decimal=True, assertion=True))

    def test_cols_add_with_value(self):
        df = self.create_dataframe(dict={('add_test', 'float64'): [nan, nan, 5.0, 10.234, -inf, -42.0]}, force_data_types=True)
        result = df.cols.add(cols=['add_test'], value=33.5)
        expected = self.create_dataframe(dict={('add_test', 'float64'): [nan, nan, 38.5, 43.734, -inf, -8.5]}, force_data_types=True)
        self.assertTrue(result.equals(expected, decimal=True, assertion=True))

    def test_cols_div(self):
        df = self.create_dataframe(dict={('div_test1', 'float64'): [nan, nan, -8.0, 10.234, -inf, -42.0], ('div_test2', 'float64'): [nan, 1.0, 0.0, 703.0, inf, -321.0]}, force_data_types=True)
        result = df.cols.div(cols=['div_test1', 'div_test2'])
        expected = self.create_dataframe(dict={('div_test1', 'float64'): [nan, nan, -8.0, 10.234, -inf, -42.0], ('div_test2', 'float64'): [nan, 1.0, 0.0, 703.0, inf, -321.0], ('div_div_test1_div_test2', 'float64'): [nan, nan, -inf, 0.014557610241820769, nan, 0.1308411214953271]}, force_data_types=True)
        self.assertTrue(result.equals(expected, decimal=True, assertion=True))

    def test_cols_div_2_numerics(self):
        df = self.df.cols.select(['height(ft)', 'rank'])
        result = df.cols.div(cols=['height(ft)', 'rank'])
        expected = self.create_dataframe(dict={('height(ft)', 'float64'): [-28.0, 17.0, 26.0, 13.0, nan, 300.0], ('rank', 'int64'): [10, 7, 7, 8, 10, 8], ('div_height(ft)_rank', 'float64'): [-2.8, 2.4285714285714284, 3.7142857142857144, 1.625, nan, 37.5]}, force_data_types=True)
        self.assertTrue(result.equals(expected, decimal=True, assertion=True))

    def test_cols_div_2_numerics_with_value(self):
        df = self.df.cols.select(['height(ft)', 'rank'])
        result = df.cols.div(cols=['height(ft)', 'rank'], value='0')
        expected = self.create_dataframe(dict={('height(ft)', 'float64'): [-inf, inf, inf, inf, nan, inf], ('rank', 'float64'): [inf, inf, inf, inf, inf, inf]}, force_data_types=True)
        self.assertTrue(result.equals(expected, decimal=True, assertion=True))

    def test_cols_div_3_numerics(self):
        df = self.df.cols.select(['height(ft)', 'rank', 'age'])
        result = df.cols.div(cols=['height(ft)', 'rank', 'age'])
        expected = self.create_dataframe(dict={('height(ft)', 'float64'): [-28.0, 17.0, 26.0, 13.0, nan, 300.0], ('rank', 'int64'): [10, 7, 7, 8, 10, 8], ('age', 'int64'): [5000000, 5000000, 5000000, 5000000, 5000000, 5000000], ('div_height(ft)_rank_age', 'float64'): [-5.599999999999999e-07, 4.857142857142856e-07, 7.428571428571429e-07, 3.25e-07, nan, 7.5e-06]}, force_data_types=True)
        self.assertTrue(result.equals(expected, decimal=True, assertion=True))

    def test_cols_div_3_numerics_with_value(self):
        df = self.df.cols.select(['height(ft)', 'rank', 'age'])
        result = df.cols.div(cols=['height(ft)', 'rank', 'age'], value=inf)
        expected = self.create_dataframe(dict={('height(ft)', 'float64'): [-0.0, 0.0, 0.0, 0.0, nan, 0.0], ('rank', 'float64'): [0.0, 0.0, 0.0, 0.0, 0.0, 0.0], ('age', 'float64'): [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]}, force_data_types=True)
        self.assertTrue(result.equals(expected, decimal=True, assertion=True))

    def test_cols_div_all(self):
        df = self.df
        result = df.cols.div(cols='*')
        expected = self.create_dataframe(dict={('NullType', 'object'): [None, None, None, None, None, None], ('attributes', 'object'): [[8.5344, 4300.0], [5.334, 2000.0], [7.9248, 4000.0], [3.9624, 1800.0], [None, 5700.0], [91.44, None]], ('date arrival', 'object'): ['1980/04/10', '1980/04/10', '1980/04/10', '1980/04/10', '1980/04/10', '1980/04/10'], ('function(binary)', 'object'): [bytearray(b'Leader'), bytearray(b'Espionage'), bytearray(b'Security'), bytearray(b'First Lieutenant'), bytearray(b'None'), bytearray(b'Battle Station')], ('height(ft)', 'float64'): [-28.0, 17.0, 26.0, 13.0, nan, 300.0], ('japanese name', 'object'): [['Inochi', 'Convoy'], ['Bumble', 'Goldback'], ['Roadbuster'], ['Meister'], ['Megatron'], ['Metroflex']], ('last date seen', 'object'): ['2016/09/10', '2015/08/10', '2014/07/10', '2013/06/10', '2012/05/10', '2011/04/10'], ('last position seen', 'object'): ['19.442735,-99.201111', '10.642707,-71.612534', '37.789563,-122.400356', '33.670666,-117.841553', None, None], ('rank', 'int64'): [10, 7, 7, 8, 10, 8], ('Cybertronian', 'bool'): [True, True, True, True, True, False], ('Date Type', 'datetime64[ns]'): [Timestamp('2016-09-10 00:00:00'), Timestamp('2015-08-10 00:00:00'), Timestamp('2014-06-24 00:00:00'), Timestamp('2013-06-24 00:00:00'), Timestamp('2012-05-10 00:00:00'), Timestamp('2011-04-10 00:00:00')], ('age', 'int64'): [5000000, 5000000, 5000000, 5000000, 5000000, 5000000], ('function', 'object'): ['Leader', 'Espionage', 'Security', 'First Lieutenant', 'None', 'Battle Station'], ('names', 'object'): ['Optimus', 'bumbl#ebéé  ', 'ironhide&', 'Jazz', 'Megatron', 'Metroplex_)^$'], ('timestamp', 'datetime64[ns]'): [Timestamp('2014-06-24 00:00:00'), Timestamp('2014-06-24 00:00:00'), Timestamp('2014-06-24 00:00:00'), Timestamp('2014-06-24 00:00:00'), Timestamp('2014-06-24 00:00:00'), Timestamp('2014-06-24 00:00:00')], ('weight(t)', 'float64'): [4.3, 2.0, 4.0, 1.8, 5.7, nan], ('div_*', 'float64'): [nan, nan, nan, nan, nan, nan]}, force_data_types=True)
        self.assertTrue(result.equals(expected, decimal=True, assertion=True))

    def test_cols_div_all_numerics(self):
        df = self.df.cols.select(['height(ft)', 'rank', 'age', 'weight(t)'])
        result = df.cols.div(cols=['height(ft)', 'rank', 'age', 'weight(t)'])
        expected = self.create_dataframe(dict={('height(ft)', 'float64'): [-28.0, 17.0, 26.0, 13.0, nan, 300.0], ('rank', 'int64'): [10, 7, 7, 8, 10, 8], ('age', 'int64'): [5000000, 5000000, 5000000, 5000000, 5000000, 5000000], ('weight(t)', 'float64'): [4.3, 2.0, 4.0, 1.8, 5.7, nan], ('div_height(ft)_rank_age_weight(t)', 'float64'): [-1.3023255813953487e-07, 2.428571428571428e-07, 1.8571428571428572e-07, 1.8055555555555556e-07, nan, nan]}, force_data_types=True)
        self.assertTrue(result.equals(expected, decimal=True, assertion=True))

    def test_cols_div_all_numerics_with_value(self):
        df = self.df.cols.select(['height(ft)', 'rank', 'age', 'weight(t)'])
        result = df.cols.div(cols=['height(ft)', 'rank', 'age', 'weight(t)'], value=nan)
        expected = self.create_dataframe(dict={('height(ft)', 'float64'): [nan, nan, nan, nan, nan, nan], ('rank', 'float64'): [nan, nan, nan, nan, nan, nan], ('age', 'float64'): [nan, nan, nan, nan, nan, nan], ('weight(t)', 'float64'): [nan, nan, nan, nan, nan, nan]}, force_data_types=True)
        self.assertTrue(result.equals(expected, decimal=True, assertion=True))

    def test_cols_div_all_with_value(self):
        df = self.df
        result = df.cols.div(cols='*', value=10.0)
        expected = self.create_dataframe(dict={('NullType', 'object'): [None, None, None, None, None, None], ('attributes', 'object'): [[8.5344, 4300.0], [5.334, 2000.0], [7.9248, 4000.0], [3.9624, 1800.0], [None, 5700.0], [91.44, None]], ('date arrival', 'object'): ['1980/04/10', '1980/04/10', '1980/04/10', '1980/04/10', '1980/04/10', '1980/04/10'], ('function(binary)', 'object'): [bytearray(b'Leader'), bytearray(b'Espionage'), bytearray(b'Security'), bytearray(b'First Lieutenant'), bytearray(b'None'), bytearray(b'Battle Station')], ('height(ft)', 'float64'): [-28.0, 17.0, 26.0, 13.0, nan, 300.0], ('japanese name', 'object'): [['Inochi', 'Convoy'], ['Bumble', 'Goldback'], ['Roadbuster'], ['Meister'], ['Megatron'], ['Metroflex']], ('last date seen', 'object'): ['2016/09/10', '2015/08/10', '2014/07/10', '2013/06/10', '2012/05/10', '2011/04/10'], ('last position seen', 'object'): ['19.442735,-99.201111', '10.642707,-71.612534', '37.789563,-122.400356', '33.670666,-117.841553', None, None], ('rank', 'int64'): [10, 7, 7, 8, 10, 8], ('Cybertronian', 'bool'): [True, True, True, True, True, False], ('Date Type', 'datetime64[ns]'): [Timestamp('2016-09-10 00:00:00'), Timestamp('2015-08-10 00:00:00'), Timestamp('2014-06-24 00:00:00'), Timestamp('2013-06-24 00:00:00'), Timestamp('2012-05-10 00:00:00'), Timestamp('2011-04-10 00:00:00')], ('age', 'int64'): [5000000, 5000000, 5000000, 5000000, 5000000, 5000000], ('function', 'object'): ['Leader', 'Espionage', 'Security', 'First Lieutenant', 'None', 'Battle Station'], ('names', 'object'): ['Optimus', 'bumbl#ebéé  ', 'ironhide&', 'Jazz', 'Megatron', 'Metroplex_)^$'], ('timestamp', 'datetime64[ns]'): [Timestamp('2014-06-24 00:00:00'), Timestamp('2014-06-24 00:00:00'), Timestamp('2014-06-24 00:00:00'), Timestamp('2014-06-24 00:00:00'), Timestamp('2014-06-24 00:00:00'), Timestamp('2014-06-24 00:00:00')], ('weight(t)', 'float64'): [4.3, 2.0, 4.0, 1.8, 5.7, nan], ('*', 'float64'): [nan, nan, nan, nan, nan, nan]}, force_data_types=True)
        self.assertTrue(result.equals(expected, decimal=True, assertion=True))

    def test_cols_div_string(self):
        df = self.df.cols.select(['names', 'function'])
        result = df.cols.div(cols=['names', 'function'], output_col='names/function')
        expected = self.create_dataframe(dict={('names', 'object'): ['Optimus', 'bumbl#ebéé  ', 'ironhide&', 'Jazz', 'Megatron', 'Metroplex_)^$'], ('function', 'object'): ['Leader', 'Espionage', 'Security', 'First Lieutenant', 'None', 'Battle Station'], ('names/function', 'float64'): [nan, nan, nan, nan, nan, nan]}, force_data_types=True)
        self.assertTrue(result.equals(expected, decimal=True, assertion=True))

    def test_cols_div_string_with_value(self):
        df = self.df.cols.select(['names', 'function'])
        result = df.cols.div(cols=['names', 'function'], value=103, output_col='names*function')
        expected = self.create_dataframe(dict={('names', 'float64'): [nan, nan, nan, nan, nan, nan], ('function', 'float64'): [nan, nan, nan, nan, nan, nan]}, force_data_types=True)
        self.assertTrue(result.equals(expected, decimal=True, assertion=True))

    def test_cols_div_various_types(self):
        df = self.df
        result = df.cols.div(cols=['NullType', 'weight(t)', 'japanese name'], output_col='nt*wt*jn')
        expected = self.create_dataframe(dict={('NullType', 'object'): [None, None, None, None, None, None], ('attributes', 'object'): [[8.5344, 4300.0], [5.334, 2000.0], [7.9248, 4000.0], [3.9624, 1800.0], [None, 5700.0], [91.44, None]], ('date arrival', 'object'): ['1980/04/10', '1980/04/10', '1980/04/10', '1980/04/10', '1980/04/10', '1980/04/10'], ('function(binary)', 'object'): [bytearray(b'Leader'), bytearray(b'Espionage'), bytearray(b'Security'), bytearray(b'First Lieutenant'), bytearray(b'None'), bytearray(b'Battle Station')], ('height(ft)', 'float64'): [-28.0, 17.0, 26.0, 13.0, nan, 300.0], ('japanese name', 'object'): [['Inochi', 'Convoy'], ['Bumble', 'Goldback'], ['Roadbuster'], ['Meister'], ['Megatron'], ['Metroflex']], ('last date seen', 'object'): ['2016/09/10', '2015/08/10', '2014/07/10', '2013/06/10', '2012/05/10', '2011/04/10'], ('last position seen', 'object'): ['19.442735,-99.201111', '10.642707,-71.612534', '37.789563,-122.400356', '33.670666,-117.841553', None, None], ('rank', 'int64'): [10, 7, 7, 8, 10, 8], ('Cybertronian', 'bool'): [True, True, True, True, True, False], ('Date Type', 'datetime64[ns]'): [Timestamp('2016-09-10 00:00:00'), Timestamp('2015-08-10 00:00:00'), Timestamp('2014-06-24 00:00:00'), Timestamp('2013-06-24 00:00:00'), Timestamp('2012-05-10 00:00:00'), Timestamp('2011-04-10 00:00:00')], ('age', 'int64'): [5000000, 5000000, 5000000, 5000000, 5000000, 5000000], ('function', 'object'): ['Leader', 'Espionage', 'Security', 'First Lieutenant', 'None', 'Battle Station'], ('names', 'object'): ['Optimus', 'bumbl#ebéé  ', 'ironhide&', 'Jazz', 'Megatron', 'Metroplex_)^$'], ('timestamp', 'datetime64[ns]'): [Timestamp('2014-06-24 00:00:00'), Timestamp('2014-06-24 00:00:00'), Timestamp('2014-06-24 00:00:00'), Timestamp('2014-06-24 00:00:00'), Timestamp('2014-06-24 00:00:00'), Timestamp('2014-06-24 00:00:00')], ('weight(t)', 'float64'): [4.3, 2.0, 4.0, 1.8, 5.7, nan], ('nt*wt*jn', 'float64'): [nan, nan, nan, nan, nan, nan]}, force_data_types=True)
        self.assertTrue(result.equals(expected, decimal=True, assertion=True))

    def test_cols_div_various_types_with_value(self):
        df = self.df
        result = df.cols.div(cols=['NullType', 'weight(t)', 'japanese name'], value=23.071, output_col='nt*wt*jn')
        expected = self.create_dataframe(dict={('NullType', 'float64'): [nan, nan, nan, nan, nan, nan], ('attributes', 'object'): [[8.5344, 4300.0], [5.334, 2000.0], [7.9248, 4000.0], [3.9624, 1800.0], [None, 5700.0], [91.44, None]], ('date arrival', 'object'): ['1980/04/10', '1980/04/10', '1980/04/10', '1980/04/10', '1980/04/10', '1980/04/10'], ('function(binary)', 'object'): [bytearray(b'Leader'), bytearray(b'Espionage'), bytearray(b'Security'), bytearray(b'First Lieutenant'), bytearray(b'None'), bytearray(b'Battle Station')], ('height(ft)', 'float64'): [-28.0, 17.0, 26.0, 13.0, nan, 300.0], ('japanese name', 'float64'): [nan, nan, nan, nan, nan, nan], ('last date seen', 'object'): ['2016/09/10', '2015/08/10', '2014/07/10', '2013/06/10', '2012/05/10', '2011/04/10'], ('last position seen', 'object'): ['19.442735,-99.201111', '10.642707,-71.612534', '37.789563,-122.400356', '33.670666,-117.841553', None, None], ('rank', 'int64'): [10, 7, 7, 8, 10, 8], ('Cybertronian', 'bool'): [True, True, True, True, True, False], ('Date Type', 'datetime64[ns]'): [Timestamp('2016-09-10 00:00:00'), Timestamp('2015-08-10 00:00:00'), Timestamp('2014-06-24 00:00:00'), Timestamp('2013-06-24 00:00:00'), Timestamp('2012-05-10 00:00:00'), Timestamp('2011-04-10 00:00:00')], ('age', 'int64'): [5000000, 5000000, 5000000, 5000000, 5000000, 5000000], ('function', 'object'): ['Leader', 'Espionage', 'Security', 'First Lieutenant', 'None', 'Battle Station'], ('names', 'object'): ['Optimus', 'bumbl#ebéé  ', 'ironhide&', 'Jazz', 'Megatron', 'Metroplex_)^$'], ('timestamp', 'datetime64[ns]'): [Timestamp('2014-06-24 00:00:00'), Timestamp('2014-06-24 00:00:00'), Timestamp('2014-06-24 00:00:00'), Timestamp('2014-06-24 00:00:00'), Timestamp('2014-06-24 00:00:00'), Timestamp('2014-06-24 00:00:00')], ('weight(t)', 'float64'): [0.18638117116726624, 0.0866889168219843, 0.1733778336439686, 0.07802002513978587, 0.24706341294265527, nan]}, force_data_types=True)
        self.assertTrue(result.equals(expected, decimal=True, assertion=True))

    def test_cols_div_with_value(self):
        df = self.create_dataframe(dict={('div_test', 'float64'): [nan, nan, 5.0, 10.234, -inf, -42.0]}, force_data_types=True)
        result = df.cols.div(cols=['div_test'], value=33.5)
        expected = self.create_dataframe(dict={('div_test', 'float64'): [nan, nan, 0.14925373134328357, 0.30549253731343284, -inf, -1.2537313432835822]}, force_data_types=True)
        self.assertTrue(result.equals(expected, decimal=True, assertion=True))

    def test_cols_mul(self):
        df = self.create_dataframe(dict={('mul_test1', 'float64'): [nan, nan, 8.0, 10.234, -inf, -42.0], ('mul_test2', 'float64'): [nan, 1.0, 0.125, 703.0, inf, -321.0]}, force_data_types=True)
        result = df.cols.mul(cols=['mul_test1', 'mul_test2'])
        expected = self.create_dataframe(dict={('mul_test1', 'float64'): [nan, nan, 8.0, 10.234, -inf, -42.0], ('mul_test2', 'float64'): [nan, 1.0, 0.125, 703.0, inf, -321.0], ('mul_mul_test1_mul_test2', 'float64'): [nan, nan, 1.0, 7194.502, -inf, 13482.0]}, force_data_types=True)
        self.assertTrue(result.equals(expected, decimal=True, assertion=True))

    def test_cols_mul_2_numerics(self):
        df = self.df.cols.select(['height(ft)', 'rank'])
        result = df.cols.mul(cols=['height(ft)', 'rank'])
        expected = self.create_dataframe(dict={('height(ft)', 'float64'): [-28.0, 17.0, 26.0, 13.0, nan, 300.0], ('rank', 'int64'): [10, 7, 7, 8, 10, 8], ('mul_height(ft)_rank', 'float64'): [-280.0, 119.0, 182.0, 104.0, nan, 2400.0]}, force_data_types=True)
        self.assertTrue(result.equals(expected, decimal=True, assertion=True))

    def test_cols_mul_2_numerics_with_value(self):
        df = self.df.cols.select(['height(ft)', 'rank'])
        result = df.cols.mul(cols=['height(ft)', 'rank'], value='-3')
        expected = self.create_dataframe(dict={('height(ft)', 'float64'): [84.0, -51.0, -78.0, -39.0, nan, -900.0], ('rank', 'float64'): [-30.0, -21.0, -21.0, -24.0, -30.0, -24.0]}, force_data_types=True)
        self.assertTrue(result.equals(expected, decimal=True, assertion=True))

    def test_cols_mul_3_numerics(self):
        df = self.df.cols.select(['height(ft)', 'rank', 'age'])
        result = df.cols.mul(cols=['height(ft)', 'rank', 'age'])
        expected = self.create_dataframe(dict={('height(ft)', 'float64'): [-28.0, 17.0, 26.0, 13.0, nan, 300.0], ('rank', 'int64'): [10, 7, 7, 8, 10, 8], ('age', 'int64'): [5000000, 5000000, 5000000, 5000000, 5000000, 5000000], ('mul_height(ft)_rank_age', 'float64'): [-1400000000.0, 595000000.0, 910000000.0, 520000000.0, nan, 12000000000.0]}, force_data_types=True)
        self.assertTrue(result.equals(expected, decimal=True, assertion=True))

    def test_cols_mul_3_numerics_with_value(self):
        df = self.df.cols.select(['height(ft)', 'rank', 'age'])
        result = df.cols.mul(cols=['height(ft)', 'rank', 'age'], value=inf)
        expected = self.create_dataframe(dict={('height(ft)', 'float64'): [-inf, inf, inf, inf, nan, inf], ('rank', 'float64'): [inf, inf, inf, inf, inf, inf], ('age', 'float64'): [inf, inf, inf, inf, inf, inf]}, force_data_types=True)
        self.assertTrue(result.equals(expected, decimal=True, assertion=True))

    def test_cols_mul_all(self):
        df = self.df
        result = df.cols.mul(cols='*')
        expected = self.create_dataframe(dict={('NullType', 'object'): [None, None, None, None, None, None], ('attributes', 'object'): [[8.5344, 4300.0], [5.334, 2000.0], [7.9248, 4000.0], [3.9624, 1800.0], [None, 5700.0], [91.44, None]], ('date arrival', 'object'): ['1980/04/10', '1980/04/10', '1980/04/10', '1980/04/10', '1980/04/10', '1980/04/10'], ('function(binary)', 'object'): [bytearray(b'Leader'), bytearray(b'Espionage'), bytearray(b'Security'), bytearray(b'First Lieutenant'), bytearray(b'None'), bytearray(b'Battle Station')], ('height(ft)', 'float64'): [-28.0, 17.0, 26.0, 13.0, nan, 300.0], ('japanese name', 'object'): [['Inochi', 'Convoy'], ['Bumble', 'Goldback'], ['Roadbuster'], ['Meister'], ['Megatron'], ['Metroflex']], ('last date seen', 'object'): ['2016/09/10', '2015/08/10', '2014/07/10', '2013/06/10', '2012/05/10', '2011/04/10'], ('last position seen', 'object'): ['19.442735,-99.201111', '10.642707,-71.612534', '37.789563,-122.400356', '33.670666,-117.841553', None, None], ('rank', 'int64'): [10, 7, 7, 8, 10, 8], ('Cybertronian', 'bool'): [True, True, True, True, True, False], ('Date Type', 'datetime64[ns]'): [Timestamp('2016-09-10 00:00:00'), Timestamp('2015-08-10 00:00:00'), Timestamp('2014-06-24 00:00:00'), Timestamp('2013-06-24 00:00:00'), Timestamp('2012-05-10 00:00:00'), Timestamp('2011-04-10 00:00:00')], ('age', 'int64'): [5000000, 5000000, 5000000, 5000000, 5000000, 5000000], ('function', 'object'): ['Leader', 'Espionage', 'Security', 'First Lieutenant', 'None', 'Battle Station'], ('names', 'object'): ['Optimus', 'bumbl#ebéé  ', 'ironhide&', 'Jazz', 'Megatron', 'Metroplex_)^$'], ('timestamp', 'datetime64[ns]'): [Timestamp('2014-06-24 00:00:00'), Timestamp('2014-06-24 00:00:00'), Timestamp('2014-06-24 00:00:00'), Timestamp('2014-06-24 00:00:00'), Timestamp('2014-06-24 00:00:00'), Timestamp('2014-06-24 00:00:00')], ('weight(t)', 'float64'): [4.3, 2.0, 4.0, 1.8, 5.7, nan], ('mul_*', 'float64'): [nan, nan, nan, nan, nan, nan]}, force_data_types=True)
        self.assertTrue(result.equals(expected, decimal=True, assertion=True))

    def test_cols_mul_all_numerics(self):
        df = self.df.cols.select(['height(ft)', 'rank', 'age', 'weight(t)'])
        result = df.cols.mul(cols=['height(ft)', 'rank', 'age', 'weight(t)'])
        expected = self.create_dataframe(dict={('height(ft)', 'float64'): [-28.0, 17.0, 26.0, 13.0, nan, 300.0], ('rank', 'int64'): [10, 7, 7, 8, 10, 8], ('age', 'int64'): [5000000, 5000000, 5000000, 5000000, 5000000, 5000000], ('weight(t)', 'float64'): [4.3, 2.0, 4.0, 1.8, 5.7, nan], ('mul_height(ft)_rank_age_weight(t)', 'float64'): [-6020000000.0, 1190000000.0, 3640000000.0, 936000000.0, nan, nan]}, force_data_types=True)
        self.assertTrue(result.equals(expected, decimal=True, assertion=True))

    def test_cols_mul_all_numerics_with_value(self):
        df = self.df.cols.select(['height(ft)', 'rank', 'age', 'weight(t)'])
        result = df.cols.mul(cols=['height(ft)', 'rank', 'age', 'weight(t)'], value=nan)
        expected = self.create_dataframe(dict={('height(ft)', 'float64'): [nan, nan, nan, nan, nan, nan], ('rank', 'float64'): [nan, nan, nan, nan, nan, nan], ('age', 'float64'): [nan, nan, nan, nan, nan, nan], ('weight(t)', 'float64'): [nan, nan, nan, nan, nan, nan]}, force_data_types=True)
        self.assertTrue(result.equals(expected, decimal=True, assertion=True))

    def test_cols_mul_all_with_value(self):
        df = self.df
        result = df.cols.mul(cols='*', value=10.0)
        expected = self.create_dataframe(dict={('NullType', 'object'): [None, None, None, None, None, None], ('attributes', 'object'): [[8.5344, 4300.0], [5.334, 2000.0], [7.9248, 4000.0], [3.9624, 1800.0], [None, 5700.0], [91.44, None]], ('date arrival', 'object'): ['1980/04/10', '1980/04/10', '1980/04/10', '1980/04/10', '1980/04/10', '1980/04/10'], ('function(binary)', 'object'): [bytearray(b'Leader'), bytearray(b'Espionage'), bytearray(b'Security'), bytearray(b'First Lieutenant'), bytearray(b'None'), bytearray(b'Battle Station')], ('height(ft)', 'float64'): [-28.0, 17.0, 26.0, 13.0, nan, 300.0], ('japanese name', 'object'): [['Inochi', 'Convoy'], ['Bumble', 'Goldback'], ['Roadbuster'], ['Meister'], ['Megatron'], ['Metroflex']], ('last date seen', 'object'): ['2016/09/10', '2015/08/10', '2014/07/10', '2013/06/10', '2012/05/10', '2011/04/10'], ('last position seen', 'object'): ['19.442735,-99.201111', '10.642707,-71.612534', '37.789563,-122.400356', '33.670666,-117.841553', None, None], ('rank', 'int64'): [10, 7, 7, 8, 10, 8], ('Cybertronian', 'bool'): [True, True, True, True, True, False], ('Date Type', 'datetime64[ns]'): [Timestamp('2016-09-10 00:00:00'), Timestamp('2015-08-10 00:00:00'), Timestamp('2014-06-24 00:00:00'), Timestamp('2013-06-24 00:00:00'), Timestamp('2012-05-10 00:00:00'), Timestamp('2011-04-10 00:00:00')], ('age', 'int64'): [5000000, 5000000, 5000000, 5000000, 5000000, 5000000], ('function', 'object'): ['Leader', 'Espionage', 'Security', 'First Lieutenant', 'None', 'Battle Station'], ('names', 'object'): ['Optimus', 'bumbl#ebéé  ', 'ironhide&', 'Jazz', 'Megatron', 'Metroplex_)^$'], ('timestamp', 'datetime64[ns]'): [Timestamp('2014-06-24 00:00:00'), Timestamp('2014-06-24 00:00:00'), Timestamp('2014-06-24 00:00:00'), Timestamp('2014-06-24 00:00:00'), Timestamp('2014-06-24 00:00:00'), Timestamp('2014-06-24 00:00:00')], ('weight(t)', 'float64'): [4.3, 2.0, 4.0, 1.8, 5.7, nan], ('*', 'float64'): [nan, nan, nan, nan, nan, nan]}, force_data_types=True)
        self.assertTrue(result.equals(expected, decimal=True, assertion=True))

    def test_cols_mul_string(self):
        df = self.df.cols.select(['names', 'function'])
        result = df.cols.mul(cols=['names', 'function'], output_col='names*function')
        expected = self.create_dataframe(dict={('names', 'object'): ['Optimus', 'bumbl#ebéé  ', 'ironhide&', 'Jazz', 'Megatron', 'Metroplex_)^$'], ('function', 'object'): ['Leader', 'Espionage', 'Security', 'First Lieutenant', 'None', 'Battle Station'], ('names*function', 'float64'): [nan, nan, nan, nan, nan, nan]}, force_data_types=True)
        self.assertTrue(result.equals(expected, decimal=True, assertion=True))

    def test_cols_mul_string_with_value(self):
        df = self.df.cols.select(['names', 'function'])
        result = df.cols.mul(cols=['names', 'function'], value=103, output_col='names*function')
        expected = self.create_dataframe(dict={('names', 'float64'): [nan, nan, nan, nan, nan, nan], ('function', 'float64'): [nan, nan, nan, nan, nan, nan]}, force_data_types=True)
        self.assertTrue(result.equals(expected, decimal=True, assertion=True))

    def test_cols_mul_various_types(self):
        df = self.df
        result = df.cols.mul(cols=['NullType', 'weight(t)', 'japanese name'], output_col='nt*wt*jn')
        expected = self.create_dataframe(dict={('NullType', 'object'): [None, None, None, None, None, None], ('attributes', 'object'): [[8.5344, 4300.0], [5.334, 2000.0], [7.9248, 4000.0], [3.9624, 1800.0], [None, 5700.0], [91.44, None]], ('date arrival', 'object'): ['1980/04/10', '1980/04/10', '1980/04/10', '1980/04/10', '1980/04/10', '1980/04/10'], ('function(binary)', 'object'): [bytearray(b'Leader'), bytearray(b'Espionage'), bytearray(b'Security'), bytearray(b'First Lieutenant'), bytearray(b'None'), bytearray(b'Battle Station')], ('height(ft)', 'float64'): [-28.0, 17.0, 26.0, 13.0, nan, 300.0], ('japanese name', 'object'): [['Inochi', 'Convoy'], ['Bumble', 'Goldback'], ['Roadbuster'], ['Meister'], ['Megatron'], ['Metroflex']], ('last date seen', 'object'): ['2016/09/10', '2015/08/10', '2014/07/10', '2013/06/10', '2012/05/10', '2011/04/10'], ('last position seen', 'object'): ['19.442735,-99.201111', '10.642707,-71.612534', '37.789563,-122.400356', '33.670666,-117.841553', None, None], ('rank', 'int64'): [10, 7, 7, 8, 10, 8], ('Cybertronian', 'bool'): [True, True, True, True, True, False], ('Date Type', 'datetime64[ns]'): [Timestamp('2016-09-10 00:00:00'), Timestamp('2015-08-10 00:00:00'), Timestamp('2014-06-24 00:00:00'), Timestamp('2013-06-24 00:00:00'), Timestamp('2012-05-10 00:00:00'), Timestamp('2011-04-10 00:00:00')], ('age', 'int64'): [5000000, 5000000, 5000000, 5000000, 5000000, 5000000], ('function', 'object'): ['Leader', 'Espionage', 'Security', 'First Lieutenant', 'None', 'Battle Station'], ('names', 'object'): ['Optimus', 'bumbl#ebéé  ', 'ironhide&', 'Jazz', 'Megatron', 'Metroplex_)^$'], ('timestamp', 'datetime64[ns]'): [Timestamp('2014-06-24 00:00:00'), Timestamp('2014-06-24 00:00:00'), Timestamp('2014-06-24 00:00:00'), Timestamp('2014-06-24 00:00:00'), Timestamp('2014-06-24 00:00:00'), Timestamp('2014-06-24 00:00:00')], ('weight(t)', 'float64'): [4.3, 2.0, 4.0, 1.8, 5.7, nan], ('nt*wt*jn', 'float64'): [nan, nan, nan, nan, nan, nan]}, force_data_types=True)
        self.assertTrue(result.equals(expected, decimal=True, assertion=True))

    def test_cols_mul_various_types_with_value(self):
        df = self.df
        result = df.cols.mul(cols=['NullType', 'weight(t)', 'japanese name'], value=23.071, output_col='nt*wt*jn')
        expected = self.create_dataframe(dict={('NullType', 'float64'): [nan, nan, nan, nan, nan, nan], ('attributes', 'object'): [[8.5344, 4300.0], [5.334, 2000.0], [7.9248, 4000.0], [3.9624, 1800.0], [None, 5700.0], [91.44, None]], ('date arrival', 'object'): ['1980/04/10', '1980/04/10', '1980/04/10', '1980/04/10', '1980/04/10', '1980/04/10'], ('function(binary)', 'object'): [bytearray(b'Leader'), bytearray(b'Espionage'), bytearray(b'Security'), bytearray(b'First Lieutenant'), bytearray(b'None'), bytearray(b'Battle Station')], ('height(ft)', 'float64'): [-28.0, 17.0, 26.0, 13.0, nan, 300.0], ('japanese name', 'float64'): [nan, nan, nan, nan, nan, nan], ('last date seen', 'object'): ['2016/09/10', '2015/08/10', '2014/07/10', '2013/06/10', '2012/05/10', '2011/04/10'], ('last position seen', 'object'): ['19.442735,-99.201111', '10.642707,-71.612534', '37.789563,-122.400356', '33.670666,-117.841553', None, None], ('rank', 'int64'): [10, 7, 7, 8, 10, 8], ('Cybertronian', 'bool'): [True, True, True, True, True, False], ('Date Type', 'datetime64[ns]'): [Timestamp('2016-09-10 00:00:00'), Timestamp('2015-08-10 00:00:00'), Timestamp('2014-06-24 00:00:00'), Timestamp('2013-06-24 00:00:00'), Timestamp('2012-05-10 00:00:00'), Timestamp('2011-04-10 00:00:00')], ('age', 'int64'): [5000000, 5000000, 5000000, 5000000, 5000000, 5000000], ('function', 'object'): ['Leader', 'Espionage', 'Security', 'First Lieutenant', 'None', 'Battle Station'], ('names', 'object'): ['Optimus', 'bumbl#ebéé  ', 'ironhide&', 'Jazz', 'Megatron', 'Metroplex_)^$'], ('timestamp', 'datetime64[ns]'): [Timestamp('2014-06-24 00:00:00'), Timestamp('2014-06-24 00:00:00'), Timestamp('2014-06-24 00:00:00'), Timestamp('2014-06-24 00:00:00'), Timestamp('2014-06-24 00:00:00'), Timestamp('2014-06-24 00:00:00')], ('weight(t)', 'float64'): [99.20530000000001, 46.142, 92.284, 41.527800000000006, 131.5047, nan]}, force_data_types=True)
        self.assertTrue(result.equals(expected, decimal=True, assertion=True))

    def test_cols_mul_with_value(self):
        df = self.create_dataframe(dict={('mul_test', 'float64'): [nan, nan, 5.0, 10.234, -inf, -42.0]}, force_data_types=True)
        result = df.cols.mul(cols=['mul_test'], value=33.5)
        expected = self.create_dataframe(dict={('mul_test', 'float64'): [nan, nan, 167.5, 342.839, -inf, -1407.0]}, force_data_types=True)
        self.assertTrue(result.equals(expected, decimal=True, assertion=True))

    def test_cols_rdiv(self):
        df = self.create_dataframe(dict={('rdiv_test1', 'float64'): [nan, nan, -8.0, 10.234, -inf, -42.0], ('rdiv_test2', 'float64'): [nan, 1.0, 0.0, 703.0, inf, -321.0]}, force_data_types=True)
        result = df.cols.rdiv(cols=['rdiv_test1', 'rdiv_test2'])
        expected = self.create_dataframe(dict={('rdiv_test1', 'float64'): [nan, nan, -8.0, 10.234, -inf, -42.0], ('rdiv_test2', 'float64'): [nan, 1.0, 0.0, 703.0, inf, -321.0], ('rdiv_rdiv_test1_rdiv_test2', 'float64'): [nan, nan, -0.0, 68.69259331639633, nan, 7.642857142857143]}, force_data_types=True)
        self.assertTrue(result.equals(expected, decimal=True, assertion=True))

    def test_cols_rdiv_2_numerics(self):
        df = self.df.cols.select(['height(ft)', 'rank'])
        result = df.cols.rdiv(cols=['height(ft)', 'rank'])
        expected = self.create_dataframe(dict={('height(ft)', 'float64'): [-28.0, 17.0, 26.0, 13.0, nan, 300.0], ('rank', 'int64'): [10, 7, 7, 8, 10, 8], ('rdiv_height(ft)_rank', 'float64'): [-0.35714285714285715, 0.4117647058823529, 0.2692307692307692, 0.6153846153846154, nan, 0.02666666666666667]}, force_data_types=True)
        self.assertTrue(result.equals(expected, decimal=True, assertion=True))

    def test_cols_rdiv_2_numerics_with_value(self):
        df = self.df.cols.select(['height(ft)', 'rank'])
        result = df.cols.rdiv(cols=['height(ft)', 'rank'], value='0')
        expected = self.create_dataframe(dict={('height(ft)', 'float64'): [-0.0, 0.0, 0.0, 0.0, nan, 0.0], ('rank', 'float64'): [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]}, force_data_types=True)
        self.assertTrue(result.equals(expected, decimal=True, assertion=True))

    def test_cols_rdiv_3_numerics(self):
        df = self.df.cols.select(['height(ft)', 'rank', 'age'])
        result = df.cols.rdiv(cols=['height(ft)', 'rank', 'age'])
        expected = self.create_dataframe(dict={('height(ft)', 'float64'): [-28.0, 17.0, 26.0, 13.0, nan, 300.0], ('rank', 'int64'): [10, 7, 7, 8, 10, 8], ('age', 'int64'): [5000000, 5000000, 5000000, 5000000, 5000000, 5000000], ('rdiv_height(ft)_rank_age', 'float64'): [-14000000.0, 12142857.142857144, 18571428.57142857, 8125000.0, nan, 187500000.0]}, force_data_types=True)
        self.assertTrue(result.equals(expected, decimal=True, assertion=True))

    def test_cols_rdiv_3_numerics_with_value(self):
        df = self.df.cols.select(['height(ft)', 'rank', 'age'])
        result = df.cols.rdiv(cols=['height(ft)', 'rank', 'age'], value=inf)
        expected = self.create_dataframe(dict={('height(ft)', 'float64'): [-inf, inf, inf, inf, nan, inf], ('rank', 'float64'): [inf, inf, inf, inf, inf, inf], ('age', 'float64'): [inf, inf, inf, inf, inf, inf]}, force_data_types=True)
        self.assertTrue(result.equals(expected, decimal=True, assertion=True))

    def test_cols_rdiv_all(self):
        df = self.df
        result = df.cols.rdiv(cols='*')
        expected = self.create_dataframe(dict={('NullType', 'object'): [None, None, None, None, None, None], ('attributes', 'object'): [[8.5344, 4300.0], [5.334, 2000.0], [7.9248, 4000.0], [3.9624, 1800.0], [None, 5700.0], [91.44, None]], ('date arrival', 'object'): ['1980/04/10', '1980/04/10', '1980/04/10', '1980/04/10', '1980/04/10', '1980/04/10'], ('function(binary)', 'object'): [bytearray(b'Leader'), bytearray(b'Espionage'), bytearray(b'Security'), bytearray(b'First Lieutenant'), bytearray(b'None'), bytearray(b'Battle Station')], ('height(ft)', 'float64'): [-28.0, 17.0, 26.0, 13.0, nan, 300.0], ('japanese name', 'object'): [['Inochi', 'Convoy'], ['Bumble', 'Goldback'], ['Roadbuster'], ['Meister'], ['Megatron'], ['Metroflex']], ('last date seen', 'object'): ['2016/09/10', '2015/08/10', '2014/07/10', '2013/06/10', '2012/05/10', '2011/04/10'], ('last position seen', 'object'): ['19.442735,-99.201111', '10.642707,-71.612534', '37.789563,-122.400356', '33.670666,-117.841553', None, None], ('rank', 'int64'): [10, 7, 7, 8, 10, 8], ('Cybertronian', 'bool'): [True, True, True, True, True, False], ('Date Type', 'datetime64[ns]'): [Timestamp('2016-09-10 00:00:00'), Timestamp('2015-08-10 00:00:00'), Timestamp('2014-06-24 00:00:00'), Timestamp('2013-06-24 00:00:00'), Timestamp('2012-05-10 00:00:00'), Timestamp('2011-04-10 00:00:00')], ('age', 'int64'): [5000000, 5000000, 5000000, 5000000, 5000000, 5000000], ('function', 'object'): ['Leader', 'Espionage', 'Security', 'First Lieutenant', 'None', 'Battle Station'], ('names', 'object'): ['Optimus', 'bumbl#ebéé  ', 'ironhide&', 'Jazz', 'Megatron', 'Metroplex_)^$'], ('timestamp', 'datetime64[ns]'): [Timestamp('2014-06-24 00:00:00'), Timestamp('2014-06-24 00:00:00'), Timestamp('2014-06-24 00:00:00'), Timestamp('2014-06-24 00:00:00'), Timestamp('2014-06-24 00:00:00'), Timestamp('2014-06-24 00:00:00')], ('weight(t)', 'float64'): [4.3, 2.0, 4.0, 1.8, 5.7, nan], ('rdiv_*', 'float64'): [nan, nan, nan, nan, nan, nan]}, force_data_types=True)
        self.assertTrue(result.equals(expected, decimal=True, assertion=True))

    def test_cols_rdiv_all_numerics(self):
        df = self.df.cols.select(['height(ft)', 'rank', 'age', 'weight(t)'])
        result = df.cols.rdiv(cols=['height(ft)', 'rank', 'age', 'weight(t)'])
        expected = self.create_dataframe(dict={('height(ft)', 'float64'): [-28.0, 17.0, 26.0, 13.0, nan, 300.0], ('rank', 'int64'): [10, 7, 7, 8, 10, 8], ('age', 'int64'): [5000000, 5000000, 5000000, 5000000, 5000000, 5000000], ('weight(t)', 'float64'): [4.3, 2.0, 4.0, 1.8, 5.7, nan], ('rdiv_height(ft)_rank_age_weight(t)', 'float64'): [-3.071428571428571e-07, 1.6470588235294117e-07, 2.153846153846154e-07, 2.2153846153846153e-07, nan, nan]}, force_data_types=True)
        self.assertTrue(result.equals(expected, decimal=True, assertion=True))

    def test_cols_rdiv_all_numerics_with_value(self):
        df = self.df.cols.select(['height(ft)', 'rank', 'age', 'weight(t)'])
        result = df.cols.rdiv(cols=['height(ft)', 'rank', 'age', 'weight(t)'], value=nan)
        expected = self.create_dataframe(dict={('height(ft)', 'float64'): [nan, nan, nan, nan, nan, nan], ('rank', 'float64'): [nan, nan, nan, nan, nan, nan], ('age', 'float64'): [nan, nan, nan, nan, nan, nan], ('weight(t)', 'float64'): [nan, nan, nan, nan, nan, nan]}, force_data_types=True)
        self.assertTrue(result.equals(expected, decimal=True, assertion=True))

    def test_cols_rdiv_all_with_value(self):
        df = self.df
        result = df.cols.rdiv(cols='*', value=10.0)
        expected = self.create_dataframe(dict={('NullType', 'object'): [None, None, None, None, None, None], ('attributes', 'object'): [[8.5344, 4300.0], [5.334, 2000.0], [7.9248, 4000.0], [3.9624, 1800.0], [None, 5700.0], [91.44, None]], ('date arrival', 'object'): ['1980/04/10', '1980/04/10', '1980/04/10', '1980/04/10', '1980/04/10', '1980/04/10'], ('function(binary)', 'object'): [bytearray(b'Leader'), bytearray(b'Espionage'), bytearray(b'Security'), bytearray(b'First Lieutenant'), bytearray(b'None'), bytearray(b'Battle Station')], ('height(ft)', 'float64'): [-28.0, 17.0, 26.0, 13.0, nan, 300.0], ('japanese name', 'object'): [['Inochi', 'Convoy'], ['Bumble', 'Goldback'], ['Roadbuster'], ['Meister'], ['Megatron'], ['Metroflex']], ('last date seen', 'object'): ['2016/09/10', '2015/08/10', '2014/07/10', '2013/06/10', '2012/05/10', '2011/04/10'], ('last position seen', 'object'): ['19.442735,-99.201111', '10.642707,-71.612534', '37.789563,-122.400356', '33.670666,-117.841553', None, None], ('rank', 'int64'): [10, 7, 7, 8, 10, 8], ('Cybertronian', 'bool'): [True, True, True, True, True, False], ('Date Type', 'datetime64[ns]'): [Timestamp('2016-09-10 00:00:00'), Timestamp('2015-08-10 00:00:00'), Timestamp('2014-06-24 00:00:00'), Timestamp('2013-06-24 00:00:00'), Timestamp('2012-05-10 00:00:00'), Timestamp('2011-04-10 00:00:00')], ('age', 'int64'): [5000000, 5000000, 5000000, 5000000, 5000000, 5000000], ('function', 'object'): ['Leader', 'Espionage', 'Security', 'First Lieutenant', 'None', 'Battle Station'], ('names', 'object'): ['Optimus', 'bumbl#ebéé  ', 'ironhide&', 'Jazz', 'Megatron', 'Metroplex_)^$'], ('timestamp', 'datetime64[ns]'): [Timestamp('2014-06-24 00:00:00'), Timestamp('2014-06-24 00:00:00'), Timestamp('2014-06-24 00:00:00'), Timestamp('2014-06-24 00:00:00'), Timestamp('2014-06-24 00:00:00'), Timestamp('2014-06-24 00:00:00')], ('weight(t)', 'float64'): [4.3, 2.0, 4.0, 1.8, 5.7, nan], ('*', 'float64'): [nan, nan, nan, nan, nan, nan]}, force_data_types=True)
        self.assertTrue(result.equals(expected, decimal=True, assertion=True))

    def test_cols_rdiv_string(self):
        df = self.df.cols.select(['names', 'function'])
        result = df.cols.rdiv(cols=['names', 'function'], output_col='names*function')
        expected = self.create_dataframe(dict={('names', 'object'): ['Optimus', 'bumbl#ebéé  ', 'ironhide&', 'Jazz', 'Megatron', 'Metroplex_)^$'], ('function', 'object'): ['Leader', 'Espionage', 'Security', 'First Lieutenant', 'None', 'Battle Station'], ('names*function', 'float64'): [nan, nan, nan, nan, nan, nan]}, force_data_types=True)
        self.assertTrue(result.equals(expected, decimal=True, assertion=True))

    def test_cols_rdiv_string_with_value(self):
        df = self.df.cols.select(['names', 'function'])
        result = df.cols.rdiv(cols=['names', 'function'], value=103, output_col='names*function')
        expected = self.create_dataframe(dict={('names', 'float64'): [nan, nan, nan, nan, nan, nan], ('function', 'float64'): [nan, nan, nan, nan, nan, nan]}, force_data_types=True)
        self.assertTrue(result.equals(expected, decimal=True, assertion=True))

    def test_cols_rdiv_various_types(self):
        df = self.df
        result = df.cols.rdiv(cols=['NullType', 'weight(t)', 'japanese name'], output_col='nt*wt*jn')
        expected = self.create_dataframe(dict={('NullType', 'object'): [None, None, None, None, None, None], ('attributes', 'object'): [[8.5344, 4300.0], [5.334, 2000.0], [7.9248, 4000.0], [3.9624, 1800.0], [None, 5700.0], [91.44, None]], ('date arrival', 'object'): ['1980/04/10', '1980/04/10', '1980/04/10', '1980/04/10', '1980/04/10', '1980/04/10'], ('function(binary)', 'object'): [bytearray(b'Leader'), bytearray(b'Espionage'), bytearray(b'Security'), bytearray(b'First Lieutenant'), bytearray(b'None'), bytearray(b'Battle Station')], ('height(ft)', 'float64'): [-28.0, 17.0, 26.0, 13.0, nan, 300.0], ('japanese name', 'object'): [['Inochi', 'Convoy'], ['Bumble', 'Goldback'], ['Roadbuster'], ['Meister'], ['Megatron'], ['Metroflex']], ('last date seen', 'object'): ['2016/09/10', '2015/08/10', '2014/07/10', '2013/06/10', '2012/05/10', '2011/04/10'], ('last position seen', 'object'): ['19.442735,-99.201111', '10.642707,-71.612534', '37.789563,-122.400356', '33.670666,-117.841553', None, None], ('rank', 'int64'): [10, 7, 7, 8, 10, 8], ('Cybertronian', 'bool'): [True, True, True, True, True, False], ('Date Type', 'datetime64[ns]'): [Timestamp('2016-09-10 00:00:00'), Timestamp('2015-08-10 00:00:00'), Timestamp('2014-06-24 00:00:00'), Timestamp('2013-06-24 00:00:00'), Timestamp('2012-05-10 00:00:00'), Timestamp('2011-04-10 00:00:00')], ('age', 'int64'): [5000000, 5000000, 5000000, 5000000, 5000000, 5000000], ('function', 'object'): ['Leader', 'Espionage', 'Security', 'First Lieutenant', 'None', 'Battle Station'], ('names', 'object'): ['Optimus', 'bumbl#ebéé  ', 'ironhide&', 'Jazz', 'Megatron', 'Metroplex_)^$'], ('timestamp', 'datetime64[ns]'): [Timestamp('2014-06-24 00:00:00'), Timestamp('2014-06-24 00:00:00'), Timestamp('2014-06-24 00:00:00'), Timestamp('2014-06-24 00:00:00'), Timestamp('2014-06-24 00:00:00'), Timestamp('2014-06-24 00:00:00')], ('weight(t)', 'float64'): [4.3, 2.0, 4.0, 1.8, 5.7, nan], ('nt*wt*jn', 'float64'): [nan, nan, nan, nan, nan, nan]}, force_data_types=True)
        self.assertTrue(result.equals(expected, decimal=True, assertion=True))

    def test_cols_rdiv_various_types_with_value(self):
        df = self.df
        result = df.cols.rdiv(cols=['NullType', 'weight(t)', 'japanese name'], value=23.071, output_col='nt*wt*jn')
        expected = self.create_dataframe(dict={('NullType', 'float64'): [nan, nan, nan, nan, nan, nan], ('attributes', 'object'): [[8.5344, 4300.0], [5.334, 2000.0], [7.9248, 4000.0], [3.9624, 1800.0], [None, 5700.0], [91.44, None]], ('date arrival', 'object'): ['1980/04/10', '1980/04/10', '1980/04/10', '1980/04/10', '1980/04/10', '1980/04/10'], ('function(binary)', 'object'): [bytearray(b'Leader'), bytearray(b'Espionage'), bytearray(b'Security'), bytearray(b'First Lieutenant'), bytearray(b'None'), bytearray(b'Battle Station')], ('height(ft)', 'float64'): [-28.0, 17.0, 26.0, 13.0, nan, 300.0], ('japanese name', 'float64'): [nan, nan, nan, nan, nan, nan], ('last date seen', 'object'): ['2016/09/10', '2015/08/10', '2014/07/10', '2013/06/10', '2012/05/10', '2011/04/10'], ('last position seen', 'object'): ['19.442735,-99.201111', '10.642707,-71.612534', '37.789563,-122.400356', '33.670666,-117.841553', None, None], ('rank', 'int64'): [10, 7, 7, 8, 10, 8], ('Cybertronian', 'bool'): [True, True, True, True, True, False], ('Date Type', 'datetime64[ns]'): [Timestamp('2016-09-10 00:00:00'), Timestamp('2015-08-10 00:00:00'), Timestamp('2014-06-24 00:00:00'), Timestamp('2013-06-24 00:00:00'), Timestamp('2012-05-10 00:00:00'), Timestamp('2011-04-10 00:00:00')], ('age', 'int64'): [5000000, 5000000, 5000000, 5000000, 5000000, 5000000], ('function', 'object'): ['Leader', 'Espionage', 'Security', 'First Lieutenant', 'None', 'Battle Station'], ('names', 'object'): ['Optimus', 'bumbl#ebéé  ', 'ironhide&', 'Jazz', 'Megatron', 'Metroplex_)^$'], ('timestamp', 'datetime64[ns]'): [Timestamp('2014-06-24 00:00:00'), Timestamp('2014-06-24 00:00:00'), Timestamp('2014-06-24 00:00:00'), Timestamp('2014-06-24 00:00:00'), Timestamp('2014-06-24 00:00:00'), Timestamp('2014-06-24 00:00:00')], ('weight(t)', 'float64'): [5.365348837209303, 11.5355, 5.76775, 12.817222222222222, 4.047543859649123, nan]}, force_data_types=True)
        self.assertTrue(result.equals(expected, decimal=True, assertion=True))

    def test_cols_rdiv_with_value(self):
        df = self.create_dataframe(dict={('rdiv_test', 'float64'): [nan, nan, 5.0, 10.234, -inf, -42.0]}, force_data_types=True)
        result = df.cols.rdiv(cols=['rdiv_test'], value=33.5)
        expected = self.create_dataframe(dict={('rdiv_test', 'float64'): [nan, nan, 6.7, 3.273402384209498, -0.0, -0.7976190476190477]}, force_data_types=True)
        self.assertTrue(result.equals(expected, decimal=True, assertion=True))

    def test_cols_sub(self):
        df = self.create_dataframe(dict={('sub_test1', 'float64'): [nan, nan, 9.0, 10.234, inf, -42.0], ('sub_test2', 'float64'): [nan, 1.0, 9.0, 703.0, inf, -321.0]}, force_data_types=True)
        result = df.cols.sub(cols=['sub_test1', 'sub_test2'])
        expected = self.create_dataframe(dict={('sub_test1', 'float64'): [nan, nan, 9.0, 10.234, inf, -42.0], ('sub_test2', 'float64'): [nan, 1.0, 9.0, 703.0, inf, -321.0], ('sub_sub_test1_sub_test2', 'float64'): [nan, nan, 0.0, -692.766, nan, 279.0]}, force_data_types=True)
        self.assertTrue(result.equals(expected, decimal=True, assertion=True))

    def test_cols_sub_2_numerics(self):
        df = self.df.cols.select(['height(ft)', 'rank'])
        result = df.cols.sub(cols=['height(ft)', 'rank'])
        expected = self.create_dataframe(dict={('height(ft)', 'float64'): [-28.0, 17.0, 26.0, 13.0, nan, 300.0], ('rank', 'int64'): [10, 7, 7, 8, 10, 8], ('sub_height(ft)_rank', 'float64'): [-38.0, 10.0, 19.0, 5.0, nan, 292.0]}, force_data_types=True)
        self.assertTrue(result.equals(expected, decimal=True, assertion=True))

    def test_cols_sub_2_numerics_with_value(self):
        df = self.df.cols.select(['height(ft)', 'rank'])
        result = df.cols.sub(cols=['height(ft)', 'rank'], value='-3')
        expected = self.create_dataframe(dict={('height(ft)', 'float64'): [-25.0, 20.0, 29.0, 16.0, nan, 303.0], ('rank', 'float64'): [13.0, 10.0, 10.0, 11.0, 13.0, 11.0]}, force_data_types=True)
        self.assertTrue(result.equals(expected, decimal=True, assertion=True))

    def test_cols_sub_3_numerics(self):
        df = self.df.cols.select(['height(ft)', 'rank', 'age'])
        result = df.cols.sub(cols=['height(ft)', 'rank', 'age'])
        expected = self.create_dataframe(dict={('height(ft)', 'float64'): [-28.0, 17.0, 26.0, 13.0, nan, 300.0], ('rank', 'int64'): [10, 7, 7, 8, 10, 8], ('age', 'int64'): [5000000, 5000000, 5000000, 5000000, 5000000, 5000000], ('sub_height(ft)_rank_age', 'float64'): [-5000038.0, -4999990.0, -4999981.0, -4999995.0, nan, -4999708.0]}, force_data_types=True)
        self.assertTrue(result.equals(expected, decimal=True, assertion=True))

    def test_cols_sub_3_numerics_with_value(self):
        df = self.df.cols.select(['height(ft)', 'rank', 'age'])
        result = df.cols.sub(cols=['height(ft)', 'rank', 'age'], value=inf)
        expected = self.create_dataframe(dict={('height(ft)', 'float64'): [-inf, -inf, -inf, -inf, nan, -inf], ('rank', 'float64'): [-inf, -inf, -inf, -inf, -inf, -inf], ('age', 'float64'): [-inf, -inf, -inf, -inf, -inf, -inf]}, force_data_types=True)
        self.assertTrue(result.equals(expected, decimal=True, assertion=True))

    def test_cols_sub_all(self):
        df = self.df
        result = df.cols.sub(cols='*')
        expected = self.create_dataframe(dict={('NullType', 'object'): [None, None, None, None, None, None], ('attributes', 'object'): [[8.5344, 4300.0], [5.334, 2000.0], [7.9248, 4000.0], [3.9624, 1800.0], [None, 5700.0], [91.44, None]], ('date arrival', 'object'): ['1980/04/10', '1980/04/10', '1980/04/10', '1980/04/10', '1980/04/10', '1980/04/10'], ('function(binary)', 'object'): [bytearray(b'Leader'), bytearray(b'Espionage'), bytearray(b'Security'), bytearray(b'First Lieutenant'), bytearray(b'None'), bytearray(b'Battle Station')], ('height(ft)', 'float64'): [-28.0, 17.0, 26.0, 13.0, nan, 300.0], ('japanese name', 'object'): [['Inochi', 'Convoy'], ['Bumble', 'Goldback'], ['Roadbuster'], ['Meister'], ['Megatron'], ['Metroflex']], ('last date seen', 'object'): ['2016/09/10', '2015/08/10', '2014/07/10', '2013/06/10', '2012/05/10', '2011/04/10'], ('last position seen', 'object'): ['19.442735,-99.201111', '10.642707,-71.612534', '37.789563,-122.400356', '33.670666,-117.841553', None, None], ('rank', 'int64'): [10, 7, 7, 8, 10, 8], ('Cybertronian', 'bool'): [True, True, True, True, True, False], ('Date Type', 'datetime64[ns]'): [Timestamp('2016-09-10 00:00:00'), Timestamp('2015-08-10 00:00:00'), Timestamp('2014-06-24 00:00:00'), Timestamp('2013-06-24 00:00:00'), Timestamp('2012-05-10 00:00:00'), Timestamp('2011-04-10 00:00:00')], ('age', 'int64'): [5000000, 5000000, 5000000, 5000000, 5000000, 5000000], ('function', 'object'): ['Leader', 'Espionage', 'Security', 'First Lieutenant', 'None', 'Battle Station'], ('names', 'object'): ['Optimus', 'bumbl#ebéé  ', 'ironhide&', 'Jazz', 'Megatron', 'Metroplex_)^$'], ('timestamp', 'datetime64[ns]'): [Timestamp('2014-06-24 00:00:00'), Timestamp('2014-06-24 00:00:00'), Timestamp('2014-06-24 00:00:00'), Timestamp('2014-06-24 00:00:00'), Timestamp('2014-06-24 00:00:00'), Timestamp('2014-06-24 00:00:00')], ('weight(t)', 'float64'): [4.3, 2.0, 4.0, 1.8, 5.7, nan], ('sub_*', 'float64'): [nan, nan, nan, nan, nan, nan]}, force_data_types=True)
        self.assertTrue(result.equals(expected, decimal=True, assertion=True))

    def test_cols_sub_all_numerics(self):
        df = self.df.cols.select(['height(ft)', 'rank', 'age', 'weight(t)'])
        result = df.cols.sub(cols=['height(ft)', 'rank', 'age', 'weight(t)'])
        expected = self.create_dataframe(dict={('height(ft)', 'float64'): [-28.0, 17.0, 26.0, 13.0, nan, 300.0], ('rank', 'int64'): [10, 7, 7, 8, 10, 8], ('age', 'int64'): [5000000, 5000000, 5000000, 5000000, 5000000, 5000000], ('weight(t)', 'float64'): [4.3, 2.0, 4.0, 1.8, 5.7, nan], ('sub_height(ft)_rank_age_weight(t)', 'float64'): [-5000042.3, -4999992.0, -4999985.0, -4999996.8, nan, nan]}, force_data_types=True)
        self.assertTrue(result.equals(expected, decimal=True, assertion=True))

    def test_cols_sub_all_numerics_with_value(self):
        df = self.df.cols.select(['height(ft)', 'rank', 'age', 'weight(t)'])
        result = df.cols.sub(cols=['height(ft)', 'rank', 'age', 'weight(t)'], value=nan)
        expected = self.create_dataframe(dict={('height(ft)', 'float64'): [nan, nan, nan, nan, nan, nan], ('rank', 'float64'): [nan, nan, nan, nan, nan, nan], ('age', 'float64'): [nan, nan, nan, nan, nan, nan], ('weight(t)', 'float64'): [nan, nan, nan, nan, nan, nan]}, force_data_types=True)
        self.assertTrue(result.equals(expected, decimal=True, assertion=True))

    def test_cols_sub_all_with_value(self):
        df = self.df
        result = df.cols.sub(cols='*', value=10.0)
        expected = self.create_dataframe(dict={('NullType', 'object'): [None, None, None, None, None, None], ('attributes', 'object'): [[8.5344, 4300.0], [5.334, 2000.0], [7.9248, 4000.0], [3.9624, 1800.0], [None, 5700.0], [91.44, None]], ('date arrival', 'object'): ['1980/04/10', '1980/04/10', '1980/04/10', '1980/04/10', '1980/04/10', '1980/04/10'], ('function(binary)', 'object'): [bytearray(b'Leader'), bytearray(b'Espionage'), bytearray(b'Security'), bytearray(b'First Lieutenant'), bytearray(b'None'), bytearray(b'Battle Station')], ('height(ft)', 'float64'): [-28.0, 17.0, 26.0, 13.0, nan, 300.0], ('japanese name', 'object'): [['Inochi', 'Convoy'], ['Bumble', 'Goldback'], ['Roadbuster'], ['Meister'], ['Megatron'], ['Metroflex']], ('last date seen', 'object'): ['2016/09/10', '2015/08/10', '2014/07/10', '2013/06/10', '2012/05/10', '2011/04/10'], ('last position seen', 'object'): ['19.442735,-99.201111', '10.642707,-71.612534', '37.789563,-122.400356', '33.670666,-117.841553', None, None], ('rank', 'int64'): [10, 7, 7, 8, 10, 8], ('Cybertronian', 'bool'): [True, True, True, True, True, False], ('Date Type', 'datetime64[ns]'): [Timestamp('2016-09-10 00:00:00'), Timestamp('2015-08-10 00:00:00'), Timestamp('2014-06-24 00:00:00'), Timestamp('2013-06-24 00:00:00'), Timestamp('2012-05-10 00:00:00'), Timestamp('2011-04-10 00:00:00')], ('age', 'int64'): [5000000, 5000000, 5000000, 5000000, 5000000, 5000000], ('function', 'object'): ['Leader', 'Espionage', 'Security', 'First Lieutenant', 'None', 'Battle Station'], ('names', 'object'): ['Optimus', 'bumbl#ebéé  ', 'ironhide&', 'Jazz', 'Megatron', 'Metroplex_)^$'], ('timestamp', 'datetime64[ns]'): [Timestamp('2014-06-24 00:00:00'), Timestamp('2014-06-24 00:00:00'), Timestamp('2014-06-24 00:00:00'), Timestamp('2014-06-24 00:00:00'), Timestamp('2014-06-24 00:00:00'), Timestamp('2014-06-24 00:00:00')], ('weight(t)', 'float64'): [4.3, 2.0, 4.0, 1.8, 5.7, nan], ('*', 'float64'): [nan, nan, nan, nan, nan, nan]}, force_data_types=True)
        self.assertTrue(result.equals(expected, decimal=True, assertion=True))

    def test_cols_sub_string(self):
        df = self.df.cols.select(['names', 'function'])
        result = df.cols.sub(cols=['names', 'function'], output_col='names-function')
        expected = self.create_dataframe(dict={('names', 'object'): ['Optimus', 'bumbl#ebéé  ', 'ironhide&', 'Jazz', 'Megatron', 'Metroplex_)^$'], ('function', 'object'): ['Leader', 'Espionage', 'Security', 'First Lieutenant', 'None', 'Battle Station'], ('names-function', 'float64'): [nan, nan, nan, nan, nan, nan]}, force_data_types=True)
        self.assertTrue(result.equals(expected, decimal=True, assertion=True))

    def test_cols_sub_string_with_value(self):
        df = self.df.cols.select(['names', 'function'])
        result = df.cols.sub(cols=['names', 'function'], value=103, output_col='names*function')
        expected = self.create_dataframe(dict={('names', 'float64'): [nan, nan, nan, nan, nan, nan], ('function', 'float64'): [nan, nan, nan, nan, nan, nan]}, force_data_types=True)
        self.assertTrue(result.equals(expected, decimal=True, assertion=True))

    def test_cols_sub_various_types(self):
        df = self.df
        result = df.cols.sub(cols=['NullType', 'weight(t)', 'japanese name'], output_col='nt-wt-jn')
        expected = self.create_dataframe(dict={('NullType', 'object'): [None, None, None, None, None, None], ('attributes', 'object'): [[8.5344, 4300.0], [5.334, 2000.0], [7.9248, 4000.0], [3.9624, 1800.0], [None, 5700.0], [91.44, None]], ('date arrival', 'object'): ['1980/04/10', '1980/04/10', '1980/04/10', '1980/04/10', '1980/04/10', '1980/04/10'], ('function(binary)', 'object'): [bytearray(b'Leader'), bytearray(b'Espionage'), bytearray(b'Security'), bytearray(b'First Lieutenant'), bytearray(b'None'), bytearray(b'Battle Station')], ('height(ft)', 'float64'): [-28.0, 17.0, 26.0, 13.0, nan, 300.0], ('japanese name', 'object'): [['Inochi', 'Convoy'], ['Bumble', 'Goldback'], ['Roadbuster'], ['Meister'], ['Megatron'], ['Metroflex']], ('last date seen', 'object'): ['2016/09/10', '2015/08/10', '2014/07/10', '2013/06/10', '2012/05/10', '2011/04/10'], ('last position seen', 'object'): ['19.442735,-99.201111', '10.642707,-71.612534', '37.789563,-122.400356', '33.670666,-117.841553', None, None], ('rank', 'int64'): [10, 7, 7, 8, 10, 8], ('Cybertronian', 'bool'): [True, True, True, True, True, False], ('Date Type', 'datetime64[ns]'): [Timestamp('2016-09-10 00:00:00'), Timestamp('2015-08-10 00:00:00'), Timestamp('2014-06-24 00:00:00'), Timestamp('2013-06-24 00:00:00'), Timestamp('2012-05-10 00:00:00'), Timestamp('2011-04-10 00:00:00')], ('age', 'int64'): [5000000, 5000000, 5000000, 5000000, 5000000, 5000000], ('function', 'object'): ['Leader', 'Espionage', 'Security', 'First Lieutenant', 'None', 'Battle Station'], ('names', 'object'): ['Optimus', 'bumbl#ebéé  ', 'ironhide&', 'Jazz', 'Megatron', 'Metroplex_)^$'], ('timestamp', 'datetime64[ns]'): [Timestamp('2014-06-24 00:00:00'), Timestamp('2014-06-24 00:00:00'), Timestamp('2014-06-24 00:00:00'), Timestamp('2014-06-24 00:00:00'), Timestamp('2014-06-24 00:00:00'), Timestamp('2014-06-24 00:00:00')], ('weight(t)', 'float64'): [4.3, 2.0, 4.0, 1.8, 5.7, nan], ('nt-wt-jn', 'float64'): [nan, nan, nan, nan, nan, nan]}, force_data_types=True)
        self.assertTrue(result.equals(expected, decimal=True, assertion=True))

    def test_cols_sub_various_types_with_value(self):
        df = self.df
        result = df.cols.sub(cols=['NullType', 'weight(t)', 'japanese name'], value=23.071, output_col='nt*wt*jn')
        expected = self.create_dataframe(dict={('NullType', 'float64'): [nan, nan, nan, nan, nan, nan], ('attributes', 'object'): [[8.5344, 4300.0], [5.334, 2000.0], [7.9248, 4000.0], [3.9624, 1800.0], [None, 5700.0], [91.44, None]], ('date arrival', 'object'): ['1980/04/10', '1980/04/10', '1980/04/10', '1980/04/10', '1980/04/10', '1980/04/10'], ('function(binary)', 'object'): [bytearray(b'Leader'), bytearray(b'Espionage'), bytearray(b'Security'), bytearray(b'First Lieutenant'), bytearray(b'None'), bytearray(b'Battle Station')], ('height(ft)', 'float64'): [-28.0, 17.0, 26.0, 13.0, nan, 300.0], ('japanese name', 'float64'): [nan, nan, nan, nan, nan, nan], ('last date seen', 'object'): ['2016/09/10', '2015/08/10', '2014/07/10', '2013/06/10', '2012/05/10', '2011/04/10'], ('last position seen', 'object'): ['19.442735,-99.201111', '10.642707,-71.612534', '37.789563,-122.400356', '33.670666,-117.841553', None, None], ('rank', 'int64'): [10, 7, 7, 8, 10, 8], ('Cybertronian', 'bool'): [True, True, True, True, True, False], ('Date Type', 'datetime64[ns]'): [Timestamp('2016-09-10 00:00:00'), Timestamp('2015-08-10 00:00:00'), Timestamp('2014-06-24 00:00:00'), Timestamp('2013-06-24 00:00:00'), Timestamp('2012-05-10 00:00:00'), Timestamp('2011-04-10 00:00:00')], ('age', 'int64'): [5000000, 5000000, 5000000, 5000000, 5000000, 5000000], ('function', 'object'): ['Leader', 'Espionage', 'Security', 'First Lieutenant', 'None', 'Battle Station'], ('names', 'object'): ['Optimus', 'bumbl#ebéé  ', 'ironhide&', 'Jazz', 'Megatron', 'Metroplex_)^$'], ('timestamp', 'datetime64[ns]'): [Timestamp('2014-06-24 00:00:00'), Timestamp('2014-06-24 00:00:00'), Timestamp('2014-06-24 00:00:00'), Timestamp('2014-06-24 00:00:00'), Timestamp('2014-06-24 00:00:00'), Timestamp('2014-06-24 00:00:00')], ('weight(t)', 'float64'): [-18.771, -21.071, -19.071, -21.271, -17.371000000000002, nan]}, force_data_types=True)
        self.assertTrue(result.equals(expected, decimal=True, assertion=True))

    def test_cols_sub_with_value(self):
        df = self.create_dataframe(dict={('sub_test', 'float64'): [nan, nan, 5.0, 10.234, -inf, -42.0]}, force_data_types=True)
        result = df.cols.sub(cols=['sub_test'], value=33.5)
        expected = self.create_dataframe(dict={('sub_test', 'float64'): [nan, nan, -28.5, -23.266, -inf, -75.5]}, force_data_types=True)
        self.assertTrue(result.equals(expected, decimal=True, assertion=True))


class TestMathDask(TestMathPandas):
    config = {'engine': 'dask', 'n_partitions': 1}


class TestMathPartitionDask(TestMathPandas):
    config = {'engine': 'dask', 'n_partitions': 2}


try:
    import cudf # pyright: reportMissingImports=false
except:
    pass
else:
    class TestMathCUDF(TestMathPandas):
        config = {'engine': 'cudf'}


try:
    import dask_cudf # pyright: reportMissingImports=false
except:
    pass
else:
    class TestMathDC(TestMathPandas):
        config = {'engine': 'dask_cudf', 'n_partitions': 1}


try:
    import dask_cudf # pyright: reportMissingImports=false
except:
    pass
else:
    class TestMathPartitionDC(TestMathPandas):
        config = {'engine': 'dask_cudf', 'n_partitions': 2}


try:
    import pyspark # pyright: reportMissingImports=false
except:
    pass
else:
    class TestMathSpark(TestMathPandas):
        config = {'engine': 'spark'}


try:
    import vaex # pyright: reportMissingImports=false
except:
    pass
else:
    class TestMathVaex(TestMathPandas):
        config = {'engine': 'vaex'}
