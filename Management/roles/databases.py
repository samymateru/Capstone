from typing import Tuple, List, Dict
from fastapi import HTTPException
from psycopg2.extensions import connection as Connection
from psycopg2.extensions import cursor as Cursor
from Management.roles.schemas import *



def create_new_role(connection: Connection, role: NewRole, company_id: str):
    query = """
                INSERT INTO public.roles (company_id, name, description, category, write, read, delete, edit, assign
                ,approve, created_at) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
    try:
        with connection.cursor() as cursor:
            cursor: Cursor
            cursor.execute(query, (
                company_id,
                role.name,
                role.description,
                role.category,
                role.write,
                role.read,
                role.delete,
                role.edit,
                role.assign,
                role.approve,
                role.created_at
            ))
        connection.commit()
    except Exception as e:
        connection.rollback()
        print(f"Error creating role {e}")
        raise HTTPException(status_code=400, detail="Error creating role")

def update_role(connection: Connection, role_data: UpdateRole):
    query_parts = []
    params = []

    #Check if the role_name is set
    if role_data.name is not None:
        query_parts.append("name = %s")
        params.append(role_data.name)

    #Check if the category is set
    if role_data.category is not None:
        query_parts.append("category = %s")
        params.append(role_data.category)

    #Checl if the description is set
    if role_data.description is not None:
        query_parts.append("description = %s")
        params.append(role_data.description)

    # If no fields to update, raise an error and return
    if not query_parts:
        raise HTTPException(status_code=400, detail="No fields to update")

    # Construct the SET part without trailing commas
    set_clause = ", ".join(query_parts)

    # Add the WHERE condition
    where_clause = "WHERE id = %s"
    params.append(role_data.id)

    # Combine the SET and WHERE parts into the final query
    query = f"UPDATE public.roles SET {set_clause} {where_clause}"
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, tuple(params))
        connection.commit()
    except Exception as e:
        connection.rollback()
        print(f"Error updating role {e}")
        raise HTTPException(status_code=400, detail="Error updating role")


def delete_role(connection: Connection, role_id: int):
    query = """DELETE FROM public.roles WHERE id = %s RETURNING id;"""
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, (role_id,))
        connection.commit()
    except Exception as e:
        connection.rollback()
        print(f"Error delete role {e}")
        raise HTTPException(status_code=400, detail="Error delete role")

def get_roles(connection: Connection, column: str = None, value: str = None, row: str = None) -> List[Dict]:
    query = "SELECT * FROM public.roles "
    if row:
        query = f"SELECT {row} FROM public.roles "
    if column and value:
        query += f"WHERE  {column} = %s"
    try:
        with connection.cursor() as cursor:
            cursor.execute(query, (value,))
            rows = cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            return [dict(zip(column_names, row_)) for row_ in rows]
    except Exception as e:
        connection.rollback()
        print(f"Error querying roles {e}")
        raise HTTPException(status_code=400, detail="Error querying roles")

def get_user_roles(connection: Connection, role_id: List[int]):
    query = "SELECT * FROM public.roles WHERE id = ANY(%s)"
    try:
        with connection.cursor() as cursor:
            # Use IN clause for better performance
            query = f"SELECT * FROM public.roles WHERE id = ANY(%s)"

            # Execute query with list of role IDs
            cursor.execute(query, (role_id,))

            # Fetch all rows and map column names
            rows = cursor.fetchall()
            column_names = [desc[0] for desc in cursor.description]
            role_list = [dict(zip(column_names, row)) for row in rows]
            return role_list
    except Exception as e:
        connection.rollback()
        print(f"Error querying roles {e}")
        raise HTTPException(status_code=400, detail="Error querying roles")
