import os

from fastapi import APIRouter, Depends, UploadFile, File, status
from sqlalchemy.orm import Session
from dotenv import load_dotenv

from src.database.db import get_db
from src.database.models import User, Role
from src.schemas.service_schemas import ServiceAddResponse, ServiceUpdateModel, ServiceAddModel, ServiceAddTagResponse, \
    ServiceAddTagModel, ServiceGetAllResponse, ServiceGetResponse, ServiceDeleteResponse, ServiceUpdateDescrResponse, \
    ServiceAdminGetAllResponse
from src.repository import services
from src.services.auth import auth_service
from src.services.roles import RolesAccess

load_dotenv()

router = APIRouter(prefix='/services', tags=["services"])

access_all = RolesAccess([Role.admin, Role.moderator, Role.user])
access_admin = RolesAccess([Role.admin])


@router.get("", response_model=ServiceGetAllResponse, dependencies=[Depends(access_all)])
async def get_services(db: Session = Depends(get_db),
                     current_user: User = Depends(auth_service.get_current_user)):
    """
    The get_images function returns a list of images that the current user has uploaded.

    :param db: Session: Pass the database session to the function
    :param current_user: User: Get the current user's information
    :return: A list of all images associated with the current user
    """

    user_services = await services.get_services(db, current_user)
    return {"services": user_services}


@router.get("/service_id/{id}", response_model=ServiceGetResponse, dependencies=[Depends(access_all)])
async def get_service(id: int, db: Session = Depends(get_db),
                    current_user: User = Depends(auth_service.get_current_user)):
    user_service, ratings, comments = await services.get_service(db, id, current_user)
    return {"service": user_service, "ratings": ratings, "comments": comments}


@router.get("/user_id/{user_id}", response_model=ServiceAdminGetAllResponse, dependencies=[Depends(access_admin)])
async def admin_get_services(user_id: int, db: Session = Depends(get_db),
                           current_user: User = Depends(auth_service.get_current_user)):
    user_response = await services.admin_get_service(db, user_id)
    return {"services": user_response}

#
# @router.post("/add", response_model=ServiceAddResponse, status_code=status.HTTP_201_CREATED,
#              dependencies=[Depends(access_all)])
# async def upload_image(body: ServiceAddModel = Depends(), file: UploadFile = File(), db: Session = Depends(get_db),
#                        current_user: User = Depends(auth_service.get_current_user)):
#     cloudinary.config(
#             cloud_name=os.environ.get('CLOUDINARY_NAME'),
#             api_key=os.environ.get('CLOUDINARY_API_KEY'),
#             api_secret=os.environ.get('CLOUDINARY_API_SECRET'),
#             secure=True
#         )
#
#     correct_tags = await images_service_normalize_tags(body)
#
#     public_name = file.filename.split(".")[0]
#
#     correct_public_name = await images_service_change_name(public_name, db)
#
#     file_name = correct_public_name + "_" + str(current_user.username)
#     r = cloudinary.uploader.upload(file.file, public_id=f'PhotoShare/{file_name}', overwrite=True)
#     src_url = cloudinary.CloudinaryImage(f'PhotoShare/{file_name}') \
#         .build_url(width=250, height=250, crop='fill', version=r.get('version'))
#
#     image, details = await images.add_image(db, body, correct_tags, src_url, correct_public_name, current_user)
#
#     return {"image": image, "detail": "Image was successfully added." + details}

#
# @router.put("/update_description/{image_id}", response_model=ImageUpdateDescrResponse,
#             dependencies=[Depends(access_all)])
# async def update_description(image_id: int, image_info: ImageUpdateModel, db: Session = Depends(get_db),
#                              current_user: User = Depends(auth_service.get_current_user)):
#     """
#     The update_description function updates the description of an image.
#         The function takes in a database session, current_user and image_id as parameters.
#         It then uses the update_image function from images to update the description of an image with that id.
#
#     :param image_id: int: Identify the image that is being updated
#     :param image_info: ImageUpdateModel: Get the new description for the image
#     :param db: Session: Access the database
#     :param current_user: User: Get the current user who is logged in
#     :return: A dictionary with the id, description and detail of the image that was updated
#     """
#
#     user_image = await images.update_image(db, image_id, image_info, current_user)
#     return {"id": user_image.id, "description": user_image.description, "detail": "Image was successfully updated"}
#
#
# @router.put("/update_tags/{image_id}", response_model=ImageAddTagResponse, dependencies=[Depends(access_all)])
# async def add_tag(image_id, body: ImageAddTagModel = Depends(), db: Session = Depends(get_db),
#                   current_user: User = Depends(auth_service.get_current_user)):
#     """
#     The add_tag function adds a tag to an image.
#         The function takes in the following parameters:
#             - image_id: The id of the image that is being tagged.
#             - body: A JSON object containing the tag name and description.  This is validated by ImageAddTagModel().
#
#     :param image_id: Identify the image to be updated
#     :param body: ImageAddTagModel: Get the tag from the request body
#     :param db: Session: Get the database session
#     :param current_user: User: Get the current user from the database
#     :return: A dictionary with the image id, tags and a detail message
#     """
#
#     image, details = await images.add_tag(db, image_id, body, current_user)
#     return {"id": image.id, "tags": image.tags, "detail": "Image was successfully updated." + details}
#
#
# @router.delete("/{id}", response_model=ImageDeleteResponse, dependencies=[Depends(access_all)])
# async def delete_image(id: int, db: Session = Depends(get_db),
#                        current_user: User = Depends(auth_service.get_current_user)):
#     """
#     The delete_image function deletes an image from the database.
#         The function takes in a user_id and an image_id, and returns a dictionary with the deleted image's information.
#
#     :param id: int: Specify the id of the image to be deleted
#     :param db: Session: Pass the database session to the function
#     :param current_user: User: Get the current user from the database
#     :return: A dictionary with the image and a message saying it was deleted
#     """
#
#     user_image = await images.delete_image(db, id, current_user)
#     return {"image": user_image, "detail": "Image was successfully deleted"}
