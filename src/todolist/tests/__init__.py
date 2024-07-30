# todolist/tests/test_views.py

import pytest
from django.urls import reverse
from django.test import Client

@pytest.mark.django_db
def test_homepage():
    client = Client()
    response = client.get(reverse('home'))  # Assuming 'home' is a name in your urls.py
    assert response.status_code == 200
    assert 'Welcome to my site' in response.content.decode()
