from sqlalchemy.ext.asyncio import AsyncSession
from src.database import connection
from src.models import Media, Theme, Platform, Bond
from asyncio import run
from datetime import  datetime

@connection
async def create_media(title:str, session:AsyncSession ,type:str = "", poster_url:str = "", description:str = "", release_date:datetime = None) -> int:
    media = Media(title = title, type = type, poster_url = poster_url, description = description, release_date = release_date)
    session.add(media)
    await session.commit()
    return media.id

@connection
async def create_theme(title:str, description:str, session:AsyncSession) -> int:
    theme = Theme(title=title, description=description)
    session.add(theme)
    await session.commit()
    return theme.id

@connection
async def create_platform(media_id:int, title:str, ref_link:str, session:AsyncSession) -> int:
    platform = Platform(media_id = media_id,title=title, ref_link=ref_link)
    session.add(platform)
    await session.commit()
    return platform.id

@connection
async def create_bond(media_id:int, theme_id:id, description:str, session:AsyncSession) -> int:
    bond = Bond(media_id=media_id, theme_id=theme_id,description=description)
    session.add(bond)
    await session.commit()
    return bond.id

