import json
import math
import numpy as np
import pandas as pd
import scipy.stats as ss


def analysis_correlation(resultfiles):
    with open(resultfiles['tourspot_visitor'], 'r', encoding='utf-8') as infile:
        json_data = json.loads(infile.read())

    tourspot_table = pd.DataFrame(json_data, columns=['count_foreigner', 'date', 'tourist_spot'])
    temp_tourspot_table = pd.DataFrame(tourspot_table.groupby('date')['count_foreigner'].sum())

    results = []
    for filename in resultfiles['foreign_visitor']:
        with open(filename, 'r', encoding='utf-8') as infile:
            json_data = json.loads(infile.read())

        foreignvisitor_table = pd.DataFrame(json_data, columns=['country_name', 'date', 'visit_count'])
        foreignvisitor_table = foreignvisitor_table.set_index('date')
        merge_table = pd.merge(temp_tourspot_table, foreignvisitor_table, left_index=True, right_index=True)

        x = list(merge_table['visit_count'])
        y = list(merge_table['count_foreigner'])
        country_name = foreignvisitor_table['country_name'].unique().item(0)
        r = ss.pearsonr(x, y)[0]
        # r = np.corrcoef(x, y).item(1)
        results.append({'x': x, 'y': y, 'country_name': country_name, 'r': r})

    return results
