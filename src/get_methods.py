from typing import Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.database import connection
from src.models import Media, Theme, Platform, Bond


@connection
async def get_media_by_id(id:int, session:AsyncSession) -> Media:
    media = await session.get(Media,id)
    await session.commit()
    if media is None:
        return Media(id = -1, title ="Error")
    else:
        return media

@connection
async def get_similar_media(input:str , session:AsyncSession) -> Sequence[Media] | None:
    try:
        statement = select(Media).filter(Media.title.ilike(f'{input}%'))
        media_obj = await session.scalars(statement)
        await session.commit()
        return media_obj.all()
    except Exception as e:
        print(e)
        return None

@connection
async def get_theme_by_id(id:int, session:AsyncSession) -> Theme:
    theme = await session.get(Theme,id)
    await session.commit()
    if theme is None:
        return Theme(id = -1, title ="Error")
    else:
        return theme


@connection
async def get_similar_theme(input:str , session:AsyncSession) -> Sequence[Theme] | None:
    try:
        statement = select(Theme).filter(Theme.title.ilike(f'{input}%'))
        theme_obj = await session.scalars(statement)
        await session.commit()
        return theme_obj.all()
    except Exception as e:
        print(e)
        return None


@connection
async def get_platforms_by_media_id(media_id:int, session:AsyncSession) -> Sequence[Platform] | None:
    try:
        statement = select(Platform).where(Platform.media_id == media_id)
        platform_obj = await session.scalars(statement)
        await session.commit()
        return platform_obj.all()
    except Exception as e:
        print(e)
        return None

@connection
async def get_bonds_by_media_id(media_id:int , session:AsyncSession) -> Sequence[Bond] | None:
    try:
        statement = select(Bond).where(Bond.media_id == media_id)
        bond_obj = await session.scalars(statement)
        await session.commit()
        return bond_obj.all()
    except Exception as e:
        print(e)
        return None

@connection
async def get_bonds_by_theme_id(theme_id:int , session:AsyncSession) -> Sequence[Bond] | None:
    try:
        statement = select(Bond).where(Bond.media_id == theme_id)
        bond_obj = await session.scalars(statement)
        await session.commit()
        return bond_obj.all()
    except Exception as e:
        print(e)
        return None