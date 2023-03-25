from pydantic import BaseModel
"""Handles the format for returning a response to the client"""

class QueryCreate(BaseModel):
    """For semantic search post request"""
    query: str
    api_key: str
    
