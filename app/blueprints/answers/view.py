import datetime
import json as js
from sanic import Blueprint
from sanic.request import Request
from sanic.response import json
from app.extensions import conn


blueprint = Blueprint('answers', url_prefix='/answers', strict_slashes=True)


@blueprint.post('/')
async def domain(request: Request):
    await conn.del_key('ap')
    await conn.set('ap', js.dumps(request.json.get('data')))
    return json({'status': 'ok'})


@blueprint.get('/')
async def get_currency(request: Request):
    resp = await conn.get('ap')
    return json(
        {
            'answers': js.load(resp),
            'status': 'ok'
        }
    )