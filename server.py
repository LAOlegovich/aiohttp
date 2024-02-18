import json

import bcrypt
from aiohttp import web
from sqlalchemy.exc import IntegrityError

from models import Session, User, Sticker, engine, init_db


def hash_password(password: str):
    password = password.encode()
    password = bcrypt.hashpw(password, bcrypt.gensalt())
    password = password.decode()
    return password


def check_password(password: str, hashed_password: str):
    password = password.encode()
    hashed_password = hashed_password.encode()
    return bcrypt.checkpw(password, hashed_password)


app = web.Application()


@web.middleware
async def session_middleware(request: web.Request, handler):
    async with Session() as session:
        request.session = session
        response = await handler(request)
        return response


async def init_orm(app: web.Application):
    print("START")
    await init_db()
    yield
    await engine.dispose()
    print("FINISH")


app.cleanup_ctx.append(init_orm)
app.middlewares.append(session_middleware)


def get_http_error(error_class, message):
    error = error_class(
        body=json.dumps({"error": message}), content_type="application/json"
    )
    return error


async def get_instance_by_id(session: Session, instance_id: int, instance_class):
    instance = await session.get(instance_class, instance_id)
    if instance is None:
        raise get_http_error(web.HTTPNotFound, f"{instance_class} with id {instance_id} not found")
    return instance


async def add_instance(session: Session, instance):
    try:
        session.add(instance)
        await session.commit()
    except IntegrityError as error:
        raise get_http_error(web.HTTPConflict, f"{instance} already exists")
    return instance

class UserView(web.View):
    @property
    def user_id(self):
        return int(self.request.match_info["user_id"])

    @property
    def session(self):
        return self.request.session

    async def get_current_user(self):
        return await get_instance_by_id(self.session, self.user_id, User)

    async def get(self):
        user = await self.get_current_user()
        return web.json_response(user.dict)

    async def post(self):
        json_data = await self.request.json()
        json_data["password"] = hash_password(json_data["password"])
        user = User(**json_data)
        user = await add_instance(self.session, user)
        return web.json_response({"id": user.id})

    async def patch(self):
        json_data = await self.request.json()
        user = await self.get_current_user()
        if "password" in json_data:
            json_data["password"] = hash_password(json_data["password"])
        for field, value in json_data.items():
            setattr(user, field, value)
        user = await add_instance(self.session, user)
        return web.json_response(user.dict)

    async def delete(self):
        user = await self.get_current_user()
        await self.session.delete(user)
        await self.session.commit()
        return web.json_response({"status": "deleted"})



class StickerView(web.View):
    @property
    def sticker_id(self):
        return int(self.request.match_info["sticker_id"])

    @property
    def session(self) -> Session:
        return self.request.session

    async def get_current_sticker(self):
        return await get_instance_by_id(self.session, self.sticker_id, Sticker)

    async def get(self):
        sticker = await self.get_current_sticker()
        return web.json_response(sticker.dict)

    async def post(self):
        json_data = await self.request.json()
        sticker = Sticker(**json_data)
        sticker = await add_instance(self.session, sticker)
        return web.json_response({"id": sticker.id})

    async def patch(self):
        json_data = await self.request.json()
        sticker = await self.get_current_sticker()
        for field, value in json_data.items():
            setattr(sticker, field, value)
        sticker = await add_instance(self.session, sticker)
        return web.json_response(sticker.dict)

    async def delete(self):
        sticker = await self.get_current_sticker()
        await self.session.delete(sticker)
        await self.session.commit()
        return web.json_response({"status": "deleted"})

app.add_routes(
    [
        web.post("/user", UserView),
        web.get(r'/user/{user_id:\d+}', UserView),
        web.patch(r"/user/{user_id:\d+}", UserView),
        web.delete(r"/user/{user_id:\d+}", UserView),
        web.post("/sticker", StickerView),
        web.get(r"/sticker/{sticker_id:\d+}", StickerView),
        web.patch(r"/sticker/{sticker_id:\d+}", StickerView),
        web.delete(r"/sticker/{sticker_id:\d+}", StickerView),
    ]
)


web.run_app(app)
