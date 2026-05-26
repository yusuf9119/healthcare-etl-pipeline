import sqlite3
import pandas as pd


def analysis(db_path:str):
    conn  = sqlite3.connect(db_path)

    q1 = """
    SELECT 
        condition, 
        COUNT(*) AS total_patients,
        ROUND(AVG(age), 1) AS average_age,
        ROUND(AVG(cholesterol), 1) AS average_cholesterol
    FROM healthcare
    GROUP BY condition
    ORDER BY total_patients DESC;
    """
    print("\n[patient summary by medical conditon]")
    print(pd.read_sql_query(q1, conn).to_string(index=False))

    # Query 2: Condition Distribution by Gender
    q2 = """
    SELECT 
        gender,
        condition, 
        COUNT(*) AS patient_count
    FROM healthcare
    GROUP BY gender, condition
    ORDER BY gender, patient_count DESC;
    """
    print("\n[condtion numbers by gender]")
    print(pd.read_sql_query(q2, conn).to_string(index=False))

    
    q3 = """
    SELECT 
        patient_name, 
        age, 
        gender,
        condition, 
        cholesterol,
        email
    FROM healthcare
    WHERE age >= 50 AND cholesterol >= 200
    ORDER BY cholesterol DESC
    LIMIT 10;
    """
    print("\n [top 10 patients over 50 with high risk of cholesterol]")
    print(pd.read_sql_query(q3, conn).to_string(index=False))

    # Query 4: Visit Volume Trends
    q4 = """
    SELECT 
        STRFTIME('%Y-%m', visit_date) AS visit_month,
        COUNT(*) AS total_visits
    FROM healthcare
    WHERE visit_date IS NOT NULL
    GROUP BY visit_month
    ORDER BY visit_month ASC;
    """
    print("[]")
    print(pd.read_sql_query(q4, conn).to_string(index=False))

if __name__ == "__main__":
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', 900)
    
    analysis('healthcare.db')