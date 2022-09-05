import server
import pytest

class TestPurchasePlaces:

    def test_points_deducted_at_purchase(self, mocker, captured_templates, client, clubs, competitions):
        mocker.patch.object(server, 'clubs', clubs)
        mocker.patch.object(server, 'competitions', competitions)
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