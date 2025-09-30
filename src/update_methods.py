from http.client import HTTPException

from sqlalchemy.ext.asyncio import AsyncSession
from src.database import connection
from src.get_methods import get_media_by_id
from src.models import Media, Theme, Platform, Bond
from datetime import  datetime


@connection
async def update_media(media_id: int,session:AsyncSession, title:str = None ,type:str = None, poster_url:str = None, description:str = None, release_date:datetime = None) -> int:
    # TODO: add logic
    return 0