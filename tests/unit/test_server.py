import server
import pytest

class TestLogin:

    def test_login_should_200(self, mocker, client, clubs):
        mocker.patch.object(server, 'clubs', clubs)
        data = {'email': clubs[0]['email']}
        response = client.post('/showSummary', data=data, follow_redirects=True)
        assert response.status_code == 200

    @pytest.mark.parametrize(
        'email',
        [
           ({'email': 'unlisted@test.com'}),
           ({'other': ''}),
           ({'': ''}),
           ()
        ])
    def test_login_should_mail_error(self, client, email):
        response = client.post('/showSummary', data=email, follow_redirects=True)
        assert response.status_code == 200
        

class TestPurchasePlaces:

    def test_points_deducted_at_purchase(self, mocker, captured_templates, client, clubs, competitions):
        mocker.patch.object(server, 'clubs', clubs)
        mocker.patch.object(server, 'competitions', competitions)
    
    @pytest.mark.parametrize(
        'places',
        [
            (3),
            (10),
            (100),
            (-10)
        ]
    )
    def test_purchase_available(self, mocker, captured_templates, client, clubs, competitions, places):
        # datas mocked
        points_per_place = 1         
        mocker.patch.object(server, 'clubs', clubs)
        mocker.patch.object(server, 'competitions', competitions)
        mocker.patch.object(server, 'points_per_place', points_per_place)
        club = clubs[0]
        club_points_after = club['points']
        competition = competitions[0]
        number_of_places_after = competition['numberOfPlaces']
        data = {
            'competition': competition['name'],
            'club': club['name'],
            'places': int(club['points'])-1
        }

        # request client and data capture returned
        response = client.post('/purchasePlaces', data=data, follow_redirects=True)
        res_data = response.data.decode('utf-8')
        assert len(captured_templates) == 1
        template, context = captured_templates[0]

        # assertion check
        assert template.name == 'welcome.html'
        assert int(context['club']['points']) == int(club_points_after) - int(data['places'])
        assert int(context['competitions'][0]['numberOfPlaces']) == int(number_of_places_after) - int(data['places'])
        assert 'Great-booking complete!' in res_data
        assert response.status_code == 200

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
