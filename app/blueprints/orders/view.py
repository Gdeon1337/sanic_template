from sanic import Blueprint
from sanic.request import Request
from sanic.response import json
from database import Point, User, Order, OrderUsers, StatusPoint
from sanic_jwt.decorators import inject_user, protected
from app.helpers.validators import raise_if_empty, raise_if_not_float

blueprint = Blueprint('orders', url_prefix='/orders', strict_slashes=True)


@blueprint.post('')
async def create(request: Request):
    year = request.json.get('year')
    mstet = request.json.get('mstet')
    ltc = request.json.get('ltc')
    place = request.json.get('place')
    address = request.json.get('address')
    client = request.json.get('client')
    project_price_predict = request.json.get('project_price_predict')
    comment = request.json.get('comment')
    google_doc_link = request.json.get('google_doc_link')

    latitude = request.json.get('latitude')
    longitude = request.json.get('longitude')
    raise_if_empty(year, mstet, ltc, place, address, client)
    order = await Order.create(
        year=year,
        mstet=mstet,
        ltc=ltc,
        google_doc_link=google_doc_link,
        place=place,
        address=address,
        client=client,
        project_price_predict=project_price_predict,
        comment=comment,
        latitude=latitude,
        longitude=longitude
    )
    order = await load_json(order)
    return json(order)


@blueprint.delete('')
async def delete(request: Request):
    order_id = request.json.get('order_id')
    raise_if_empty(order_id)
    order = await Order.query.where(Order.id == order_id).gino.first_or_404()
    await order.delete()
    return json({'status': 'ok'})


@blueprint.get('')
async def get(request: Request):
    order_id = request.args.get('order_id')
    if order_id:
        order = await Order.query.where(Order.id == order_id).gino.first_or_404()
        return json(load_json(order))
    orders = await Order.query.where(Order.activate.is_(True)).gino.all()
    orders = [await load_json(order) for order in orders]
    return json(orders)


@blueprint.get('/in-activate')
async def get_in(request: Request):
    orders = await Order.query.where(Order.user_id == user.id).where(Order.activate.is_(False)).gino.all()
    orders = [await load_json(order) for order in orders]
    return json(orders)


@blueprint.put('')
async def update(request: Request):
    year = request.json.get('year')
    mstet = request.json.get('mstet')
    ltc = request.json.get('ltc')
    place = request.json.get('place')
    address = request.json.get('address')
    client = request.json.get('client')
    project_price_predict = request.json.get('project_price_predict')
    comment = request.json.get('comment')
    google_doc_link = request.json.get('google_doc_link')
    order_id = request.json.get('order_id')
    raise_if_empty(order_id)
    order = await Order.query.where(Order.id == order_id).gino.first_or_404()
    if year:
        order = order.update(year=year)
    if mstet:
        order = order.update(mstet=mstet)
    if ltc:
        order = order.update(ltc=ltc)
    if address:
        order = order.update(address=address)
    if place:
        order = order.update(place=place)
    if project_price_predict:
        order = order.update(project_price_predict=project_price_predict)
    if client:
        order = order.update(client=client)
    if google_doc_link:
        order = order.update(google_doc_link=google_doc_link)
    if comment:
        order = order.update(comment=comment)
    await order.apply()
    order = await load_json(order)
    return json(order)


@blueprint.post('/activate')
async def create_point(request: Request):
    order_user_id = request.json.get('order_user_id')
    order_id = request.json.get('order_id')
    raise_if_empty(order_id, order_user_id)
    order = await Order.query.where(Order.id == order_id).gino.first_or_404()
    order_user = await OrderUsers.query.where(OrderUsers.id == order_user_id).gino.first_or_404()
    await order.update(activate=False).apply()
    point = await Point.create(
        year=order.year,
        mstet=order.mstet,
        ltc=order.ltc,
        google_doc_link=order.google_doc_link,
        place=order.place,
        address=order.address,
        client=order.client,
        project_price_predict=order_user.auction_price,
        comment=order.comment,
        latitude=order.latitude,
        longitude=order.longitude,
        user_id=order_user.user_id,
        failure=False,
        status=StatusPoint.IN_WORK
    )
    order = await load_json(order)
    return json(order)


async def load_json(point):
    u = OrderUsers.join(User).select()
    users = await u.where(OrderUsers.order_id == point.id)\
        .gino.load(OrderUsers.load(login=User.login)).all()
    return {
        'info': {
            'id': str(point.id),
            'year': point.year,
            'mstet': point.mstet,
            'ltc': point.ltc,
            'place': point.place,
            'address': point.address,
            'client': point.client,
            'project_price_predict': point.project_price_predict,
            'user_id': point.user_id,
            'coordinates': {
                'latitude': point.latitude,
                'longitude': point.longitude
            },
            'users': [user.to_dict() for user in users]
        }
    }
