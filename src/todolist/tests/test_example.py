# src/todolist/tests/test_example.py

import pytest
from django.urls import reverse
from django.test import Client

@pytest.mark.django_db
def test_homepage():
    client = Client()
    response = client.get(reverse('lists:index'))  # Change 'home' to 'lists:index'
    assert response.status_code == 200
