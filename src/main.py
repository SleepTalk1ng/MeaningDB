import os.path
from datetime import datetime
from http.client import HTTPException
from typing import Optional

from fastapi import FastAPI, Request, Form
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from starlette.templating import Jinja2Templates

from src.add_methods import create_media, create_theme, create_platform, create_bond
from src.get_methods import get_media_by_id, get_theme_by_id, get_similar_media, get_similar_theme, \
    get_platforms_by_media_id, get_bonds_by_media_id, get_bonds_by_theme_id
from src.models import Media, Theme, Platform

app = FastAPI(title="MNDB")

current_file_path = os.path.dirname(__file__)
static_dir = os.path.join(current_file_path, "static")
templates_dir = os.path.join(current_file_path, "templates")

app.mount("/static", StaticFiles(directory=static_dir), name="static")

templates = Jinja2Templates(directory=templates_dir)

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    """Главная страница с поиском"""
    return templates.TemplateResponse("search.html", {"request": request})


@app.get("/search/", response_class=HTMLResponse)
async def search_results(
        request: Request,
        query: Optional[str] = None
):

    results = []

    if query:

        content =  await get_similar_media(query)
        if content is not None:
            for media in content:
                results.append({"title":f"{media.title}", "url":f"/media/{media.id}", "snippet": f"{media.description.split()[:20]} ..."})

        content = await get_similar_theme(query)
        if content is not None:
            for theme in content:
                results.append({"title": f"{theme.title}", "url": f"/theme/{theme.id}",
                                "snippet": f"{theme.description.split()[:20]} ..."})





    return templates.TemplateResponse(
        "search_results.html",
        {
            "request": request,
            "query": query,
            "results": results,
            "results_count": len(results)
        }
    )

@app.get("/api/search_suggestions")
async def autocomplete(q:str = ""):
    media_result = await get_similar_media(q)
    suggestions = []
    try:
        for media in media_result:
            suggestions.append({"id": media.id, "title": media.title, "type": media.type, "url": f"/media/{media.id}"})
            print(media.title)

        return suggestions

    except Exception as e:
        print(e)

@app.get("/media/add_platform/", response_class=HTMLResponse)
async def add_platform_screen(request: Request):


    return templates.TemplateResponse(
        "add_platform.html",
        {
            "request":request,
        }
    )

@app.post("/media/add_platform/", response_class=HTMLResponse)
async def add_platform(
        request: Request,
        media_id:int = Form(...),
        title: str = Form(...),
        ref_link: str = Form(...)
):
    print(await create_platform(media_id=media_id,title=title, ref_link=ref_link))

    return templates.TemplateResponse("add_successful.html", {"request": request})


@app.get("/media/add_bond/", response_class=HTMLResponse)
async def add_bond(request:Request):
    return templates.TemplateResponse("add_bond.html",{"request":request})

@app.post("/media/add_bond/", response_class=HTMLResponse)
async def add_platform(
        request: Request,
        media_id:int = Form(...),
        theme_id:int  = Form(...),
        description: str = Form(...)
):
    print(await create_bond(media_id=media_id,theme_id=theme_id, description = description))

    return templates.TemplateResponse("add_successful.html", {"request": request})



@app.get("/media/{media_id}", response_class=HTMLResponse)
async def media_detail(request: Request, media_id: int):

    media:Media = await get_media_by_id(media_id)

    result = await get_platforms_by_media_id(media_id)
    platforms = []
    if result is not None:
        for platform in result:
            platforms.append({"url" : platform.ref_link, "name" : platform.title})

    result_2 = await get_bonds_by_media_id(media_id)
    themes = []
    if result_2 is not None:
        for theme in result_2:
            title = await get_theme_by_id(theme.theme_id)
            themes.append({"title": title.title,"description": theme.description, "id": theme.theme_id})



    media_data = {"title" : media.title,
                  "type" : media.type,
                  "poster_url": media.poster_url,
                  "description": media.description,
                  "release_date": media.release_date,
                  "platforms" : platforms,
                  "themes" : themes
                  }

    return templates.TemplateResponse(
        "media_detail.html",
        {
            "request": request,
            "media": media_data
        }
    )





@app.get("/add_media/", response_class=HTMLResponse)
async def add_media_screen(request: Request):
    return templates.TemplateResponse("add_media.html", {"request" : request})

@app.post("/add_media/", response_class=HTMLResponse)
async def add_media(
        request:Request,
        title:str = Form(...),
        type:str = Form(...),
        poster_url:str = Form(...),
        description:str = Form(...),
        release_date:datetime = Form(...)
):
    print(await create_media(title=title, type=type, poster_url=poster_url, description=description, release_date=release_date))

    return templates.TemplateResponse("add_successful.html", {"request" : request})

@app.get("/theme/{theme_id}", response_class=HTMLResponse)
async def theme_detail(request: Request, theme_id: int):

    theme:Theme = await get_theme_by_id(theme_id)

    result = await get_bonds_by_theme_id(theme_id)
    media_id = []
    if result is not None:
        for bond in result:
            media_id.append(bond.media_id)
            print(bond.id)
    else:
        print(result)

    media_id = set(media_id)

    media_data = []
    for id in media_id:
        tmp = await get_media_by_id(id)
        media_data.append({"title":tmp.title, "id": tmp.id})

    theme_data = {
        "title" : theme.title,
        "description": theme.description
    }

    return templates.TemplateResponse(
        "theme_detail.html",
        {
            "request": request,
            "theme": theme_data,
            "media" : media_data
        }
    )


@app.get("/add_theme/", response_class=HTMLResponse)
async def add_theme_screen(request: Request):
    return  templates.TemplateResponse("add_theme.html", {"request" : request})

@app.post("/add_theme/", response_class=HTMLResponse)
async def add_theme(
        request:Request,
        title:str = Form(...),
        description:str = Form(...)
):
    print(await create_theme(title=title, description=description))
    return  templates.TemplateResponse("add_successful.html", {"request": request})