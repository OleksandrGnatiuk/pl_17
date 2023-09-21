from datetime import datetime

from fastapi import HTTPException, status
from sqlalchemy.orm import Session

from src.database.models import Service, User, Tag, Comment, Role
from src.repository.ratings import get_average_rating
from src.schemas.service_schemas import ServiceUpdateModel, ServiceAddModel, ServiceAddTagModel
from src.services.images import service_normalize_tags


async def get_services(db: Session, user: User):
    services = db.query(Service).order_by(Service.id).all()

    user_response = []
    for service in services:
        ratings = await get_average_rating(service.id, db)
        comments = db.query(Comment).filter(Comment.service_id == service.id, Comment.user_id == user.id).all()
        user_response.append({"service": service, "ratings": ratings, "comments": comments})
    return user_response


async def get_service(db: Session, id: int, user: User):

    # if user.role == Role.admin:
    #     service = db.query(Service).filter(Service.id == id).first()
    # else:
    service = db.query(Service).filter(Service.id == id).first()

    if service:
        ratings = await get_average_rating(service.id, db)
        comments = db.query(Comment).filter(Comment.service_id == service.id, Comment.user_id == user.id).all()
        return service, ratings, comments
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Service not found")


async def admin_get_service(db: Session, user_id: id):

    services = db.query(Service).filter(Service.user_id == user_id).order_by(Service.id).all()
    if services:
        user_response = []
        for service in services:
            ratings = await get_average_rating(service.id, db)
            comments = db.query(Comment).filter(Comment.service_id == service.id, Comment.user_id == service.user_id).all()
            user_response.append({"service": service, "ratings": ratings, "comments": comments})
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Service not found")
    return user_response


async def add_service(db: Session, service: ServiceAddModel, tags: list[str], url: str, public_name: str, user: User):

    if not user:
        return None

    detail = ""
    num_tags = 0
    service_tags = []
    for tag in tags:
        if len(tag) > 25:
            tag = tag[0:25]
        if not db.query(Tag).filter(Tag.name == tag.lower()).first():
            db_tag = Tag(name=tag.lower())
            db.add(db_tag)
            db.commit()
            db.refresh(db_tag)
        if num_tags < 5:
            service_tags.append(tag.lower())
        num_tags += 1

    if num_tags >= 5:
        detail = " But be attentive you can add only five tags to an image"

    tags = db.query(Tag).filter(Tag.name.in_(service_tags)).all()
    # Save service in the database
    db_service = Service(description=service.description, tags=tags, url=url, user_id=user.id)
    db.add(db_service)
    db.commit()
    db.refresh(db_service)
    return db_service, detail


async def update_service(db: Session, service_id, service: ServiceUpdateModel, user: User):

    if user.role == Role.admin:
        db_service = db.query(Service).filter(Service.id == service_id).first()
    else:
        db_service = db.query(Service).filter(Service.id == service_id, Service.user_id == user.id).first()

    if db_service:
        db_service.description = service.description
        db.commit()
        db.refresh(db_service)
        return db_service
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Service not found")


async def add_tag(db: Session, service_id, body: ServiceAddTagModel, user: User):

    tags = await service_normalize_tags(body)

    detail = ""
    num_tags = 0
    service_tags = []
    for tag in tags:
        if tag:
            if len(tag) > 25:
                tag = tag[0:25]
            if not db.query(Tag).filter(Tag.name == tag.lower()).first():
                db_tag = Tag(name=tag.lower())
                db.add(db_tag)
                db.commit()
                db.refresh(db_tag)
            if num_tags < 5:
                service_tags.append(tag.lower())
            num_tags += 1

    if num_tags >= 5:
        detail = "But be attentive you can add only five tags to an service"

    tags = db.query(Tag).filter(Tag.name.in_(service_tags)).all()

    if user.role == Role.admin:
        service = db.query(Service).filter(Service.id == service_id).first()
    else:
        service = db.query(Service).filter(Service.id == service_id, Service.user_id == user.id).first()

    if service:
        service.updated_at = datetime.utcnow()
        service.tags = tags
        db.commit()
        db.refresh(service)
        return service, detail
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Service not found")


async def delete_service(db: Session, id: int, user: User):
    if user.role == Role.admin:
        db_service = db.query(Service).filter(Service.id == id).first()
    else:
        db_service = db.query(Service).filter(Service.id == id, Service.user_id == user.id).first()

    if db_service:
        db.delete(db_service)
        db.commit()
        return db_service
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Service not found")
