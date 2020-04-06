from sanic import Blueprint
from sanic.request import Request
from sanic.response import json
from database import Point
from app.helpers.executors import gather
from sanic_jwt.decorators import inject_user, protected
from app.helpers.validators import raise_if_empty

blueprint = Blueprint('answers', url_prefix='/answers', strict_slashes=True)


@blueprint.get('')
async def answer(request: Request):
    points = await Point.query.where(Point.brigadier != '').where(Point.failure.is_(False)).gino.all()
    points = await gather(load_json, points)
    return json(points)


@blueprint.get('/new-answers')
async def new_answer(request: Request):
    points = await Point.query.where(Point.brigadier == None).where(Point.failure.is_(False)).gino.all()
    points = await gather(load_json, points)
    return json(points)


@blueprint.post('/user-point')
@protected()
@inject_user()
async def create_user_point(request: Request, user):
    point_id = request.json.get('point_id')
    raise_if_empty(point_id)
    point = await Point.query.where(Point.id == point_id).gino.first_or_404()
    point = point.update(brigadier=user.login)
    await point.update(user_id=user.id).apply()
    return json({'status': 'ok'})


@blueprint.get('/user-point')
@protected()
@inject_user()
async def get_user_point(request: Request, user):
    points = await Point.query.where(Point.user_id == user.id).gino.all()
    points = await gather(load_json, points)   
    return json(points)


@blueprint.post('')
async def create_answer(request: Request):
    point = request.json.get('data')
    await create_points(point)
    return json({'status': 'ok'})


async def create_points(points):
    from datetime import datetime
    for point in points:
        _point = await Point.query.where(Point.year == point.get('year')).where(Point.id_dot == point.get('id_dot'))\
            .gino.first()
        if _point:
            continue
        await Point.create(
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
