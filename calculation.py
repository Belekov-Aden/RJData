import sqlite3
import pandas as pd


def task1():
    conn = sqlite3.connect('dataset.db')

    query = "SELECT polygon_name, vehicle_registration_number, waybill_data_mileage, telematics_data_mileage FROM dataset;"
    df = pd.read_sql(query, conn)

    def calculate_inverted_mileage_coefficient(x):
        deviation = abs(x - 1) / 1
        if deviation < 0.1:
            return 0.9
        elif deviation < 0.2:
            return 0.8
        elif deviation < 0.3:
            return 0.7
        elif deviation < 0.4:
            return 0.6
        elif deviation < 0.5:
            return 0.5
        elif deviation < 0.6:
            return 0.4
        elif deviation < 0.7:
            return 0.3
        elif deviation < 0.8:
            return 0.2
        elif deviation < 0.9:
            return 0.1
        elif deviation < 1:
            return 0
        else:
            return None

    df['inverted_waybill_mileage_coefficient'] = df['waybill_data_mileage'].apply(
        calculate_inverted_mileage_coefficient)

    df['inverted_telematics_mileage_coefficient'] = df['telematics_data_mileage'].apply(
        calculate_inverted_mileage_coefficient)

    grouped_df = df.groupby('polygon_name').agg({
        'vehicle_registration_number': 'count',
        'inverted_waybill_mileage_coefficient': ['mean', 'count'],
        'inverted_telematics_mileage_coefficient': ['mean', 'count']
    }).reset_index()

    for _, row in grouped_df.iterrows():
        polygon_id = row['polygon_name']
        total_count = row[('vehicle_registration_number', 'count')]

        waybill_mean_coefficient = round(row[('inverted_waybill_mileage_coefficient', 'mean')], 3)
        waybill_count_by_coefficient = row[('inverted_waybill_mileage_coefficient', 'count')]

        telematics_mean_coefficient = round(row[('inverted_telematics_mileage_coefficient', 'mean')], 3)
        telematics_count_by_coefficient = row[('inverted_telematics_mileage_coefficient', 'count')]

        print(f"Полигон: {polygon_id} - Общее количество машин: {total_count}")
        print(f"Коэффициент манеры вождения по waybill_data_mileage: {waybill_mean_coefficient}")
        print(f"Количество машин с данным коэффициентом (waybill_data_mileage): {waybill_count_by_coefficient}")
        print("")
        print(f"Коэффициент манеры вождения по telematics_data_mileage: {telematics_mean_coefficient}")
        print(f"Количество машин с данным коэффициентом (telematics_data_mileage): {telematics_count_by_coefficient}")
        print("----------------------------")

    conn.close()


def task2():
    conn = sqlite3.connect('dataset.db')

    query = "SELECT polygon_name, structural_subdivision_name, vehicle_registration_number FROM dataset;"
    df = pd.read_sql(query, conn)

    # Рассчитываем общее количество машин в каждом подразделении
    subdivision_counts = df.groupby('structural_subdivision_name')['vehicle_registration_number'].nunique()

    # Рассчитываем общее количество машин в целевой структуре (полигоне)
    total_polygon_count = df.groupby('polygon_name')['vehicle_registration_number'].nunique()

    coefficients = []

    def calculate_coefficient(value):
        if deviation < 0.1:
            return 0.9
        elif deviation < 0.2:
            return 0.8
        elif deviation < 0.3:
            return 0.7
        elif deviation < 0.4:
            return 0.6
        elif deviation < 0.5:
            return 0.5
        elif deviation < 0.6:
            return 0.4
        elif deviation < 0.7:
            return 0.3
        elif deviation < 0.8:
            return 0.2
        elif deviation < 0.9:
            return 0.1
        elif deviation < 1:
            return 0

    for polygon, count in total_polygon_count.items():
        polygon_df = df[df['polygon_name'] == polygon]
        for subdivision, sub_count in subdivision_counts.items():
            if subdivision in polygon_df['structural_subdivision_name'].unique():
                subdivision_count = polygon_df[polygon_df['structural_subdivision_name'] == subdivision][
                    'vehicle_registration_number'].nunique()
                ratio = subdivision_count / count
                deviation = abs(ratio - 1.0)
                coefficient = calculate_coefficient(deviation)
                coefficients.append(
                    {'polygon_name': polygon, 'structural_subdivision_name': subdivision, 'coefficient': coefficient})

    coefficients_df = pd.DataFrame(coefficients)

    for index, row in coefficients_df.iterrows():
        print(
            f"Полигон: {row['polygon_name']}\nПодразделение: {row['structural_subdivision_name']}\nКоэффициент: {row['coefficient']}\n")

    conn.close()


def task3():
    conn = sqlite3.connect('dataset.db')

    query = "SELECT polygon_name, IFNULL(fines, 1) AS fines FROM dataset;"
    df = pd.read_sql(query, conn)

    def calculate_penalty_coefficient(x):
        deviation = abs(x - 1)
        if deviation < 0.1:
            return 0.9
        elif deviation < 0.2:
            return 0.8
        elif deviation < 0.3:
            return 0.7
        elif deviation < 0.4:
            return 0.6
        elif deviation < 0.5:
            return 0.5
        elif deviation < 0.6:
            return 0.4
        elif deviation < 0.7:
            return 0.3
        elif deviation < 0.8:
            return 0.2
        elif deviation < 0.9:
            return 0.1
        elif deviation < 1:
            return 0
        else:
            return 1

    df['penalty_coefficient'] = df['fines'].apply(calculate_penalty_coefficient)

    grouped_df = df.groupby('polygon_name')['penalty_coefficient'].mean().reset_index()

    for index, row in grouped_df.iterrows():
        print(f"Полигон: {row['polygon_name']}\nКоэффициент штрафов: {round(row['penalty_coefficient'], 3)}\n")

    conn.close()


def task4():
    conn = sqlite3.connect('dataset.db')

    query = "SELECT polygon_name, vehicle_registration_number, driving_style FROM dataset;"
    df = pd.read_sql(query, conn)

    def calculate_inverted_driving_coefficient(x):
        if x == 0:
            return None
        deviation = abs(x - 6) / 6
        if deviation < 0.1:
            return 0.9
        elif deviation < 0.2:
            return 0.8
        elif deviation < 0.3:
            return 0.7
        elif deviation < 0.4:
            return 0.6
        elif deviation < 0.5:
            return 0.5
        elif deviation < 0.6:
            return 0.4
        elif deviation < 0.7:
            return 0.3
        elif deviation < 0.8:
            return 0.2
        elif deviation < 0.9:
            return 0.1
        elif deviation < 1:
            return 0
        else:
            return None

    df['inverted_driving_coefficient'] = df['driving_style'].apply(calculate_inverted_driving_coefficient)

    grouped_df = df.groupby('polygon_name').agg({'vehicle_registration_number': 'count',
                                                 'inverted_driving_coefficient': ['mean', 'count']}).reset_index()

    for index, row in grouped_df.iterrows():
        polygon_id = row['polygon_name']
        total_count = row['vehicle_registration_number']['count']
        mean_coefficient = row['inverted_driving_coefficient']['mean']
        count_by_coefficient = row['inverted_driving_coefficient']['count']

        if not pd.isnull(mean_coefficient):
            print(f"Полигон: {polygon_id} - Общее количество машин: {total_count}")
            print(f"Коэффициент манеры вождения: {round(mean_coefficient, 3)}")
            print(f"Количество машин с данной манерой вождения: {count_by_coefficient}\n")

    conn.close()


def task5():
    conn = sqlite3.connect('dataset.db')

    # Task 1: Calculate mileage coefficients
    mileage_query = "SELECT polygon_name, vehicle_registration_number, waybill_data_mileage, telematics_data_mileage FROM dataset;"
    mileage_df = pd.read_sql(mileage_query, conn)

    def calculate_inverted_mileage_coefficient(x):
        deviation = abs(x - 1) / 1
        if deviation < 0.1:
            return 0.9
        elif deviation < 0.2:
            return 0.8
        elif deviation < 0.3:
            return 0.7
        elif deviation < 0.4:
            return 0.6
        elif deviation < 0.5:
            return 0.5
        elif deviation < 0.6:
            return 0.4
        elif deviation < 0.7:
            return 0.3
        elif deviation < 0.8:
            return 0.2
        elif deviation < 0.9:
            return 0.1
        elif deviation < 1:
            return 0
        else:
            return None

    mileage_df['inverted_waybill_mileage_coefficient'] = mileage_df['waybill_data_mileage'].apply(
        calculate_inverted_mileage_coefficient)
    mileage_df['inverted_telematics_mileage_coefficient'] = mileage_df['telematics_data_mileage'].apply(
        calculate_inverted_mileage_coefficient)

    mileage_grouped_df = mileage_df.groupby('polygon_name').agg({
        'inverted_waybill_mileage_coefficient': 'mean',
        'inverted_telematics_mileage_coefficient': 'mean'
    }).reset_index()

    mileage_grouped_df['P'] = mileage_grouped_df[
        ['inverted_waybill_mileage_coefficient', 'inverted_telematics_mileage_coefficient']].mean(axis=1)

    # Task 2: Calculate compliance coefficients
    compliance_query = "SELECT polygon_name, structural_subdivision_name, vehicle_registration_number FROM dataset;"
    compliance_df = pd.read_sql(compliance_query, conn)

    subdivision_counts = compliance_df.groupby('structural_subdivision_name')['vehicle_registration_number'].nunique()
    total_polygon_count = compliance_df.groupby('polygon_name')['vehicle_registration_number'].nunique()

    compliance_coefficients = []

    def calculate_coefficient(value):
        if deviation < 0.1:
            return 0.9
        elif deviation < 0.2:
            return 0.8
        elif deviation < 0.3:
            return 0.7
        elif deviation < 0.4:
            return 0.6
        elif deviation < 0.5:
            return 0.5
        elif deviation < 0.6:
            return 0.4
        elif deviation < 0.7:
            return 0.3
        elif deviation < 0.8:
            return 0.2
        elif deviation < 0.9:
            return 0.1
        elif deviation < 1:
            return 0

    for polygon, count in total_polygon_count.items():
        polygon_df = compliance_df[compliance_df['polygon_name'] == polygon]
        for subdivision, sub_count in subdivision_counts.items():
            if subdivision in polygon_df['structural_subdivision_name'].unique():
                subdivision_count = polygon_df[polygon_df['structural_subdivision_name'] == subdivision][
                    'vehicle_registration_number'].nunique()
                ratio = subdivision_count / count
                deviation = abs(ratio - 1.0)
                coefficient = calculate_coefficient(deviation)
                compliance_coefficients.append({
                    'polygon_name': polygon,
                    'structural_subdivision_name': subdivision,
                    'coefficient': coefficient
                })

    compliance_df = pd.DataFrame(compliance_coefficients).groupby('polygon_name')['coefficient'].mean().reset_index()
    compliance_df.rename(columns={'coefficient': 'C'}, inplace=True)

    # Task 3: Calculate penalty coefficients
    fines_query = "SELECT polygon_name, IFNULL(fines, 1) AS fines FROM dataset;"
    fines_df = pd.read_sql(fines_query, conn)

    def calculate_penalty_coefficient(x):
        deviation = abs(x - 1)
        if deviation < 0.1:
            return 0.9
        elif deviation < 0.2:
            return 0.8
        elif deviation < 0.3:
            return 0.7
        elif deviation < 0.4:
            return 0.6
        elif deviation < 0.5:
            return 0.5
        elif deviation < 0.6:
            return 0.4
        elif deviation < 0.7:
            return 0.3
        elif deviation < 0.8:
            return 0.2
        elif deviation < 0.9:
            return 0.1
        elif deviation < 1:
            return 0

    fines_df['penalty_coefficient'] = fines_df['fines'].apply(calculate_penalty_coefficient)
    penalty_grouped_df = fines_df.groupby('polygon_name')['penalty_coefficient'].mean().reset_index()
    penalty_grouped_df.rename(columns={'penalty_coefficient': 'Ш'}, inplace=True)

    # Task 4: Calculate driving style coefficients
    driving_query = "SELECT polygon_name, vehicle_registration_number, driving_style FROM dataset;"
    driving_df = pd.read_sql(driving_query, conn)

    def calculate_inverted_driving_coefficient(x):
        if x == 0:
            return None
        deviation = abs(x - 6) / 6
        if deviation < 0.1:
            return 0.9
        elif deviation < 0.2:
            return 0.8
        elif deviation < 0.3:
            return 0.7
        elif deviation < 0.4:
            return 0.6
        elif deviation < 0.5:
            return 0.5
        elif deviation < 0.6:
            return 0.4
        elif deviation < 0.7:
            return 0.3
        elif deviation < 0.8:
            return 0.2
        elif deviation < 0.9:
            return 0.1
        elif deviation < 1:
            return 0
        else:
            return None

    driving_df['inverted_driving_coefficient'] = driving_df['driving_style'].apply(
        calculate_inverted_driving_coefficient)
    driving_grouped_df = driving_df.groupby('polygon_name')['inverted_driving_coefficient'].mean().reset_index()
    driving_grouped_df.rename(columns={'inverted_driving_coefficient': 'МВ'}, inplace=True)

    # Merge all the dataframes
    final_df = mileage_grouped_df[['polygon_name', 'P']].merge(
        compliance_df[['polygon_name', 'C']], on='polygon_name'
    ).merge(
        penalty_grouped_df[['polygon_name', 'Ш']], on='polygon_name'
    ).merge(
        driving_grouped_df[['polygon_name', 'МВ']], on='polygon_name'
    )

    # Calculate the final rating
    final_df['Р'] = final_df['P'] * 0.4 + final_df['C'] * 0.3 + final_df['Ш'] * 0.15 + final_df['МВ'] * 0.15

    # Display the results
    for _, row in final_df.iterrows():
        print(f"Полигон: {row['polygon_name']}")
        print(f"Рейтинг эффективности: {round(row['Р'], 3)}")
        print("----------------------------")

    conn.close()
