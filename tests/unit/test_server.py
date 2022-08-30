import server
import pytest

class TestPurchasePlaces:

    def test_purchase_more_max_places(self, mocker, client, clubs, competitions):
        max_places = 8
        mocker.patch.object(server, 'clubs', clubs)
        mocker.patch.object(server, 'competitions', competitions)
        mocker.patch.object(server, 'MAX_PLACES', max_places)
        club = clubs[0]
        competition = competitions[0]
        data = {
            'competition': competition['name'],
            'club': club['name'],
            'places': max_places + 1
        }
        response = client.post('/purchasePlaces', data=data, follow_redirects=True)
        res_data = response.data.decode('utf-8')
        assert f'Maximum number of places at reservation {max_places}!' in res_data
        assert response.status_code == 200