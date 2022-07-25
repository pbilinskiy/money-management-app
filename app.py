import sys

import pandas as pd
import streamlit as st
from streamlit import cli as stcli
from st_on_hover_tabs import on_hover_tabs
import plotly.express as px

from dictionaries import transaction_name_category, fund_names, fund_distribution
from DataKeeper import DataKeeper


d = DataKeeper()




def tab_dashboard(): 
    # get expenditures for current month
    df = d.df_transaction
    df = df[(df['month_date'] == d.month_date) 
             & (df['money_value'] < 0)]

    # display balance
    columns_0 = st.columns(6)
    currency = columns_0[0].selectbox('Валюта', ['UAH', 'EUR', 'USD'])
    
    df = df[df['currency'] == currency]
    
    columns_1 = st.columns(4)
    for i, fund in enumerate(fund_names):
        money_value = d.df_balance.loc[(d.month_date, fund), f'value_{currency.lower()}']
        metric_balance_str = f'{money_value} {currency}' if money_value != 0 else None
        columns_1[i].metric(label=fund_names[fund], 
                            value=metric_balance_str)
    
    # pie chart
    df = df[df['currency'] == currency]
    df['money_value'] = -df['money_value']
    df_agg = df.groupby('category')['money_value'].sum().reset_index()
    # # rename categories NEEDS OPTIMIZATION
    category_names = [transaction_name_category[category] for category in df_agg['category'].values]
    df_agg['category_name'] = category_names
    
    df_agg =    df_agg.rename(columns={'money_value': f'Гроші {currency}', 'category_name': 'Категорія'})
    fig = px.pie(df_agg, values=f'Гроші {currency}', names='Категорія', title='Структура витрат')
    st.plotly_chart(fig)
    

def tab_transactions():
    columns_1 = st.columns([1, 2])
    is_income = columns_1[0].radio(label="", options=[False, True], 
                                   format_func=lambda is_income: "Витрати (беремо із конвертів)" if not is_income else "Доходи (кладемо у конверти)")

    with st.form(key='transaction-input'):
        columns_2 = st.columns([1, 2])
        money_input = columns_2[0].text_input(label='Величина та валюта операції')

        category, fund_destination = '', ''
        if not is_income:
            category = columns_2[1].selectbox('Категорія', transaction_name_category.keys(), format_func=lambda option: transaction_name_category[option])
        else:
            fund_destination = columns_2[1].selectbox('✉️ Покласти у конверт', ['all'] + list(fund_names.keys()), format_func=lambda option: 'Розподілити по всіх' if option == 'all' else fund_names[option])

        is_submit = st.form_submit_button('Зберегти')

        if is_submit:
            if is_income and fund_destination == 'all':
                for fund in fund_distribution:
                    money_input = '{:} {:}'.format(fund_distribution[fund]['money_value'], fund_distribution[fund]['currency'])
                    d.add_transaction(money_input, is_income, category, fund)
            else:
                d.add_transaction(money_input, is_income, category, fund_destination)
            
            st.success(f'✔️ Додано нову операцію: {money_input}')
            # except Exception as e:
            #     st.error('Помилка. Не вдалося додати операцію. Деталі: {:}'.format(e))


def tab_history():
    st.dataframe(d.df_transaction)
            


def main():
    st.set_page_config(layout="wide", page_title='Трекер бюджету', page_icon='💰')
    
    st.header('💰 Трекер бюджету')
    st.markdown('<style>' + open('style.css').read() + '</style>', unsafe_allow_html=True)

    with st.sidebar:
        tabs = on_hover_tabs(tabName=['Дашборд', 'Операції', 'Історія'], 
                            iconName=['bar_chart', 'add_circle', 'history'], default_choice=0)

    if tabs =='Дашборд':
        tab_dashboard()
    elif tabs == 'Операції':
        tab_transactions()
    elif tabs == 'Історія':
        tab_history()
    
    

if __name__ == '__main__':
   if st._is_running_with_streamlit:
       main()
   else:
       sys.argv = ["streamlit", "run", "app.py"]
       sys.exit(stcli.main())