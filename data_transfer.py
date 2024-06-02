import pandas as pd
import sqlite3


def transfer_xlsx(file_name):
    df = pd.read_excel(file_name)

    df.columns = [
        'polygon_name', 'short_name', 'polygon', 'vehicle_registration_number',
        'structural_subdivision_name', 'assignment_type', 'functions_performed',
        'position_of_vehicle_assignee', 'waybill_date', 'waybill_data_mileage',
        'telematics_signal_date', 'telematics_data_mileage', 'fines', 'driving_style'
    ]

    columns_to_fill = [
        'polygon_name', 'short_name', 'polygon', 'vehicle_registration_number', 'structural_subdivision_name',
        'assignment_type'
    ]
    df[columns_to_fill] = df[columns_to_fill].ffill()

    conn = sqlite3.connect('dataset.db')
    c = conn.cursor()

    c.execute('''
    CREATE TABLE IF NOT EXISTS dataset (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        polygon_name TEXT,
        short_name TEXT,
        polygon TEXT,
        vehicle_registration_number TEXT,
        structural_subdivision_name TEXT,
        assignment_type TEXT,
        functions_performed TEXT,
        position_of_vehicle_assignee TEXT,
        waybill_date TEXT,
        waybill_data_mileage REAL,
        telematics_signal_date TEXT,
        telematics_data_mileage REAL,
        fines REAL,
        driving_style TEXT
    )
    ''')

    df.to_sql('dataset', conn, if_exists='replace', index=False)
    conn.close()


def create_polygon_table(database):
    conn = sqlite3.connect(database)
    c = conn.cursor()

    c.execute('''
    SELECT DISTINCT polygon_name FROM dataset
    ''')

    unique_polygons = c.fetchall()

    c.execute('''
    CREATE TABLE IF NOT EXISTS unique_polygons (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        polygon_name TEXT
    )
    ''')

    c.executemany('''
    INSERT INTO unique_polygons (polygon_name) VALUES (?)
    ''', unique_polygons)

    conn.commit()
    conn.close()
