from typing import List

from sqlalchemy.orm import Session
from sqlalchemy import and_

from src.database.models import Rating, User, Service
from src.schemas.rating_schemas import RatingModel

from fastapi import HTTPException


async def get_average_rating(service_id, db: Session):
    """
    The get_average_rating function takes in an image_id and a database session.
    It then queries the Rating table for all ratings associated with that image_id.
    If there are no ratings, it returns 0 as the average rating. If there are ratings, 
    it sums up all of the star values (one star = 1 point, two stars = 2 points etc.) 
    and divides by the number of total votes to get an average rating.
    
    :param service_id: Find the image in the database
    :param db: Session: Access the database
    :return: The average rating of the image with the given id
    """
    service_ratings = db.query(Rating).filter(Rating.service_id == service_id).all()
    if len(service_ratings) == 0:
        return 0
    sum_user_rating = 0
    for element in service_ratings:
        if element.one_star:
            sum_user_rating += 1
        if element.two_stars:
            sum_user_rating += 2
        if element.three_stars:
            sum_user_rating += 3
        if element.four_stars:
            sum_user_rating += 4
        if element.five_stars:
            sum_user_rating += 5
    average_user_rating = sum_user_rating / len(service_ratings)
    return average_user_rating


async def get_rating(rating_id: int, db: Session) -> Rating:
    """
    The get_rating function returns a rating object from the database.
        
    
    :param rating_id: int: Specify the id of the rating that you want to get
    :param db: Session: Pass the database session to the function
    :return: A rating object, which is a sqlalchemy model
    """
    return db.query(Rating).filter(Rating.id == rating_id).first()


def get_service(db: Session, image_id: int):

    service = db.query(Service).filter(Service.id == image_id).first()
    if not service:
        raise HTTPException(status_code=404, detail="Image not found")
    return service


async def create_rating(service_id: int, body: RatingModel, user: User, db: Session) -> Rating:
    service_in_database = get_service(db, service_id)
    if service_in_database.user_id == user.id:
        return None
    sum_of_rates = 0
    for el in body:
        if el[1]:
            sum_of_rates += 1
    if sum_of_rates != 1:
        return None
    rating_in_database = db.query(Rating).filter(Rating.service_id == service_id, Rating.user_id == user.id).first()
    if rating_in_database:
        return rating_in_database
    rating = Rating(one_star=body.one_star, two_stars=body.two_stars, three_stars=body.three_stars,
                    four_stars=body.four_stars, five_stars=body.five_stars, user_id=user.id, service_id=service_id)
    db.add(rating)
    db.commit()
    db.refresh(rating)
    return rating


async def update_rating(rating_id: int, body: RatingModel, db: Session):
    """
    The update_rating function updates a rating in the database.
        
    
    :param rating_id: int: Identify which rating to update
    :param body: RatingModel: Get the data from the request body
    :param db: Session: Pass the database session to the function
    :return: The rating object if the rating exists in the database
    """
    sum_of_rates = 0
    for el in body:
        if el[1]:
            sum_of_rates += 1
    if sum_of_rates > 1:
        return None
    rating = db.query(Rating).filter(Rating.id == rating_id).first()
    if rating:
        rating.one_star = body.one_star
        rating.two_stars = body.two_stars
        rating.three_stars = body.three_stars
        rating.four_stars = body.four_stars
        rating.five_stars = body.five_stars
        db.commit()
    return rating


async def remove_rating(rating_id: int, db: Session):
    """
    The remove_rating function removes a rating from the database.
        
    
    :param rating_id: int: Tell the function which rating to delete
    :param db: Session: Pass the database session to the function
    :return: A rating object
    """
    rating = db.query(Rating).filter(Rating.id == rating_id).first()
    if rating:
        db.delete(rating)
        db.commit()
    return rating
