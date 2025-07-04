"""
Simple database module for storing carbon footprint calculations
"""

import os
import json
import psycopg2
from datetime import datetime
from typing import List, Dict, Optional

class DatabaseManager:
    """Simple PostgreSQL database manager for carbon footprint data"""
    
    def __init__(self):
        self.connection_string = os.environ.get("DATABASE_URL")
        if not self.connection_string:
            raise ValueError("DATABASE_URL environment variable not found")
        self._create_tables()
    
    def _get_connection(self):
        """Get database connection"""
        return psycopg2.connect(self.connection_string)
    
    def _create_tables(self):
        """Create the necessary database tables"""
        create_table_sql = """
        CREATE TABLE IF NOT EXISTS carbon_calculations (
            id SERIAL PRIMARY KEY,
            user_id VARCHAR(255),
            calculation_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            total_emissions DECIMAL(10,2),
            travel_emissions DECIMAL(10,2),
            transport_emissions DECIMAL(10,2),
            diet_emissions DECIMAL(10,2),
            shopping_emissions DECIMAL(10,2),
            home_energy_emissions DECIMAL(10,2),
            lifestyle_data JSONB,
            recommendations JSONB,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        
        try:
            with self._get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(create_table_sql)
                conn.commit()
        except Exception as e:
            print(f"Error creating tables: {e}")
    
    def save_calculation(self, user_id: str, results: Dict, recommendations: List = None) -> Optional[int]:
        """Save a carbon footprint calculation"""
        insert_sql = """
        INSERT INTO carbon_calculations 
        (user_id, total_emissions, travel_emissions, transport_emissions, 
         diet_emissions, shopping_emissions, home_energy_emissions, 
         lifestyle_data, recommendations)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        RETURNING id;
        """
        
        try:
            with self._get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(insert_sql, (
                        user_id,
                        results['total_emissions'],
                        results['breakdown']['travel'],
                        results['breakdown']['transport'],
                        results['breakdown']['diet'],
                        results['breakdown']['shopping'],
                        results['breakdown']['home_energy'],
                        json.dumps(results['lifestyle_data']),
                        json.dumps(recommendations or [])
                    ))
                    record_id = cursor.fetchone()[0]
                conn.commit()
                return record_id
        except Exception as e:
            print(f"Error saving calculation: {e}")
            return None
    
    def get_user_history(self, user_id: str, limit: int = 10) -> List[Dict]:
        """Get calculation history for a user"""
        select_sql = """
        SELECT id, calculation_date, total_emissions, travel_emissions, 
               transport_emissions, diet_emissions, shopping_emissions, 
               home_energy_emissions, lifestyle_data, recommendations
        FROM carbon_calculations 
        WHERE user_id = %s 
        ORDER BY calculation_date DESC 
        LIMIT %s;
        """
        
        try:
            with self._get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(select_sql, (user_id, limit))
                    rows = cursor.fetchall()
                    
                    results = []
                    for row in rows:
                        results.append({
                            'id': row[0],
                            'date': row[1],
                            'total_emissions': float(row[2]),
                            'breakdown': {
                                'travel': float(row[3]),
                                'transport': float(row[4]),
                                'diet': float(row[5]),
                                'shopping': float(row[6]),
                                'home_energy': float(row[7])
                            },
                            'lifestyle_data': row[8] or {},
                            'recommendations': row[9] or []
                        })
                    return results
        except Exception as e:
            print(f"Error getting user history: {e}")
            return []
    
    def get_statistics(self) -> Dict:
        """Get general statistics about all calculations"""
        stats_sql = """
        SELECT 
            COUNT(*) as total_calculations,
            AVG(total_emissions) as avg_emissions,
            MAX(calculation_date) as latest_calculation
        FROM carbon_calculations;
        """
        
        try:
            with self._get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(stats_sql)
                    row = cursor.fetchone()
                    
                    return {
                        'total_calculations': row[0] or 0,
                        'average_emissions': round(float(row[1] or 0), 2),
                        'latest_calculation': row[2]
                    }
        except Exception as e:
            print(f"Error getting statistics: {e}")
            return {
                'total_calculations': 0,
                'average_emissions': 0,
                'latest_calculation': None
            }
    
    def delete_user_data(self, user_id: str) -> bool:
        """Delete all data for a specific user"""
        delete_sql = "DELETE FROM carbon_calculations WHERE user_id = %s;"
        
        try:
            with self._get_connection() as conn:
                with conn.cursor() as cursor:
                    cursor.execute(delete_sql, (user_id,))
                    deleted_count = cursor.rowcount
                conn.commit()
                return deleted_count > 0
        except Exception as e:
            print(f"Error deleting user data: {e}")
            return False
