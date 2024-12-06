import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
from core_analysis import *
import requests
import json

import warnings
warnings.filterwarnings('ignore')

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    st.write("""
    # Analysis the suicide rates
    
    # Introduction
    In recent years, the examination of suicide rates has emerged as a critical area of 
    study within public health, shedding light on the complex interplay of societal, psychological, and demographic 
    factors influencing mental well-being. This project undertakes a comprehensive analysis of suicide rates, 
    focusing specifically on their variation across different age groups and over an extended period. By leveraging 
    robust data visualization and statistical techniques, the study aims to uncover meaningful trends and insights 
    that can inform policy-making and targeted interventions. 
    
    # Data preparation / Data cleanup
    So, lets look at the data we have:
    
    """)

    df = None
    if st.button('Upload the dataset via GET fastapi',key='button1'):
        # st.session_state["button1"] = not st.session_state["button1"]
        # df = pd.read_csv('../data/master.csv')
        response = requests.get("http://eternalmech-analysis-of-suicidal-rates-7479.twc1.net/data")
        data = response.json()
        df = pd.DataFrame(data)

    if df is None:
        raise Exception('You should upload a dataset to make analysis')

    st.dataframe(df.sample(5))  # higlight_max highlights the max value in column

    info = pd.DataFrame({"name": df.columns, "non-nulls": len(df) - df.isnull().sum().values,
                         "nulls": df.isnull().sum().values, "type": df.dtypes.values})

    st.dataframe(info)

    st.write("""As you can see, most of the HDIForYear value is empty. Lets clean up the dataset by deleting useless
             column.
             
             """)
    df = df.drop('HDI for year', axis=1)

    info = pd.DataFrame({"name": df.columns, "non-nulls": len(df) - df.isnull().sum().values,
                         "nulls": df.isnull().sum().values, "type": df.dtypes.values})

    st.dataframe(info)

    st.write("""As you can see, most of the HDIForYear value is empty. Lets clean up the dataset by deleting useless
                 column. """)
    st.write("""
    # Descriptive statistics
    Let's see at Descriptive statistics of our dataset:
    """)
    st.dataframe(df.describe())

    st.write("""
    
    # Hypothesis - Gender Disparity in Suicide Rates Across Generations
    A central element of the project is the hypothesis check.
    So, Let introduce Hypothesis.
    
    Previous studies have indicated that suicide rates often exhibit significant gender
    disparities, with males typically having higher rates compared to females. However, societal changes and evolving
    gender roles across generations may influence these trends differently.
    
    Formulation: “Across all generations, males exhibit higher suicide rates than females. However, the gender gap in
    suicide rates has narrowed in younger generations (e.g., Generation Z) compared to older generations
     (e.g., Baby Boomers).”
    
    """)

    st.write("""
        # Data analysis / Plots
        First of all, lets analyse data to check our hypothesis:""")
    st.write("""
    ___
        Population at 1985:
        """)

    country_1985, country_1985_population = get_population(df)
    plt.style.use('dark_background')

    plt.figure(figsize=(10, 10))
    sns.barplot(y=country_1985, x=country_1985_population, palette='pastel')
    plt.xlabel('Population Count')
    plt.ylabel('Countries')
    plt.title('1985 Year Sum Population for Suicide Rate')

    st.pyplot(plt)

    st.write("""
    ___
            Number of suicides over 25 countries:
            """)

    data_suicide_countr = get_n_suicides(df)
    plt.clf()
    sns.barplot(y=data_suicide_countr.country[:25], x=data_suicide_countr.suicides_no[:25], palette='pastel')
    st.pyplot(plt)

    st.write("""
    ___
                Graphical analysis suicides for all ages and genders:
                """)

    male_, female_ = get_diff_ages(df)
    # print(male_, female_)
    plt.clf()
    plot_id = 0
    for i, age in enumerate(['15-24 years', '25-34 years', '35-54 years', '5-14 years', '55-74 years', '75+ years']):
        plot_id += 1
        plt.subplot(3, 2, plot_id)
        plt.title(age)
        fig, ax = plt.gcf(), plt.gca()
        sns.barplot(x=['male', 'female'], y=[male_[i], female_[i]], palette='pastel')
        plt.tight_layout()
        fig.set_size_inches(10, 15)
    st.pyplot(plt)

    st.write("""
    ___
                    Visualising graph of suicidal rates over years:
                    """)

    plt.clf()
    plt.figure(figsize=(10, 10))
    sns.set_color_codes("muted")
    sns.barplot(x="year", y="suicides_no", data=df,
                label="Year Suicides", color="b")
    plt.xticks(rotation=90)
    st.pyplot(plt)

    st.write("""
    # Let's analyse suicidal rates over generations.
    
    Creating multi-line plots to depict suicide rates for males and females across different generations.
    """)

    st.write("""
    ---
        Firstly lets calculate number of people in each generation:
    """)

    plt.clf()
    f, ax = plt.subplots(1, 2, figsize=(24, 8))
    data = df['generation'].value_counts().plot.pie(explode=[0.1, 0.1, 0.1, 0.1, 0.1, 0.1], autopct='%1.1f%%', ax=ax[0],
                                               shadow=True)
    ax[0].set_title('Generations Count')
    ax[0].set_ylabel('Count')
    sns.countplot(df, ax=ax[0])
    ax[1].set_title('Generations Count')
    sns.countplot(df.generation, ax=ax[1], palette='pastel')
    st.pyplot(plt)
    del data

    st.write("""
        ---
            Number of suicides over years in each generation:
        """)

    plt.clf()
    # Plot sepal with as a function of sepal_length across days
    g = sns.lmplot(x="year", y="suicides_no", hue="generation",
                   truncate=True, height=5, data=df)

    # Use more informative axis labels than are provided by default
    g.set_axis_labels("Year", "Suicides No")
    st.pyplot(plt)

    st.write("""
            ---
                Finally, lets see all dependencies between all datas we have colorizing by genders:
            """)
    plt.clf()
    sns.pairplot(df, hue="sex", palette='pastel')
    st.pyplot(plt)

    st.write("""
    # Conclusion about hypothesis:
    
    Upon analyzing the data, it was observed that:
     - Older Generations (Baby Boomers and Generation X): Males consistently exhibited higher suicide rates than 
     females, maintaining a substantial gender gap.
     
     - Younger Generations (Millennials and Generation Z): While males still had higher suicide rates, the gap between
      males and females was notably smaller compared to older generations.
      
      So, the data supports the hypothesis that males generally have higher suicide rates than females across all
      generations. Moreover, the gender disparity in suicide rates has diminished in younger generations,
      indicating a narrowing gap. This trend may reflect changing societal norms, increased mental health
      awareness among females, or evolving stressors affecting different genders across generations.
    
    """)

    st.write('# Cleaned and analysed dataset has been saved via POST fastapi')
    url = 'http://eternalmech-analysis-of-suicidal-rates-7479.twc1.net/upload-dataframe/'

    # Преобразуем DataFrame в JSON с использованием ориентации 'split'
    df_json = df.to_json(orient='split')

    # Парсим JSON строку в словарь
    df_dict = json.loads(df_json)

    # Создаем структуру данных для отправки
    payload = {
        'data': df_dict['data'],
        'columns': df_dict['columns'],
        'index': df_dict['index']
    }

    # Отправляем POST-запрос с JSON-данными
    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()  # Проверка на успешный запрос
        # Вывод ответа от сервера
        print(response.json())
    except requests.exceptions.HTTPError as err:
        print(f"HTTP error occurred: {err}")
    except Exception as err:
        print(f"An error occurred: {err}")
