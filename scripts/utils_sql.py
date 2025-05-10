import psycopg2
from psycopg2.extras import execute_values

def upsert_dataframe(df, db_uri, table_name, pk):
    """
    Generic UPSERT function for any DataFrame and PostgreSQL table.

    Args:
        df (pd.DataFrame): The DataFrame to insert.
        db_uri (str): PostgreSQL connection URI.
        table_name (str): Target table name.
        pk (str): Primary key column for ON CONFLICT.
        add_updated_at (bool): Whether to add 'updated_at' timestamp (MYT).
    """
    if df.empty:
        print("No data to upsert.")
        return

    # Prepare SQL
    columns = list(df.columns)
    values = [tuple(row) for row in df.to_numpy()]

    insert_sql = f"""
        INSERT INTO {table_name} ({', '.join(columns)})
        VALUES %s
        ON CONFLICT ({pk}) DO UPDATE SET
        {', '.join([f"{col} = EXCLUDED.{col}" for col in columns if col != pk])};
    """

    # Connect and execute
    conn = psycopg2.connect(db_uri)
    with conn:
        with conn.cursor() as cur:
            execute_values(cur, insert_sql, values)

    print(f"UPSERT into '{table_name}' complete. Rows processed: {len(values)}")

