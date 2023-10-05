from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship



from .database import Base
# from database import Base

class Post(Base):
    __tablename__ = "posts"

    post_id = Column(Integer, primary_key=True, index=True)
    post_title = Column(String, index=True)
    post_body = Column(Text)
    post_origin_id = Column(Integer)
    api_result = Column(Text)
