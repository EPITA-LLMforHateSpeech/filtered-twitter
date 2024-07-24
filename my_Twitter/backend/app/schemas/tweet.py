from pydantic import BaseModel
from typing import Optional

class TweetBase(BaseModel):
    tweet_id: str
    tweet: str
    user: str
    likes: int
    retweets: int
    retweet_id: Optional[str] = None
    logreg_prob: Optional[float] = None
    logreg_result: Optional[int] = None
    cnn_prob: Optional[float] = None
    cnn_result: Optional[int] = None
    admin_result: Optional[int] = None

class TweetCreate(TweetBase):
    pass

class Tweet(TweetBase):
    id: int

    class Config:
        orm_mode = True
