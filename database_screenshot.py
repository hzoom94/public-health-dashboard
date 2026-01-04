# انسخ هذا كاملاً والصقه في PowerShell
@'
# database_screenshot.py - Perfect for report screenshot
print("========================================================")
print("          HEALTH DASHBOARD - DATABASE CHECK")
print("========================================================")

import sqlite3
import os
import sys

def main():
    db_file = "health_data.db"
    
    print(f"Database: {db_file}")
    print(f"Current dir: {os.getcwd()}")
    print("-" * 60)
    
    # Check if file exists
    if not os.path.exists(db_file):
        print("❌ ERROR: Database file not found!")
        print("\nCreating sample database...")
        return create_sample_db()
    
    try:
        conn = sqlite3.connect(db_file)
        cursor = conn.cursor()
        
        # Get all tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        
        print(f"📊 TABLES FOUND: {len(tables)}")
        print("-" * 60)
        
        if tables:
            for i, (table_name,) in enumerate(tables, 1):
                print(f"{i}. {table_name}")
                
                # Count rows
                cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                count = cursor.fetchone()[0]
                print(f"   Records: {count:,}")
                
                # Show columns
                cursor.execute(f"PRAGMA table_info({table_name})")
                columns = cursor.fetchall()
                print(f"   Columns: {len(columns)}")
                
                # For health_metrics, show sample
                if table_name == "health_metrics" and count > 0:
                    print(f"\n   Sample data (first 2 rows):")
                    cursor.execute(f"SELECT * FROM {table_name} LIMIT 2")
                    for row in cursor.fetchall():
                        print(f"   {row}")
                
                print()
        
        # Summary
        print("=" * 60)
        print("SUMMARY:")
        print("=" * 60)
        
        if "health_metrics" in [t[0] for t in tables]:
            cursor.execute("SELECT COUNT(*) FROM health_metrics")
            total = cursor.fetchone()[0]
            print(f"Total health records: {total:,}")
            
            cursor.execute("SELECT COUNT(DISTINCT country) FROM health_metrics")
            countries = cursor.fetchone()[0]
            print(f"Countries covered: {countries}")
            
            cursor.execute("SELECT MIN(year), MAX(year) FROM health_metrics")
            min_year, max_year = cursor.fetchone()
            print(f"Year range: {min_year} - {max_year}")
        
        conn.close()
        print("\n✅ Database check completed successfully!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    return True

def create_sample_db():
    """Create a sample database for testing"""
    try:
        conn = sqlite3.connect("health_data.db")
        cursor = conn.cursor()
        
        cursor.execute('''
        CREATE TABLE health_metrics (
            id INTEGER PRIMARY KEY,
            country TEXT,
            year INTEGER,
            life_expectancy REAL,
            child_mortality REAL,
            health_expenditure REAL
        )
        ''')
        
        # Add sample data
        data = [
            ('Japan', 2020, 84.3, 2.1, 10.9),
            ('Germany', 2020, 81.2, 3.4, 11.7),
            ('Brazil', 2020, 75.5, 13.8, 9.5),
        ]
        
        cursor.executemany("INSERT INTO health_metrics VALUES (NULL,?,?,?,?,?)", data)
        conn.commit()
        conn.close()
        
        print("✅ Created sample database with 3 records")
        print("✅ Table: health_metrics")
        return True
        
    except Exception as e:
        print(f"❌ Error creating database: {e}")
        return False

if __name__ == "__main__":
    
    main()
'@ | Out-File -FilePath "database_screenshot.py" -Encoding UTF8