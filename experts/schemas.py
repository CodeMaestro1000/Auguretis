from pydantic import BaseModel

"""Handles the format for returning a response to the client"""

class ShowItems(BaseModel):
    user_id: int
    number_of_answers: int
    reps: int

    class Config():  #to convert non dict obj to json
        orm_mode = True
