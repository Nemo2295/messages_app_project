from .storage_operations import InMemoryStorage
from .storage_operations import UserStorageBase


storage_controller: UserStorageBase = InMemoryStorage()
