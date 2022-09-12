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

    @pytest.mark.parametrize(
        'places',
        [
            (3),
            (10),
            (11),
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
            'places': places
        }

        # request client and data capture returned
        response = client.post('/purchasePlaces', data=data, follow_redirects=True)
        res_data = response.data.decode('utf-8')
        assert len(captured_templates) == 1
        template, context = captured_templates[0]
        
        # assertion check
        assert template.name == 'welcome.html'
        if data['places'] * points_per_place > int(club_points_after) or data['places'] > int(number_of_places_after) or data['places'] < 0:
            # Number of places is invalid
            assert int(context['club']['points']) == int(club_points_after)
            assert int(context['competitions'][0]['numberOfPlaces']) == int(number_of_places_after)
            if data['places'] * points_per_place > int(club_points_after):
                assert 'Insufficient points!' in res_data
            elif data['places'] > int(number_of_places_after):
                assert 'Number of places not available!' in res_data
            else:
                assert 'Invalid number of places!' in res_data
        else:
            # Points and places available
            assert int(context['club']['points']) == int(club_points_after) - int(data['places']) * int(points_per_place)
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

    @pytest.mark.parametrize(
        'competitions_param',
        (
            ([{
                "name": "Test competition",
                "date": "2023-12-10 08:55:23",
                "numberOfPlaces": "20"
            }]),
            ([{
                "name": "Test competition",
                "date": "2023-12-10 08:55:23",
                "numberOfPlaces": "20",
                "investedPoints": {
                    "Test club": {
                        "places": 1,
                        "points": 2
                    }
                }
            }])
        )
    )
    def test_login_show_places_purchased(self, mocker, captured_templates, client, clubs, competitions_param):
        # datas mocked
        mocker.patch.object(server, 'competitions', competitions_param)
        mocker.patch.object(server, 'clubs', clubs)
        competition = competitions_param[0]
        data = {'email': clubs[0]['email']}

        # request client and data capture returned
        response = client.post('/showSummary', data=data, follow_redirects=True)
        res_data = response.data.decode('utf-8')
        assert len(captured_templates) == 1
        template, context = captured_templates[0]
        
        # assertion check
        assert template.name == 'welcome.html'
        res_data = response.data.decode('utf-8')
        if 'investedPoints' in context['competitions'][0]:
            assert context['competitions'][0]['investedPoints'][clubs[0]['name']]['places'] == competition['investedPoints'][clubs[0]['name']]['places']
            assert context['competitions'][0]['investedPoints'][clubs[0]['name']]['points'] == competition['investedPoints'][clubs[0]['name']]['points']
            assert f"You have: {competition['investedPoints'][clubs[0]['name']]['places']} places" in res_data
            assert f"Points invested: {competition['investedPoints'][clubs[0]['name']]['points']}" in res_data
        else:
            assert f"You have:" not in res_data
            assert f"Points invested:" not in res_data

        assert response.status_code == 200

    @pytest.mark.parametrize(
        'competitions_param',
        (
            ([{
                "name": "Test competition",
                "date": "2023-12-10 08:55:23",
                "numberOfPlaces": "20"
            }]),
            ([{
                "name": "Test competition",
                "date": "2023-12-10 08:55:23",
                "numberOfPlaces": "20",
                "investedPoints": {
                    "Test club": {
                        "places": 1,
                        "points": 2
                    }
                }
            }])
        )
    )
    def test_update_show_places_to_purchase(self, mocker, captured_templates, client, clubs, competitions_param):
        # datas mocked
        points_per_place = 1         
        mocker.patch.object(server, 'clubs', clubs)
        mocker.patch.object(server, 'competitions', competitions_param)
        mocker.patch.object(server, 'points_per_place', points_per_place)
        club = clubs[0]
        competition = competitions_param[0]
        data = {
            'competition': competition['name'],
            'club': club['name'],
            'places': 1
        }

        # request client and data capture returned
        response = client.post('/purchasePlaces', data=data, follow_redirects=True)
        res_data = response.data.decode('utf-8')
        assert len(captured_templates) == 1
        template, context = captured_templates[0]
        
        # assertion check
        assert template.name == 'welcome.html'
        assert context['competitions'][0]['investedPoints'][clubs[0]['name']]['places'] == competition['investedPoints'][clubs[0]['name']]['places']
        assert context['competitions'][0]['investedPoints'][clubs[0]['name']]['points'] == competition['investedPoints'][clubs[0]['name']]['points']
        assert f"You have: {competition['investedPoints'][clubs[0]['name']]['places']} places" in res_data
        assert f"Points invested: {competition['investedPoints'][clubs[0]['name']]['points']}" in res_data
        assert response.status_code == 200

