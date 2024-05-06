from typing import List
from schemas.user import Users
from models.user import Users as UsersModel


class UserService():
    def __init__(self, db) -> None:
        self.db = db

    def get_users(self):
        result = self.db.query(UsersModel).all()
        return result
    
    def get_user(self, id):
        result = self.db.query(UsersModel).filter(UsersModel.id == id).first()
        return result
    
    def create_user(self, user:Users):
        new_user = UsersModel(**user.model_dump())
        self.db.add(new_user)
        self.db.commit()
        return
    
    
    def delete_user(self, id: int):
        user_to_delete = self.db.query(UsersModel).filter(UsersModel.id == id).first()
        if user_to_delete:
            self.db.delete(user_to_delete)
            self.db.commit()
            return True
        return False
    
    # def delete_user(self, id:int):
    #     self.db.query(UsersModel).filter(UsersModel.id == id).delete()      
    #     self.db.commit()
    #     return

