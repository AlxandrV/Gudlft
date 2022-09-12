import server
class TestIntegration:

    def test_should_login_showsummary_logout(self, mocker, captured_templates, client, clubs, competitions):
        mocker.patch.object(server, 'clubs', clubs)
        mocker.patch.object(server, 'competitions', competitions)
        club = clubs[0]

        # Index
        response = client.get('/')
        assert len(captured_templates) == 1
        template, context = captured_templates[0]
        assert template.name == 'index.html'
        assert response.status_code == 200

        # Login
        email = {'email': club['email']}
        response = client.post('/showSummary', data=email)
        assert captured_templates[1][1]['club'] == club
        assert captured_templates[1][1]['competitions'] == competitions
        assert captured_templates[1][0].name == 'welcome.html'
        assert response.status_code == 200

        # Logout
        response = client.get('/logout', follow_redirects=True)
        assert captured_templates[2][0].name == 'index.html'
        assert response.status_code == 200

    def test_booking_page_and_purchase(self, mocker, captured_templates, client, clubs, competitions):
        points_per_place = 1
        mocker.patch.object(server, 'clubs', clubs)
        mocker.patch.object(server, 'competitions', competitions)
        mocker.patch.object(server, 'points_per_place', points_per_place)

        club = clubs[0]
        competition = competitions[0]

        # Booking page
        response = client.get(f"/book/{competition['name']}/{club['name']}")
        assert len(captured_templates) == 1
        template, context = captured_templates[0]
        assert template.name == 'booking.html'
        assert context['club'] == club
        assert context['competition'] == competition
        assert response.status_code == 200

        # Purchase
        data = {
            'competition': competition['name'],
            'club': club['name'],
            'places': 1
        }
        response = client.post('/purchasePlaces', data=data)
        assert captured_templates[1][1]['club'] == club
        assert captured_templates[1][1]['competitions'] == competitions
        assert captured_templates[1][0].name == 'welcome.html'
