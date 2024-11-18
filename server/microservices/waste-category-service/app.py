import os

from fastapi import FastAPI, Body, HTTPException, status
from fastapi.responses import Response

from bson import ObjectId
import motor.motor_asyncio
from pymongo import ReturnDocument

from model import WasteCategoryModel, WasteCategoryCollection, UpdateWasteCategoryModel


app = FastAPI(
    title="Category Course API",
    summary="A sample application showing how to use FastAPI to add a ReST API to a MongoDB collection.",
)
MONGO_URL = "mongodb+srv://haonngcs220336:microservice@microservicedb.754np.mongodb.net/?retryWrites=true&w=majority&appName=microserviceDB"
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URL)
db = client["Project"]
waste_category_collection = db.get_collection("wastecategories")


@app.post(
    "/waste_categories/",
    response_description="Add new category",
    response_model=WasteCategoryModel,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
async def create_category(waste_category: WasteCategoryModel = Body(...)):
    new_category = await waste_category_collection.insert_one(
        waste_category.model_dump(by_alias=True, exclude=["id"])
    )
    created_waste_category = await waste_category_collection.find_one(
        {"_id": new_category.inserted_id}
    )
    return created_waste_category

@app.get(
    "/waste_categories/",
    response_description="List all categories",
    response_model=WasteCategoryCollection,
    response_model_by_alias=False,
)
async def list_categories():
    return WasteCategoryCollection(waste_categories=await waste_category_collection.find().to_list(1000))


@app.get(
    "/waste_categories/{id}",
    response_description="Get a single category",
    response_model=WasteCategoryModel,
    response_model_by_alias=False,
)
async def show_category(id: str):
    if (
        waste_category := await waste_category_collection.find_one({"_id": ObjectId(id)})
    ) is not None:
        return waste_category

    raise HTTPException(status_code=404, detail=f"Waste category {id} not found")


@app.put(
    "/waste_categories/{id}",
    response_description="Update a waste category",
    response_model=WasteCategoryModel,
    response_model_by_alias=False,
)
async def update_category(id: str, waste_category: UpdateWasteCategoryModel = Body(...)):
    waste_category = {
        k: v for k, v in waste_category.model_dump(by_alias=True).items() if v is not None
    }

    if len(waste_category) >= 1:
        update_result = await waste_category_collection.find_one_and_update(
            {"_id": ObjectId(id)},
            {"$set": waste_category},
            return_document=ReturnDocument.AFTER,
        )
        if update_result is not None:
            return update_result
        else:
            raise HTTPException(status_code=404, detail=f"Category {id} not found")

    # The update is empty, but we should still return the matching document:
    if (existing_waste_category := await waste_category_collection.find_one({"_id": id})) is not None:
        return existing_waste_category

    raise HTTPException(status_code=404, detail=f"Category {id} not found")


@app.delete("/waste_categories/{id}", response_description="Delete a category")
async def delete_category(id: str):
    delete_result = await waste_category_collection.delete_one({"_id": ObjectId(id)})

    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"Category {id} not found")
