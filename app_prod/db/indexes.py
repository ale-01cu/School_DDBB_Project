from django.db import connection

def execute_indexes():
    with connection.cursor() as cursor:
                
        # Indices
        
        cursor.execute("""

            CREATE INDEX idx_nombre ON producto (nombre);
            CREATE INDEX idx_categoria ON producto (categoria);

        """)
                        