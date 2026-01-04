# db_check.py - Updated version
print("=" * 50)
print("     HEALTH DASHBOARD - DATABASE")
print("=" * 50)

import sqlite3

conn = sqlite3.connect("health_data.db")
cursor = conn.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()

print(f"Total Tables: {len(tables)}\n")

for table in tables:
    table_name = table[0]
    print(f"Table: {table_name}")
    
    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
    count = cursor.fetchone()[0]
    print(f"  Records: {count}")
    
    # Show sample ONLY for health_metrics table
    if count > 0 and table_name == "health_metrics":
        cursor.execute(f"SELECT country, year, life_expectancy FROM {table_name} LIMIT 3")
        sample = cursor.fetchall()
        print("  Sample (3 rows):")
        for row in sample:
            print(f"    - {row[0]} ({row[1]}): {row[2]} years")
    elif count > 0:
        # For other tables, show a simple sample
        cursor.execute(f"SELECT * FROM {table_name} LIMIT 1")
        sample = cursor.fetchall()
        if sample:
            print(f"  Sample (1 row): {sample[0]}")
    
    print()

conn.close()
print("=" * 50)
print("DATABASE CHECK COMPLETE")
print("=" * 50)