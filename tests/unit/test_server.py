import server

class TestLogin:

    def test_login_should_200(self, mocker, client, clubs):
        mocker.patch.object(server, 'clubs', clubs)
        data = {'email': clubs[0]['email']}
        response = client.post('/showSummary', data=data, follow_redirects=True)
        assert response.status_code == 200