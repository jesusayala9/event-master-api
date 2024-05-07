from typing import List
from schemas.user import Users
from models.user import Users as UsersModel
import bcrypt



class UserService():
    def __init__(self, db) -> None:
        self.db = db
        
        
    def get_user_by_username(self, username: str):
        return self.db.query(UsersModel).filter(UsersModel.username == username).first()
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

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
    
    
    def update_user(self, id:int, data:Users):
            user = self.db.query(UsersModel).filter(UsersModel.id == id).first() 
            user.id = data.id        
            user.username = data.username
            user.email = data.email
            user.password = data.password
            user.events = data.events
            user.created_events = data.created_events
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

