from fastapi import APIRouter, HTTPException

from app.twitter import get_user


router = APIRouter()


@router.get('/user/{twitter_handle}')
async def user(twitter_handle: str):

    output = get_user(twitter_handle)

    return output
