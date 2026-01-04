# check_tables.py
import sqlite3
import sys

def main():
    db_path = 'health_data.db'
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # الحصول على جميع الجداول
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        
        print(f"Database: {db_path}")
        print(f"Tables found: {len(tables)}")
        
        if tables:
            print("\nTable names:")
            for table in tables:
                print(f"  - {table[0]}")
                
                # عرض أعمدة كل جدول
                cursor.execute(f"PRAGMA table_info({table[0]});")
                columns = cursor.fetchall()
                print(f"    Columns: {len(columns)}")
                for col in columns:
                    print(f"      {col[1]} ({col[2]})")
        else:
            print("No tables found in the database.")
            
        conn.close()
        
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    main()