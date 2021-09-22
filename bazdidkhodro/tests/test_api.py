import pytest
from rest_framework.test import APIClient


class ApiTestBazdidKhodro:

    @pytest.fixture
    def api_client(self):
        return APIClient()
