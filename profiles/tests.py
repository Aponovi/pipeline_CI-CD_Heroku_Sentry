import pytest
from django.contrib.auth import get_user_model
from django.test import Client
from django.urls import reverse
from pytest_django.asserts import assertTemplateUsed

from .models import Profile

User = get_user_model()


@pytest.mark.django_db(transaction=True, reset_sequences=True)
class Tests_Profiles_Views:

    def test_profiles_index_view(self):
        client = Client()
        expected_content_1 = '<title>Profiles</title>'
        expected_content_2 = '<h1>Profiles</h1>'
        expected_content_3 = 'Batman'
        user = User.objects.create(username='Batman',
                                   password='jokerwillpay4it',
                                   first_name='Bruce',
                                   last_name='Wayne',
                                   email='bruce.wayne@')
        Profile.objects.create(user_id=user.id,
                               favorite_city='Paris'
                               )
        path = reverse('profiles:index')
        response = client.get(path)
        content = response.content.decode()

        assert expected_content_1 in content
        assert expected_content_2 in content
        assert expected_content_3 in content
        assert response.status_code == 200
        assertTemplateUsed(response, "profiles/index.html")

    def test_profiles_profile_view(self):
        client = Client()
        expected_content_1 = '<title>Batman</title>'
        expected_content_2 = '<h1>Batman</h1>'
        expected_content_3 = 'Paris'
        user = User.objects.create(username='Batman',
                                   password='jokerwillpay4it',
                                   first_name='Bruce',
                                   last_name='Wayne',
                                   email='bruce.wayne@')
        Profile.objects.create(user_id=user.id,
                               favorite_city='Paris'
                               )
        path = reverse('profiles:profile', kwargs={'username': 'Batman'})
        response = client.get(path)
        content = response.content.decode()

        assert expected_content_1 in content
        assert expected_content_2 in content
        assert expected_content_3 in content
        assert response.status_code == 200
        assertTemplateUsed(response, "profiles/profile.html")
