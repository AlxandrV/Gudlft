import server
import pytest

class TestPurchasePlaces:
    
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
            'places': places
        }

        # request client and data capture returned
        response = client.post('/purchasePlaces', data=data, follow_redirects=True)
        res_data = response.data.decode('utf-8')
        assert len(captured_templates) == 1
        template, context = captured_templates[0]
        
        # assertion check
        assert template.name == 'welcome.html'
        if data['places'] > int(club_points_after) or data['places'] > int(number_of_places_after) or data['places'] < 0:
            # Number of places is invalid
            assert int(context['club']['points']) == int(club_points_after)
            assert int(context['competitions'][0]['numberOfPlaces']) == int(number_of_places_after)
            if data['places'] > int(club_points_after):
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
