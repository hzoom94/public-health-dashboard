# create_sample_db.py
import sqlite3
import pandas as pd
import numpy as np
from datetime import date, timedelta

def create_sample_database():
    """إنشاء قاعدة بيانات تجريبية مع بيانات واقعية"""
    
    # الاتصال بقاعدة البيانات
    conn = sqlite3.connect('health_data.db')
    cursor = conn.cursor()
    
    # إنشاء الجداول
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS health_metrics (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        country TEXT NOT NULL,
        year INTEGER NOT NULL,
        life_expectancy REAL,
        child_mortality REAL,
        health_expenditure REAL,
        physicians_per_10k REAL,
        hospital_beds_per_10k REAL
    )
    ''')
    
    # بيانات واقعية للدول المختارة
    countries = ['Japan', 'Germany', 'Brazil', 'United States', 'United Kingdom']
    
    # بيانات محاكاة للسنوات 2000-2020
    data = []
    for country in countries:
        for year in range(2000, 2021):
            # قيم محاكاة واقعية
            base_values = {
                'Japan': {'life_exp': 81, 'child_mort': 4, 'health_exp': 9, 'physicians': 23, 'beds': 13},
                'Germany': {'life_exp': 79, 'child_mort': 5, 'health_exp': 11, 'physicians': 42, 'beds': 8},
                'Brazil': {'life_exp': 72, 'child_mort': 33, 'health_exp': 8, 'physicians': 19, 'beds': 2.3},
                'United States': {'life_exp': 77, 'child_mort': 7, 'health_exp': 17, 'physicians': 26, 'beds': 2.9},
                'United Kingdom': {'life_exp': 79, 'child_mort': 5, 'health_exp': 9, 'physicians': 28, 'beds': 2.8}
            }
            
            base = base_values[country]
            
            # إضافة تحسن تدريجي مع مرور السنوات
            year_factor = (year - 2000) / 20  # من 0 إلى 1
            
            data.append((
                country,
                year,
                round(base['life_exp'] + year_factor * 5, 1),  # تحسن بمقدار 5 سنوات
                round(base['child_mort'] * (1 - year_factor * 0.6), 1),  # انخفاض 60%
                round(base['health_exp'] + year_factor * 3, 1),  # زيادة الإنفاق
                round(base['physicians'] + year_factor * 10, 1),  # زيادة الأطباء
                round(base['beds'] + year_factor * 2, 1)  # زيادة الأسرة
            ))
    
    # إدخال البيانات
    cursor.executemany('''
    INSERT INTO health_metrics 
    (country, year, life_expectancy, child_mortality, health_expenditure, 
     physicians_per_10k, hospital_beds_per_10k)
    VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', data)
    
    conn.commit()
    
    # عرض الإحصائيات
    cursor.execute("SELECT COUNT(*) FROM health_metrics")
    total_records = cursor.fetchone()[0]
    
    cursor.execute("SELECT DISTINCT country FROM health_metrics")
    unique_countries = cursor.fetchall()
    
    print(f"✅ Database created successfully!")
    print(f"📊 Total records: {total_records}")
    print(f"🌍 Countries: {', '.join([c[0] for c in unique_countries])}")
    print(f"📅 Years: 2000-2020")
    
    # عرض عينة من البيانات
    print("\n📋 Sample data:")
    cursor.execute("SELECT * FROM health_metrics LIMIT 5")
    for row in cursor.fetchall():
        print(f"  {row[1]} ({row[2]}): Life Exp={row[3]}")
    
    conn.close()

def display_database_info():
    """عرض معلومات قاعدة البيانات"""
    print("\n" + "="*50)
    print("DATABASE INFORMATION")
    print("="*50)
    
    conn = sqlite3.connect('health_data.db')
    cursor = conn.cursor()
    
    # عرض الجداول
    cursor.execute('SELECT name FROM sqlite_master WHERE type="table";')
    tables = cursor.fetchall()
    print('📁 Tables in database:')
    for table in tables:
        print(f'  • {table[0]}')
        
        # عرض أعمدة كل جدول
        cursor.execute(f'PRAGMA table_info({table[0]})')
        columns = cursor.fetchall()
        for col in columns:
            print(f'    └─ {col[1]} ({col[2]})')
    
    # إحصائيات الجدول الرئيسي
    cursor.execute('SELECT COUNT(*) FROM health_metrics')
    count = cursor.fetchone()[0]
    print(f'\n📊 Total records in health_metrics: {count:,}')
    
    # توزيع البيانات
    print('\n📈 Data distribution:')
    cursor.execute('SELECT country, COUNT(*) FROM health_metrics GROUP BY country')
    for row in cursor.fetchall():
        print(f'  {row[0]}: {row[1]} records')
    
    conn.close()

if __name__ == "__main__":
    create_sample_database()
    display_database_info()
    
    # إظهار أمر الاستعلام للصورة
    print("\n" + "="*50)
    print("COMMAND FOR SCREENSHOT:")
    print("="*50)
    print('''python -c "
import sqlite3
conn = sqlite3.connect('health_data.db')
cursor = conn.cursor()
cursor.execute('SELECT name FROM sqlite_master WHERE type=\"table\";')
print('Tables:', cursor.fetchall())
cursor.execute('SELECT COUNT(*) FROM health_metrics')
print('Records:', cursor.fetchone()[0])
conn.close()
"''')