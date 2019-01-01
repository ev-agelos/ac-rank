import json

from laptimes.models import Laptime


def test_adding_laptime_with_unknown_car(client, user):
    api_auth = client.post('/new.json', dict(username=user.username,
                                             password=user.password))
    token = api_auth.json()['token']
    data = dict(car='foo', track='bar', splits=['1', '2', '3'])
    response = client.post(
        '/api/laptimes/add?user=1&token={}'.format(token),
        json.dumps(data),
        content_type='application/json'
    )
    assert Laptime.objects.get(pk=response.json()['laptime_id'])
