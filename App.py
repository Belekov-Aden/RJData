import dash
from dash import dcc, html, dash_table
from dash.dependencies import Input, Output
import pandas as pd
import sqlite3
import plotly.express as px

app = dash.Dash(__name__)

# Вспомогательная функция для получения данных
def get_data(query):
    conn = sqlite3.connect('dataset.db')
    df = pd.read_sql_query(query, conn)
    conn.close()
    return df

# Вспомогательные функции
def calculate_inverted_coefficient(value):
    if pd.isnull(value) or value == 0:
        return 1  # Или другое значение по умолчанию
    return 1 / value

def calculate_penalty_coefficient(value):
    if pd.isnull(value):
        return 1
    return value

def calculate_inverted_driving_coefficient(value):
    if pd.isnull(value) or value == 0:
        return 1  # Или другое значение по умолчанию
    return 1 / value

app.layout = html.Div([
    dcc.Tabs(id="tabs", value='tab-1', children=[
        dcc.Tab(label='Коэффициент пробега', value='tab-1'),
        dcc.Tab(label='Коэффициент соблюдения', value='tab-2'),
        dcc.Tab(label='Штрафной коэффициент', value='tab-3'),
        dcc.Tab(label='Коэффициент стиля вождения', value='tab-4'),
        dcc.Tab(label='Сводный коэффициент', value='tab-5'),
    ]),
    html.Div(id='tabs-content')
])

@app.callback(Output('tabs-content', 'children'),
              Input('tabs', 'value'))
def render_content(tab):
    if tab == 'tab-1':
        query = """
        SELECT 
            polygon_name, 
            vehicle_registration_number, 
            waybill_data_mileage, 
            telematics_data_mileage 
        FROM dataset;
        """
        df = get_data(query)
        df['inverted_waybill_mileage_coefficient'] = df['waybill_data_mileage'].apply(calculate_inverted_coefficient)
        df['inverted_telematics_mileage_coefficient'] = df['telematics_data_mileage'].apply(calculate_inverted_coefficient)

        grouped_df = df.groupby('polygon_name').agg(
            vehicle_registration_count=('vehicle_registration_number', 'count'),
            mean_waybill_mileage=('inverted_waybill_mileage_coefficient', 'mean'),
            count_waybill_mileage=('inverted_waybill_mileage_coefficient', 'count'),
            mean_telematics_mileage=('inverted_telematics_mileage_coefficient', 'mean'),
            count_telematics_mileage=('inverted_telematics_mileage_coefficient', 'count')
        ).reset_index()

        fig = px.bar(grouped_df, x='polygon_name', y=['mean_waybill_mileage', 'mean_telematics_mileage'],
                     barmode='group', title='Средние коэффициенты пробега по путевым листам и телематике')
        return html.Div([
            dcc.Graph(figure=fig)
        ])
    elif tab == 'tab-2':
        query = "SELECT polygon_name, waybill_data_mileage FROM dataset WHERE waybill_data_mileage IS NOT NULL;"
        df = get_data(query)
        df['compliance_coefficient'] = df['waybill_data_mileage'].apply(calculate_inverted_coefficient)
        compliance_df = df.groupby('polygon_name')['compliance_coefficient'].mean().reset_index()

        fig = px.bar(compliance_df, x='polygon_name', y='compliance_coefficient',
                     title='Средний коэффициент соблюдения по путевым листам')
        return html.Div([
            dcc.Graph(figure=fig)
        ])
    elif tab == 'tab-3':
        query = "SELECT polygon_name, fines FROM dataset;"
        df = get_data(query)
        df['penalty_coefficient'] = df['fines'].apply(calculate_penalty_coefficient)
        fines_df = df.groupby('polygon_name')['penalty_coefficient'].mean().reset_index()

        fig = px.bar(fines_df, x='polygon_name', y='penalty_coefficient', title='Средний штрафной коэффициент')
        return html.Div([
            dcc.Graph(figure=fig)
        ])
    elif tab == 'tab-4':
        query = "SELECT polygon_name, driving_style FROM dataset;"
        df = get_data(query)
        df['inverted_driving_coefficient'] = df['driving_style'].apply(calculate_inverted_driving_coefficient)
        driving_df = df.groupby('polygon_name')['inverted_driving_coefficient'].mean().reset_index()

        fig = px.bar(driving_df, x='polygon_name', y='inverted_driving_coefficient', title='Средний коэффициент стиля вождения')
        return html.Div([
            dcc.Graph(figure=fig)
        ])
    elif tab == 'tab-5':
        mileage_query = """
        SELECT 
            polygon_name, 
            vehicle_registration_number, 
            waybill_data_mileage, 
            telematics_data_mileage 
        FROM dataset;
        """
        mileage_df = get_data(mileage_query)
        mileage_df['inverted_waybill_mileage_coefficient'] = mileage_df['waybill_data_mileage'].apply(calculate_inverted_coefficient)
        mileage_df['inverted_telematics_mileage_coefficient'] = mileage_df['telematics_data_mileage'].apply(calculate_inverted_coefficient)

        mileage_grouped_df = mileage_df.groupby('polygon_name').agg(
            P_waybill=('inverted_waybill_mileage_coefficient', 'mean'),
            P_telematics=('inverted_telematics_mileage_coefficient', 'mean')
        ).reset_index()
        mileage_grouped_df['P'] = mileage_grouped_df[['P_waybill', 'P_telematics']].mean(axis=1)

        compliance_query = "SELECT polygon_name, waybill_data_mileage FROM dataset WHERE waybill_data_mileage IS NOT NULL;"
        compliance_df = get_data(compliance_query)
        compliance_df['compliance_coefficient'] = compliance_df['waybill_data_mileage'].apply(calculate_inverted_coefficient)
        compliance_grouped_df = compliance_df.groupby('polygon_name')['compliance_coefficient'].mean().reset_index()

        fines_query = "SELECT polygon_name, fines FROM dataset;"
        fines_df = get_data(fines_query)
        fines_df['penalty_coefficient'] = fines_df['fines'].apply(calculate_penalty_coefficient)
        fines_grouped_df = fines_df.groupby('polygon_name')['penalty_coefficient'].mean().reset_index()

        driving_query = "SELECT polygon_name, driving_style FROM dataset;"
        driving_df = get_data(driving_query)
        driving_df['inverted_driving_coefficient'] = driving_df['driving_style'].apply(calculate_inverted_driving_coefficient)
        driving_grouped_df = driving_df.groupby('polygon_name')['inverted_driving_coefficient'].mean().reset_index()

        final_df = mileage_grouped_df.merge(compliance_grouped_df, on='polygon_name').merge(fines_grouped_df, on='polygon_name').merge(driving_grouped_df, on='polygon_name')
        final_df['S'] = final_df[['P', 'compliance_coefficient', 'penalty_coefficient', 'inverted_driving_coefficient']].mean(axis=1)

        fig = px.bar(final_df, x='polygon_name', y=['P', 'compliance_coefficient', 'penalty_coefficient', 'inverted_driving_coefficient', 'S'],
                     barmode='group', title='Сводный коэффициент')

        return html.Div([
            dcc.Graph(figure=fig)
        ])

if __name__ == '__main__':
    app.run_server(debug=True)
