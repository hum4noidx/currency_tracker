import random

from locust import HttpUser, between, task

headers = {'Content-Type': 'application/json',
           'Accept': 'application/json'}

courses = ["BTCRUB", "BTCUSDT", "ETHRUB", "ETHUSDT", "USDTRUB"]


class HealthCheck(HttpUser):
    wait_time = between(10, 15)
    host = 'http://localhost:8000'

    @task
    def test_hc(self):
        self.client.get("/api/v1/ping", headers=headers)


class courses(HttpUser):
    # wait_time = between(10, 15)
    host = 'http://localhost:8000'

    @task
    def test_courses(self):
        self.client.get("/api/v1/courses/", headers=headers)

    @task
    def test_single_cource(self):
        # select random cource
        pair = random.choice(courses)
        self.client.get(f"/api/v1/courses/?trade_pair={pair}", headers=headers)
