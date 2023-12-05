from fastapi import FastAPI, HTTPException
from typing import Optional, Dict
from fastapi import Request
import aiosqlite
import os
import sys
import logging

app = FastAPI()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("app.log"),
        logging.StreamHandler()
    ]
)

db_name = os.environ.get('DB_NAME', 'db')
return_item_limit = int(os.environ.get('RETURN_ITEM_LIMIT', '500'))

# Full path to the SQLite database file in the Documents folder
database_path = f"/databases/{db_name}.sqlite"

# Check if the database file exists before proceeding
if not os.path.exists(database_path):
    raise FileNotFoundError(f"The database file '{database_path}' does not exist.")
    sys.exit(1)

async def dynamic_query(table_name, conditions, limit=return_item_limit, all_fields=False):
    async with aiosqlite.connect(database_path) as conn:
        cursor = await conn.cursor()

        query_conditions = []
        values = []

        for column, value in conditions.items():
            if '*' in value:
                query_conditions.append(f"LOWER({column}) LIKE ?")
                values.append(f'%{value.replace("*", "").lower()}%')
            else:
                query_conditions.append(f"LOWER({column}) = ?")
                values.append(value.lower())

        query = f"SELECT * FROM {table_name} WHERE {' AND '.join(query_conditions)}"
        query += f" LIMIT ?"

        # Use parameterized query to prevent SQL injection
        await cursor.execute(query, (*values, limit))

        columns = [desc[0] for desc in cursor.description]
        result = await cursor.fetchall()

        if all_fields:
            result_as_json = [dict(zip(columns, row)) for row in result]
        else:
            result_as_json = [dict((k, v) for k, v in zip(columns, row) if v) for row in result]

    return result_as_json

@app.get("/api/{table_name}")
async def read_item(table_name: str, request: Request):
    try:
        params = dict(request.query_params)
        all_fields = params.pop("all_fields", False)  # Remove and get the value of all_fields
        result = await dynamic_query(table_name, params, all_fields=all_fields)
        logging.info(f"Query successful for table '{table_name}' with conditions {params}")
        return result
    except Exception as e:
        logging.error(f"Error processing query for table '{table_name}' with conditions {params}: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
