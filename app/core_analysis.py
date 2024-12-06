import pandas as pd
import numpy as np


def get_population(data):
    min_year = min(data.year)

    country_1985 = data[(data['year'] == min_year)].country.unique()
    data_country = data[(data['year'] == min_year)]
    country_1985_population = []
    for country in country_1985:
        country_1985_population.append(sum(data_country[(data_country['country'] == country)].population))

    return country_1985, country_1985_population


def get_n_suicides(data):
    suicidesNo = []
    for country in data.country.unique():
        suicidesNo.append(sum(data[data['country'] == country].suicides_no))

    suicidesNo = pd.DataFrame(suicidesNo, columns=['suicides_no'])
    country = pd.DataFrame(data.country.unique(), columns=['country'])
    data_suicide_countr = pd.concat([suicidesNo, country], axis=1)
    data_suicide_countr = data_suicide_countr.sort_values(by='suicides_no', ascending=False)

    return data_suicide_countr


def get_diff_ages(data):
    group_data = data.groupby(['age', 'sex'])['suicides_no'].sum().unstack()
    group_data = group_data.reset_index().melt(id_vars='age')
    group_data_female = group_data.iloc[:6, :]
    group_data_male = group_data.iloc[6:, :]

    return list(group_data_male['value']), list(group_data_female['value'])
