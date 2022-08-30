import server
import pytest

class TestShowCompetions:

    def test_booking_competions_in_past(self, mocker, client, clubs, competitions):
        mocker.patch.object(server, 'competitions', [competitions[1]])
        mocker.patch.object(server, 'clubs', clubs)
        data = {'email': clubs[0]['email']}
        response = client.post('/showSummary', data=data, follow_redirects=True)
        res_data = response.data.decode('utf-8')
        assert 'Book Places' not in res_data
        assert response.status_code == 200

    def test_booking_competions_in_future(self, mocker, client, clubs, competitions):
        mocker.patch.object(server, 'competitions', [competitions[0]])
        mocker.patch.object(server, 'clubs', clubs)
        data = {'email': clubs[0]['email']}
        response = client.post('/showSummary', data=data, follow_redirects=True)
        res_data = response.data.decode('utf-8')
        assert 'Book Places' in res_data
        assert response.status_code == 200