from models.user import User as UserModel
from schemas.user import User


class UserService():

    def __init__(self, db) -> None:
        self.db = db

    def get_users(self):
        result = self.db.query(UserModel).all()
        return result
    
    def create_user(self, user:User):
        new_user = UserModel(**user.model_dump())
        self.db.add(new_user)
        self.db.commit()
        return