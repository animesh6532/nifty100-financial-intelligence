"""
Backup database script
"""

import subprocess
import datetime


def backup_database():
    """Backup PostgreSQL database"""
    timestamp = datetime.datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f'nifty100_backup_{timestamp}.sql'
    
    try:
        subprocess.run([
            'pg_dump',
            '-U', 'postgres',
            '-h', 'localhost',
            'nifty100_db',
            f'> {filename}'
        ])
        print(f"Backup created: {filename}")
    except Exception as e:
        print(f"Backup failed: {str(e)}")


if __name__ == '__main__':
    backup_database()
