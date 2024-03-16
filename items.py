from fastapi import APIRouter, HTTPException
from exceptions import MyException, NotFoundException
from models import Item

router = APIRouter(prefix="/items", tags=["items"])

items = {"foo": "this is foo", "woo": "this is woo"}

@router.post("/")
def create_item(item: Item):
    return item

@router.get("/items1/{item_id}")
async def get_item1(item_id: str):
    if item_id not in items:
        raise HTTPException(status_code=404, detail="Item not found")
    return items[item_id]

@router.get("/items2/{item_id}")
async def get_item2(item_id: str):
    if item_id not in items:
        raise NotFoundException(detail="Item not found")
    return items[item_id]

@router.get("/items3/{item_id}")
async def get_item3(item_id: str):
    if item_id not in items:
        raise MyException(item_id=item_id)
    return items[item_id]