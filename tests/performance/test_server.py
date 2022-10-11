from locust import HttpUser, task

class GudlftPerfTest(HttpUser):

    @task
    def home(self):
        self.client.get('')

    @task
    def showSummary(self):
        data = {"email": "admin@test.com"}
        self.client.post('showSummary', data=data)

    @task
    def book(self):
        self.client.get('book/Test competitions/Admin')

    @task
    def purchasePlaces(self):
        data = {"club": "Admin", "competition": "Test competitions", "places": 3}
        self.client.post('purchasePlaces', data=data)

    @task
    def publicBoard(self):
        self.client.get('board')

    @task
    def logout(self):
        self.client.get('logout')