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
