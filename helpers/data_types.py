
def determine_dtype_of_df_column(dataframe, col_label):
    series = dataframe[col_label].dropna()
    if str(series.dtype) == 'object':
        return ('string', series)
    elif str(series.dtype) == 'bool':
        return ('boolean', series)
    elif str(series.dtype) == 'float64':
        if set(series.values) == set([0.0, 1.0]):
            return ('boolean', series.astype('bool'))
        elif all(val.is_integer() for val in set(series.values)):
            return ('integer', series.astype('int64'))
        else:
            return ('float', series)
    elif str(series.dtype) == 'int64':
        if set(series.values) == set([0, 1]):
            return ('boolean', series.astype('bool'))
        else:
            return ('integer', series)
    else:
        return ('string', series)
