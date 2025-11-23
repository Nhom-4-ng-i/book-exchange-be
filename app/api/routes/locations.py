from fastapi import APIRouter
from app.crud.locations import (
    get_locations_list,
    get_location,
    insert_location,
    update_location,
    delete_location
)
from app.schemas.locations import InsertUpdateLocationRequest


router = APIRouter(prefix="/locations", tags=["locations"])


@router.get("/")
async def get_locations_list_route():
    locations = get_locations_list()
    locations = [{"id": location["id"], "name": location["name"]}
                 for location in locations]
    return locations


@router.get("/{location_id}")
async def get_location_route(location_id: int):
    location = get_location(id=location_id)
    return {"id": location["id"], "name": location["name"]}


@router.post("/")
async def insert_location_route(location_request: InsertUpdateLocationRequest):
    name = location_request.name
    insert_location(name=name)


@router.put("/{location_id}")
async def update_location_route(location_id: int, location_request: InsertUpdateLocationRequest):
    name = location_request.name
    update_location(id=location_id, name=name)


@router.delete("/{location_id}")
async def delete_location_route(location_id: int):
    delete_location(id=location_id)
