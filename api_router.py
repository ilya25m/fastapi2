from fastapi import APIRouter, status

from schemas import TourCreateSchema, TourSavedSchema
from storage import MongoDBStorage

storage = MongoDBStorage()

api_router = APIRouter(
    prefix="/api/tours"
)


@api_router.post("", status_code=status.HTTP_201_CREATED)
def create_tour(tour: TourCreateSchema) -> TourSavedSchema:
    return storage.create_tour(tour)


@api_router.get("")
def get_all_tours():
    return storage.get_all_tours()


@api_router.get("/{tour_id}")
def get_tour(tour_id: str):
    return storage.get_tour(tour_id)


@api_router.put("/{tour_id}")
def update_tour(
    tour_id: str,
    tour: TourCreateSchema
):
    return storage.update_tour(tour_id, tour)


@api_router.delete("/{tour_id}")
def delete_tour(tour_id: str):
    storage.delete_tour(tour_id)

    return {
        "message": "Tour deleted"
    }