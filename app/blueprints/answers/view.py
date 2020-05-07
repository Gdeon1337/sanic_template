from base64 import b64encode

from sanic import Blueprint
from sanic.request import Request
from sanic.response import json
from database import Point, User, Order, OrderUsers, StatusPoint
from app.helpers.executors import gather
from sanic_jwt.decorators import inject_user, protected
from app.helpers.validators import raise_if_empty, raise_if_not_float

blueprint = Blueprint('answers', url_prefix='/answers', strict_slashes=True)


@blueprint.get('')
async def answer(request: Request):
    points = await Point.query.where(Point.brigadier != '').where(Point.failure.is_(False)).gino.all()
    points = await gather(load_json, points)
    return json(points)


@blueprint.get('/point')
#@protected()
async def get_point(request: Request):
    point_id = request.args.get('point_id')
    raise_if_empty(point_id)
    point = await Point.query.where(Point.id == point_id).gino.first_or_404()
    point = await load_json(point)
    return json(point)


@blueprint.put('/point')
async def update_point(request: Request):
    from datetime import datetime
    point_id = request.args.get('point_id')
    raise_if_empty(point_id)
    point = await Point.query.where(Point.id == point_id).gino.first_or_404()
    year = request.json.get('year')
    mstet = request.json.get('mstet')
    ltc = request.json.get('ltc')
    place = request.json.get('place')
    address = request.json.get('address')
    client = request.json.get('client')
    project_price_predict = request.json.get('project_price_predict')
    comment = request.json.get('comment')
    latitude = request.json.get('latitude')
    longitude = request.json.get('longitude')
    failure = request.json.get('failure')
    date_failure = request.json.get('date_failure')
    application_source = request.json.get('application_source')
    hermes_number = request.json.get('hermes_number')
    hermes_deadline = datetime.strptime(request.json.get('hermes_deadline'), "%Y-%m-%d %H:%M:%S") if request.json.get(
        'hermes_deadline') else None
    hermes_smr_successful = request.json.get('hermes_smr_successful')
    brigadier = request.json.get('brigadier')
    project_engineer = request.json.get('project_engineer')
    smr = request.json.get('smr')
    svarka = request.json.get('svarka')
    subcontracting_price = request.json.get('subcontracting_price')
    material_price = request.json.get('material_price')
    ks11_signed_by_ltc = request.json.get('ks11_signed_by_ltc')
    project_price_ks2 = request.json.get('project_price_ks2')
    date_ks2 = datetime.strptime(request.json.get('date_ks2'), "%Y-%m-%d %H:%M:%S") if request.json.get('date_ks2') else None
    google_doc_link = request.json.get('google_doc_link')
    if year:
        point = point.update(year=year)
    if mstet:
        point = point.update(mstet=mstet)
    if ltc:
        point = point.update(ltc=ltc)
    if place:
        point = point.update(place=place)
    if address:
        point = point.update(address=address)
    if client:
        point = point.update(client=client)
    if project_price_predict:
        point = point.update(project_price_predict=project_price_predict)
    if comment:
        point = point.update(comment=comment)
    if latitude:
        point = point.update(latitude=latitude)
    if longitude:
        point = point.update(longitude=longitude)
    if failure:
        point = point.update(failure=failure)
    if date_failure:
        point = point.update(date_failure=date_failure)
    if application_source:
        point = point.update(application_source=application_source)
    if hermes_number:
        point = point.update(hermes_number=hermes_number)
    if hermes_deadline:
        point = point.update(hermes_deadline=hermes_deadline)
    if hermes_smr_successful:
        point = point.update(hermes_smr_successful=hermes_smr_successful)
    if brigadier:
        point = point.update(brigadier=brigadier)
    if project_engineer:
        point = point.update(project_engineer=project_engineer)
    if smr:
        point = point.update(smr=smr)
    if svarka:
        point = point.update(svarka=svarka)
    if subcontracting_price:
        point = point.update(subcontracting_price=subcontracting_price)
    if material_price:
        point = point.update(material_price=material_price)
    if ks11_signed_by_ltc:
        point = point.update(ks11_signed_by_ltc=ks11_signed_by_ltc)
    if project_price_ks2:
        point = point.update(project_price_ks2=project_price_ks2)
    if date_ks2:
        point = point.update(date_ks2=date_ks2)
    if google_doc_link:
        point = point.update(google_doc_link=google_doc_link)
    await point.apply()
    point = await load_json(point)
    return json(point)


@blueprint.get('/new-answers')
@protected()
@inject_user()
async def new_answer(request: Request, user):
    points_user = await OrderUsers.query.where(OrderUsers.user_id == user.id).gino.all()
    points = await Order.query.where(Order.activate.is_(True))\
        .gino.all()
    points_js = []
    for point in points:
        order_user = [order for order in points_user if order.order_id == point.id]
        if not order_user:
            points_js.append(point)
    points = await gather(load_json_order, points_js)
    return json(points)


@blueprint.post('/user-point')
@protected()
@inject_user()
async def create_user_point(request: Request, user):
    point_id = request.json.get('point_id')
    auction_price = request.json.get('auction_price')
    google_disk_link = request.json.get('google_disk_link')
    file = request.files.get('data')
    raise_if_empty(point_id)
    point = await Order.query.where(Order.id == point_id).gino.first_or_404()
    order_user = await OrderUsers.create(
        user_id=user.id,
        order_id=point.id,
        auction_price=float(auction_price) if auction_price else None,
        google_disk_link=google_disk_link,
        file_name=file.name if file else None,
        file_type=file.type if file else None,
        file_data=file.body if file else None
    )
    return json({'status': 'ok', 'order_user_id': str(order_user.id)})


@blueprint.post('/file')
@protected()
async def create_user_point(request: Request):
    #import pdb; pdb.set_trace()
    order_user_id = request.args.get('order_user_id')
    file = request.files.get('data')
    raise_if_empty(order_user_id)
    order_user = await OrderUsers.query.where(OrderUsers.id == order_user_id).gino.first_or_404()
    await order_user.update(
        file_name=file.name if file else None,
        file_type=file.type if file else None,
        file_data=file.body if file else None
    ).apply()
    return json({'status': 'ok'})


@blueprint.delete('/user-point')
async def delete_user_point(request: Request):
    point_id = request.json.get('point_id')
    raise_if_empty(point_id)
    point = await Point.query.where(Point.id == point_id).gino.first_or_404()
    point = point.update(brigadier=None)
    await point.update(user_id=None).apply()
    return json({'status': 'ok'})


@blueprint.get('/user-point')
@protected()
@inject_user()
async def get_user_point(request: Request, user):
    points = await Point.query.where(Point.user_id == user.id).gino.all()
    points = await gather(load_json, points)
    return json(points)


@blueprint.get('/new-orders')
async def new_orders(request: Request):
    users = await User.query.gino.all()
    json_users = []
    for user in users:
        points = await Point.query.where(Point.user_id == user.id).gino.all()
        points = await gather(load_json, points)
        json_users.append({
            'user_name': user.name,
            'user': user.login,
            'user_id': str(user.id),
            'orders': points
        })
    return json(json_users)


@blueprint.post('')
async def create_answer(request: Request):
    point = request.json.get('data')
    await create_points(point)
    return json({'status': 'ok'})


@blueprint.post('/registration')
async def create_answer(request: Request):
    login = request.json.get('data')
    password = request.json.get('password')
    raise_if_empty(login, password)
    argon2 = request.app.argon2
    rehashed_password = await argon2.async_hash(password)
    user = User.query.where(User.login == login).gino.first()
    if user:
        return json({'status': 'Такой пользователь уже есть'})
    await User.create(login=login, password=rehashed_password)
    return json({'status': 'ok'})


async def create_points(points):
    from datetime import datetime
    for point in points:
        _point = await Point.query.where(Point.year == point.get('year')).where(Point.id_dot == str(point.get('id_dot')))\
            .gino.first()
        if _point:
            continue
        await Point.create(
            status=StatusPoint.IN_WORK,
            id_dot=str(point.get('id_dot')),
            year=point.get('year'),
            mstet=point.get('mstet'),
            ltc=point.get('ltc'),
            place=point.get('place'),
            address=point.get('address'),
            client=point.get('client'),
            project_price_predict=point.get('project_price_predict'),
            comment=point.get('comment'),
            latitude=point.get('latitude'),
            longitude=point.get('longitude'),
            failure=point.get('failure'),
            date_failure=point.get('date_failure'),
            application_source=point.get('application_source'),
            hermes_number=point.get('hermes_number'),
            hermes_deadline=datetime.strptime(point.get('hermes_deadline'), "%Y-%m-%d %H:%M:%S") if point.get('hermes_deadline') else None,
            hermes_smr_successful=point.get('hermes_smr_successful'),
            brigadier=point.get('brigadier'),
            project_engineer=point.get('project_engineer'),
            smr=point.get('smr'),
            svarka=point.get('svarka'),
            subcontracting_price=point.get('subcontracting_price'),
            material_price=point.get('material_price'),
            ks11_signed_by_ltc=point.get('ks11_signed_by_ltc'),
            project_price_ks2=point.get('project_price_ks2'),
            date_ks2=datetime.strptime(point.get('date_ks2'), "%Y-%m-%d %H:%M:%S") if point.get('date_ks2') else None,
            google_doc_link=point.get('google_doc_link')
        )


async def load_json(point: Point):
    return {
        'info': {
            'failure': {
                'status': point.failure,
                'date': point.date_failure
            },
            'id': str(point.id),
            'year': point.year,
            'mstet': point.mstet,
            'ltc': point.ltc,
            'place': point.place,
            'address': point.address,
            'client': point.client,
            'project_price_predict': point.project_price_predict,
            'google_disk_link': point.google_disk_link,
            'coordinates': {
                'latitude': point.latitude,
                'longitude': point.longitude
            }
        },
        'application': {
            'application_source': point.application_source,
            'hermes': {
                'hermes_number': point.hermes_number,
                'hermes_deadline': point.hermes_deadline.isoformat() if point.hermes_deadline else None,
                'hermes_smr_successful': point.hermes_smr_successful
            },
        },
        'worker': {
            'brigadier': point.brigadier,
            'project_engineer': point.project_engineer
        },
        'documents': {
            'smr': point.smr,
            'svarka': point.svarka,
            'subcontracting_price': point.subcontracting_price,
            'material_price': point.material_price,
            'ks11_signed_by_ltc': point.ks11_signed_by_ltc,
            'project_price_ks2': point.project_price_ks2,
            'date_ks2': point.date_ks2.isoformat() if point.date_ks2 else None,
            'google_doc_link': point.google_doc_link
        }
    }


async def load_json_order(point):
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
            'file_type': point.file_type,
            'file_name': point.file_name,
            'file_data': b64encode(point.file_data) if point.file_data else None
        },
        'application': {
            'application_source': None,
            'hermes': {
                'hermes_number': None,
                'hermes_deadline': None,
                'hermes_smr_successful': None
            }
        },
        'worker': {
            'brigadier': None,
            'project_engineer': None
        },
        'documents': {
            'smr': False,
            'svarka': False,
            'subcontracting_price': None,
            'material_price': None,
            'ks11_signed_by_ltc': None,
            'project_price_ks2': None,
            'date_ks2': None,
            'google_doc_link': point.google_doc_link
        }
    }

