from pymongo import MongoClient
from pymongo.server_api import ServerApi
from datetime import datetime
from bson import ObjectId
from bson.errors import InvalidId
from fastapi import HTTPException, status

from schemas import TourCreateSchema, TourSavedSchema
from settings import settings


class MongoDBStorage:
    def __init__(self):
        client = MongoClient(
            settings.MONGO_URI,
            server_api=ServerApi("1")
        )

        db = client[settings.MONGO_DB]
        self.collection = db[settings.MONGO_COLLECTION]

    def create_tour(self, tour: TourCreateSchema):
        tour_dict = tour.model_dump()
        tour_dict["created_at"] = datetime.now()

        result = self.collection.insert_one(tour_dict)

        return self.get_tour(str(result.inserted_id))

    def get_tour(self, tour_id: str):
        try:
            query = {"_id": ObjectId(tour_id)}
        except InvalidId:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid tour id"
            )

        tour = self.collection.find_one(query)

        if not tour:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Tour not found"
            )

        return TourSavedSchema(
            id=str(tour["_id"]),
            title=tour["title"],
            country=tour["country"],
            price=tour["price"],
            duration_days=tour["duration_days"],
            created_at=tour["created_at"]
        )

    def get_all_tours(self):
        tours = []

        for tour in self.collection.find():
            tours.append(
                TourSavedSchema(
                    id=str(tour["_id"]),
                    title=tour["title"],
                    country=tour["country"],
                    price=tour["price"],
                    duration_days=tour["duration_days"],
                    created_at=tour["created_at"]
                )
            )

        return tours

    def delete_tour(self, tour_id: str):
        self.collection.delete_one(
            {"_id": ObjectId(tour_id)}
        )

    def update_tour(self, tour_id: str, tour: TourCreateSchema):
        self.collection.update_one(
            {"_id": ObjectId(tour_id)},
            {"$set": tour.model_dump()}
        )

        return self.get_tour(tour_id)