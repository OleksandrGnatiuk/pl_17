# import redis.asyncio as redis
import uvicorn
from fastapi import FastAPI
from sqladmin import Admin, ModelView
# from fastapi_limiter import FastAPILimiter
# from src.conf.config import settings
from src.database.db import engine
from src.database.models import Service, Tag, Comment, Rating, Client, Master, Administrator
from src.routes import auth, tags, comments_routes, ratings, users, services


# Стоврюємо екземпляр FastApi, встановлюємо назву додатка в swagger та відсоруємо роути по методам:
app = FastAPI(swagger_ui_parameters={"operationsSorter": "method"}, title='Platforma17 app')

# створюємо адмінку
admin = Admin(app, engine)


# визначаємо зміст адмінки: якими моделями бази даних і якими полями хочемо керувати через адмінку:
class ClientAdmin(ModelView, model=Client):
    column_list = [Client.id, Client.username, Client.email]
    column_searchable_list = [Client.username]
    column_sortable_list = [Client.id]
    column_default_sort = [(Client.email, True), (Client.username, False)]
    can_create = True
    can_edit = True
    can_delete = False
    can_view_details = True
    can_export = True
    icon = "fa-solid fa-user"


class MasterAdmin(ModelView, model=Master):
    column_list = [Master.id, Master.username, Master.email]
    column_searchable_list = [Master.username]
    column_sortable_list = [Master.id]
    column_default_sort = [(Master.email, True), (Master.username, False)]
    can_create = True
    can_edit = True
    can_delete = False
    can_view_details = True
    can_export = True
    icon = "fa-solid fa-user-gear"


class ServiceAdmin(ModelView, model=Service):
    column_list = "__all__"
    can_create = True
    can_edit = True
    can_delete = False
    can_view_details = True
    can_export = True
    icon = "fa-solid fa-scissors"


class TagAdmin(ModelView, model=Tag):
    column_list = "__all__"
    can_create = True
    can_edit = True
    can_delete = False
    can_view_details = True
    can_export = True
    icon = "fa-solid fa-tag"


class CommentAdmin(ModelView, model=Comment):
    column_list = "__all__"
    can_create = True
    can_edit = True
    can_delete = False
    can_view_details = True
    can_export = True
    icon = "fa-regular fa-comment"


class RatingAdmin(ModelView, model=Rating):
    column_list = "__all__"
    can_create = True
    can_edit = True
    can_delete = False
    can_view_details = True
    can_export = True
    icon = "fa-regular fa-star-half-stroke"


class AdministratorAdmin(ModelView, model=Administrator):
    column_list = [Administrator.id, Administrator.username, Administrator.email]
    column_searchable_list = [Administrator.username]
    column_sortable_list = [Administrator.id]
    column_default_sort = [(Administrator.email, True), (Administrator.username, False)]
    can_create = True
    can_edit = True
    can_delete = False
    can_view_details = True
    can_export = True
    icon = "fa-solid fa-person-military-pointing"


admin.add_view(MasterAdmin)
admin.add_view(ClientAdmin)
admin.add_view(ServiceAdmin)
admin.add_view(TagAdmin)
admin.add_view(CommentAdmin)
admin.add_view(RatingAdmin)
admin.add_view(AdministratorAdmin)

@app.get("/")
def root():
    return {"message": "Welcome to FastAPI!"}


# @app.on_event("startup")
# async def startup():
#     r = await redis.Redis(host=settings.redis_host, port=settings.redis_port, password=settings.redis_password, encoding="utf-8", db=0)
#     await FastAPILimiter.init(r)

app.include_router(auth.router, prefix='/api')
app.include_router(users.router, prefix='/api')
app.include_router(services.router, prefix='/api')
app.include_router(comments_routes.router, prefix='/api')
app.include_router(tags.router, prefix='/api')
app.include_router(ratings.router, prefix='/api')


if __name__ == '__main__':
    uvicorn.run('main:app', reload=True)
