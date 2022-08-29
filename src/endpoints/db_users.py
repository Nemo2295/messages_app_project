from fastapi import APIRouter
import psycopg2
import psycopg2.extras
from typing import List

from src.app_entities import AppUser
from src.pydentic_models import UserBodyModel, UsersId

connection_string = 'user=postgres password=Norway2022 dbname=Nemo_Messages_App host=localhost'

db_users_router = APIRouter(prefix="/db_users", tags=["DB users"])


@db_users_router.post("/", status_code=201)
async def create_user(user: UserBodyModel):
    new_user = AppUser(user.display_name, user.first_name, user.last_name, user.middle_name)
    if not new_user.middle_name:
        new_user.middle_name = "null"
    try:
        db_connection = psycopg2.connect(connection_string)
        my_cursor = db_connection.cursor()
        query = f"INSERT INTO app_users.users VALUES " \
                f"('{new_user.user_id}'," \
                f" '{new_user.display_name}'," \
                f" '{new_user.first_name}'," \
                f" '{new_user.last_name}'," \
                f" '{new_user.middle_name}'," \
                f" '{new_user.registration_date}')"
        my_cursor.execute(query)
        db_connection.commit()
        my_cursor.close()
        db_connection.close()
    except Exception as error:
        print(error)
        return {"message": "User registration was not successful", "user_id": f"{new_user.user_id}"}
    return {"message": "User registration was successful", "user_id": f"{new_user.user_id}"}


@db_users_router.put("/", status_code=201)
async def update_user_information(user_id: str, column_name: str, new_value: str):
    try:
        db_connection = psycopg2.connect(connection_string)
        my_cursor = db_connection.cursor()
        query = f"UPDATE app_users.users SET {column_name} = '{new_value}' WHERE app_users.users.id = '{user_id}' "
        my_cursor.execute(query)
        db_connection.commit()
        my_cursor.close()
        db_connection.close()
    except Exception as error:
        print(error)
    return {"message": f"User update was successful",
            "user_id": user_id}


@db_users_router.delete("/", status_code=200)
async def delete_user(user_id: str):
    try:
        db_connection = psycopg2.connect(connection_string)
        my_cursor = db_connection.cursor()
        query = f"DELETE FROM app_users.users u WHERE u.id = '{user_id}' "
        my_cursor.execute(query)
        db_connection.commit()
        my_cursor.close()
        db_connection.close()
    except Exception as error:
        print(error)
    return {"message": f"User deletion was successful",
            "user_id": user_id}


@db_users_router.get("/", status_code=200)
async def retrieve_user(user_id: str):
    try:
        db_connection = psycopg2.connect(connection_string)
        my_cursor = db_connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        query = f"SELECT * FROM app_users.users u WHERE u.id = '{user_id}'"
        my_cursor.execute(query)
        user_in_db = my_cursor.fetchone()
        db_connection.close()
        user_in_db = AppUser(user_in_db["display_name"],
                             user_in_db["first_name"],
                             user_in_db["last_name"],
                             user_in_db["middle_name"],
                             user_in_db["registration_date"].strftime("%d/%m/%Y %H:%M:%S"),
                             user_in_db["id"])
        return {"message": user_in_db}
    except Exception as e:
        print(e)
    return {"message": f"User was not found in DB",
            "status_code": 404,
            "user_id": user_id}


@db_users_router.get("/all", status_code=200)
async def retrieve_all_users():
    try:
        db_connection = psycopg2.connect(connection_string)
        my_cursor = db_connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        query = f"SELECT * FROM app_users.users"
        my_cursor.execute(query)
        all_users_in_db = my_cursor.fetchall()
        db_connection.close()
        all_users: List[AppUser] = []
        for user in all_users_in_db:
            app_user = AppUser(user["display_name"],
                               user["first_name"],
                               user["last_name"],
                               user["middle_name"],
                               user["registration_date"].strftime("%d/%m/%Y %H:%M:%S"),
                               user["id"])
            all_users.append(app_user)
        return {"message": all_users}
    except Exception as e:
        print(e)
    return {"message": f"User was not found in DB",
            "status_code": 200,
            "user_id": "DB is empty - no users"}


@db_users_router.delete("/multiple", status_code=200)
async def delete_multiple_users_by_id(users_ids: UsersId):
    try:
        db_connection = psycopg2.connect(connection_string)
        my_cursor = db_connection.cursor(cursor_factory=psycopg2.extras.DictCursor)
        query = f"DELETE FROM app_users.users u WHERE u.id IN {tuple(set(users_ids.users_id))}"
        my_cursor.execute(query)
        db_connection.commit()
        my_cursor.close()
        db_connection.close()
        return {"message": "deleted requested users",
                "users_id": users_ids.users_id}
    except Exception as e:
        print(e)
    return {"message": f"Users was not found in DB",
            "status_code": 200,
            "user_id": "DB is empty - no users"}
