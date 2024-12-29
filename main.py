from fastapi import FastAPI, Query, Body
from fastapi.openapi.docs import get_swagger_ui_html
import uvicorn


app = FastAPI(docs_url=None)


hotels = [
    {"id": 1, "title": "Sochi-hotel", "name": "Sochi"},
    {"id": 2, "title": "Дубай-hotel", "name": "Дубай"},
]


@app.get("/hotels")
def get_hotels(
        id: int | None = Query(None, description="Айдишник"),
        title: str | None = Query(None, description="Название отеля"),
):
    hotels_ = []
    for hotel in hotels:
        if id and hotel["id"] != id:
            continue
        if title and hotel["title"] != title:
            continue
        hotels_.append(hotel)
    return hotels_


@app.put("/hotels/{hotel_id}")
def put_hotels(
        hotel_id: int,
        title: str = Body(),
        name: str = Body(),
):
    hotel = next((hotel for hotel in hotels if hotel["id"] == hotel_id), None)

    if hotel is None:
        return {"status": "!OK"}

    hotel["title"] = title
    hotel["name"] = name

    return {"status": "OK"}


@app.patch("/hotels/{hotel_id}")
def patch_hotels(
        hotel_id: int,
        title: str | None = Body(None),
        name: str | None = Body(None),
):
    hotel = next((hotel for hotel in hotels if hotel["id"] == hotel_id), None)

    if hotel is None:
        return {"status": "!OK"}

    hotel["title"] = title if title else hotel["title"]
    hotel["name"] = name if name else hotel["name"]

    return {"status": "OK"}


@app.post("/hotels")
def create_hotel(
        title: str = Body(),
        name: str = Body(),
):
    global hotels
    hotels.append({
        "id": hotels[-1]["id"] + 1,
        "title": title,
        "name": name
    })
    return {"status": "OK"}


@app.delete("/hotels/{hotel_id}")
def delete_hotel(hotel_id: int):
    global hotels
    hotels = [hotel for hotel in hotels if hotel["id"] != hotel_id]
    return {"status": "OK"}


@app.get("/docs", include_in_schema=False)
async def custom_swagger_ui_html():
    return get_swagger_ui_html(
        openapi_url=app.openapi_url,
        title=app.title + " - Swagger UI",
        oauth2_redirect_url=app.swagger_ui_oauth2_redirect_url,
        swagger_js_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui-bundle.js",
        swagger_css_url="https://unpkg.com/swagger-ui-dist@5/swagger-ui.css",
    )


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)