"""
import psycopg2

connection_string = 'user=postgres password=Norway2022 dbname=Nemo_Messages_App host=localhost'

app = FastAPI(title="Nemo messaging app with db")


@app.post("/users/db", tags=["Users"])
async def create_user(user: User):
    new_user = AppUser(user.display_name, user.first_name, user.last_name, user.middle_name)
    print(new_user.__dict__)
    try:
        db_connection = psycopg2.connect(connection_string)
        my_cursor = db_connection.cursor()
        query = f"INSERT INTO app_users.users VALUES " \
                f"('{new_user.id}'," \
                f" '{new_user.display_name}'," \
                f" '{new_user.first_name}'," \
                f" '{new_user.last_name}'," \
                f" '{new_user.middle_name}'," \
                f" '{new_user.registration_date}')"
        my_cursor.execute(query)
        db_connection.commit()
        db_connection.close()
    except Exception as e:
        print("something wrong happened", e)
    return {"message": f"User {new_user.id} registration was successful"}


@app.get("/users/db", tags=["DB Users"])
async def create_user(user_id: str):
    try:
        db_connection = psycopg2.connect(connection_string)
        my_cursor = db_connection.cursor()
        query = f"SELECT * FROM app_users.users u WHERE u.id = '{user_id}'"
        my_cursor.execute(query)
        result = my_cursor.fetchall()
        db_connection.close()
        print(result)
        return result
    except Exception as e:
        print(e)
    return {"message": f"User was not found in DB",
            "status_code": 404,
            "user_id": user_id}
"""

"""
import requests
import json

url = "http://127.0.0.1:8000/db_users"

payload = json.dumps({
  "display_name": "shwazi",
  "first_name": "shiraz",
  "last_name": "benhaim",
  "middle_name": "aliza"
})
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
"""

"""
import requests

url = "http://127.0.0.1:8000/db_users/all"

payload={}
headers = {}

response = requests.request("GET", url, headers=headers, data=payload)

print(response.text)
"""