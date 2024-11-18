import os

from fastapi import FastAPI, Body, HTTPException, status
from fastapi.responses import Response

from bson import ObjectId
import motor.motor_asyncio
from pymongo import ReturnDocument

from model import ChallengeModel, ChallengeCollection, UpdateChallengeModel


app = FastAPI(
    title="Challenges API",
    summary="A sample application showing how to use FastAPI to add a ReST API to a MongoDB collection.",
)
MONGO_URL = "mongodb+srv://haonngcs220336:microservice@microservicedb.754np.mongodb.net/?retryWrites=true&w=majority&appName=microserviceDB"
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URL)
db = client["Project"]
challenge_collection = db.get_collection("challenges")

@app.post(
    "/challenges/",
    response_description="Add new challenge",
    response_model=ChallengeModel,
    status_code=status.HTTP_201_CREATED,
    response_model_by_alias=False,
)
async def create_challenge(challenge: ChallengeModel = Body(...)):
    """
    Insert a new challenge record.

    A unique `id` will be created and provided in the response.
    """
    new_challenge = await challenge_collection.insert_one(
        challenge.model_dump(by_alias=True, exclude=["id"])
    )
    created_challenge = await challenge_collection.find_one(
        {"_id": new_challenge.inserted_id}
    )
    return created_challenge


@app.get(
    "/challenges/",
    response_description="List all challenges",
    response_model=ChallengeCollection,
    response_model_by_alias=False,
)
async def list_challenges():
    """
    List all of the challenge data in the database.

    The response is unpaginated and limited to 1000 results.
    """
    return ChallengeCollection(challenges=await challenge_collection.find().to_list(1000))


@app.get(
    "/challenges/{id}",
    response_description="Get a single challenge",
    response_model=ChallengeModel,
    response_model_by_alias=False,
)
async def show_challenge(id: str):
    """
    Get the record for a specific challenge, looked up by `id`.
    """
    if (
        challenge := await challenge_collection.find_one({"_id": ObjectId(id)})
    ) is not None:
        return challenge

    raise HTTPException(status_code=404, detail=f"Challenge {id} not found")


@app.put(
    "/challenges/{id}",
    response_description="Update a challenge",
    response_model=ChallengeModel,
    response_model_by_alias=False,
)
async def update_challenge(id: str, challenge: UpdateChallengeModel = Body(...)):
    """
    Update individual fields of an existing challenge record.

    Only the provided fields will be updated.
    Any missing or `null` fields will be ignored.
    """
    challenge = {
        k: v for k, v in challenge.model_dump(by_alias=True).items() if v is not None
    }

    if len(challenge) >= 1:
        update_result = await challenge_collection.find_one_and_update(
            {"_id": ObjectId(id)},
            {"$set": challenge},
            return_document=ReturnDocument.AFTER,
        )
        if update_result is not None:
            return update_result
        else:
            raise HTTPException(status_code=404, detail=f"Challenge {id} not found")

    # The update is empty, but we should still return the matching document:
    if (existing_challenge := await challenge_collection.find_one({"_id": id})) is not None:
        return existing_challenge

    raise HTTPException(status_code=404, detail=f"Challenge {id} not found")


@app.delete("/challenges/{id}", response_description="Delete a challenge")
async def delete_challenge(id: str):
    """
    Remove a single challenge record from the database.
    """
    delete_result = await challenge_collection.delete_one({"_id": ObjectId(id)})

    if delete_result.deleted_count == 1:
        return Response(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"Challenge {id} not found")
