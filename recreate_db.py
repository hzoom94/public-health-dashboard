# recreate_db.py
import sqlite3
import os

print("=" * 50)
print("RECREATING DATABASE WITH SAMPLE DATA")
print("=" * 50)

# Remove old database if exists
if os.path.exists("health_data.db"):
    os.remove("health_data.db")
    print("✓ Deleted old database file")

# Create new database
conn = sqlite3.connect("health_data.db")
cursor = conn.cursor()

# Create table
cursor.execute("""
CREATE TABLE health_metrics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    country TEXT NOT NULL,
    year INTEGER NOT NULL,
    life_expectancy REAL
)
""")
print("✓ Created table: health_metrics")

# Add sample data
data = [
    ("Japan", 2020, 84.3),
    ("Germany", 2020, 81.2),
    ("Brazil", 2020, 75.5),
    ("Japan", 2019, 84.1),
    ("Germany", 2019, 80.9),
    ("Brazil", 2019, 75.2)
]

cursor.executemany("INSERT INTO health_metrics (country, year, life_expectancy) VALUES (?, ?, ?)", data)
conn.commit()
print(f"✓ Added {len(data)} records")

# Verify
cursor.execute("SELECT COUNT(*) FROM health_metrics")
count = cursor.fetchone()[0]

cursor.execute("SELECT DISTINCT country FROM health_metrics")
countries = cursor.fetchall()

print(f"\nVERIFICATION:")
print(f"  • Total records: {count}")
print(f"  • Countries: {', '.join([c[0] for c in countries])}")
print(f"  • File size: {os.path.getsize('health_data.db')} bytes")

conn.close()
print("\n" + "=" * 50)
print("✅ DATABASE RECREATION COMPLETE")
print("=" * 50)