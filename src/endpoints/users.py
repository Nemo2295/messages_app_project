from fastapi import APIRouter

from src.pydentic_models import UserBodyModel
from src.app_entities import AppUser
from src.storage_acsses import storage_controller
from src.validations import validations


users_router = APIRouter(prefix="/users", tags=["Users"])


@users_router.post("/", status_code=201)
async def create_user(user: UserBodyModel):
    new_user = AppUser(user.display_name, user.first_name, user.last_name, user.middle_name)
    validations.raise_for_existing_user(new_user.user_id)
    storage_controller.save_user(new_user)
    new_user_id = new_user.user_id
    return {"message": new_user_id}


@users_router.delete("/{user_id}", status_code=200)
async def delete_user(user_id: str):
    validations.raise_for_non_existing_user(user_id)
    storage_controller.delete_user(user_id)
    return {"message": user_id}


@users_router.get("/", status_code=200)
async def get_all_users():
    all_users = storage_controller.retrieve_all_users()
    return {"message": all_users}
