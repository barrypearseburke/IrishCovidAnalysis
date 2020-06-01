def get_all_dfs():
    import json
    from datetime import date, timedelta
    import pandas
    import pandas as pd
    import requests
    Daily_deaths = {'Week_number': [],
                    'Value': []
                    }
    base_url = '''
https://rip.ie/deathnotices.php?do=get_deathnotices_pages&sEcho=6&iColumns=5&sColumns=&iDisplayStart={start_number}&iDisplayLength=40&mDataProp_0=0&mDataProp_1=1&mDataProp_2=2&mDataProp_3=3&mDataProp_4=4&iSortingCols=2&iSortCol_0=0&sSortDir_0=desc&iSortCol_1=0&sSortDir_1=asc&bSortable_0=true&bSortable_1=true&bSortable_2=true&bSortable_3=true&bSortable_4=true&iDisplayLength=40&DateFrom={cob_from}+00%3A00%3A00&DateTo={cob_to}+23%3A59%3A59&NoWhere=y
'''
    start_date_2017 = date(year=2017, month=1, day=2)
    start_date_2018 = date(year=2018, month=1, day=1)
    start_date_2019 = date(year=2018, month=12, day=31)
    start_date_2020 = date(year=2019, month=12, day=30)

    def get_weekly_data_for_1_year(start_date):
        df_base_year = pd.DataFrame(data=Daily_deaths)
        for iter in range(1, 23):
            end_date = start_date + timedelta(days=7)
            formated_url = base_url.format(start_number=0,
                                           cob_from=start_date.strftime("%Y-%m-%d"),
                                           cob_to=end_date.strftime("%Y-%m-%d")
                                           )
            results = requests.get(formated_url)
            json_results = json.loads(results.text)
            weekly_value = json_results['iTotalRecords']
            week_deaths = {'Week_number': [int(iter)],
                           'Value': [int(weekly_value)]
                           }
            df_week = pd.DataFrame(data=week_deaths)
            df_base_year = df_base_year.append(df_week)
            start_date = end_date
        return df_base_year

    def average_df(df1, df2, df3, average_on_col='Value', join_on='Week_number'):
        results = pd.merge(df1, df2, 'inner', 'Week_number')
        results = pd.merge(results, df3, 'inner', 'Week_number')
        results['average'] = list((results['Value_x'] + results['Value_y'] + results['Value']) / 3)
        return results

    def df_without_covid(df_2020, covid_df):
        results = pd.merge(df_2020, covid_df, 'inner', 'Week_number')
        results['Value'] = list(results['Value_x'] - results['Value_y'])
        return results

    def get_covid_data():
        df_orginial = pandas.read_csv('covid200601.csv')
        df2 = df_orginial[['Date', 'ConfirmedCovidDeaths']]
        df2.rename(columns={'ConfirmedCovidDeaths': 'Value'}, inplace=True)
        df2['Date'] = pd.to_datetime(df2['Date'])
        df2['Week_number'] = df2['Date'].dt.week
        df3 = df2.groupby([pd.Grouper(key='Week_number')])['Value'].sum().reset_index().sort_values(
            'Week_number')
        return df3

    ## Get Data
    try:
        df_2017 = pandas.read_pickle("df_2017.pkl")
    except:
        df_2017 = get_weekly_data_for_1_year(start_date_2017)
        df_2017.to_pickle("df_2017.pkl")
    try:
        df_2018 = pandas.read_pickle("df_2018.pkl")
    except:
        df_2018 = get_weekly_data_for_1_year(start_date_2018)
        df_2018.to_pickle("df_2018.pkl")
    try:
        df_2019 = pandas.read_pickle("df_2019.pkl")
    except:
        df_2019 = get_weekly_data_for_1_year(start_date_2019)
        df_2019.to_pickle("df_2019.pkl")
    try:
        df_2020 = pandas.read_pickle("df_2020.pkl")
    except:
        df_2020 = get_weekly_data_for_1_year(start_date_2020)
        df_2020.to_pickle("df_2020.pkl")
    covid_df = get_covid_data()
    df_average = average_df(df_2017, df_2018, df_2019, average_on_col='Value', join_on='Week_number')
    df2020_without_covid = df_without_covid(df_2020, covid_df)
    ## Get Data End

    return {
        'df_2017': df_2017,
        'df_2018':df_2018,
        'df_2019':df_2019,
        'df_2020':df_2020,
        'covid_df':covid_df,
        'df_average':df_average,
        'df2020_without_covid':df2020_without_covid
    }


