# from sanic import Blueprint
# from sanic.request import Request
# from sanic.response import json
# from database import File, User, Order, OrderUsers, StatusPoint
# from app.helpers.executors import gather
# from sanic_jwt.decorators import inject_user, protected
# from app.helpers.validators import raise_if_empty, raise_if_not_float
#
#
# blueprint = Blueprint('files', url_prefix='/files', strict_slashes=True)
#
#
# @blueprint.get('')
# async def files(request: Request):
#     points = await File.query.where(Point.brigadier != '').where(Point.failure.is_(False)).gino.all()
#     points = await gather(load_json, points)
#     return json(points)
#
#
# @blueprint.get('/point')
# #@protected()
# async def get_point(request: Request):
#     point_id = request.args.get('point_id')
#     raise_if_empty(point_id)
#     point = await Point.query.where(Point.id == point_id).gino.first_or_404()
#     point = await load_json(point)
#     return json(point)