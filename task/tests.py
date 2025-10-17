from django.test import TestCase

# Create your tests here.
# tasks/tests.py
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from user.models import User
from .models import Task

class TaskAPITestCase(APITestCase):

    def setUp(self):
        # create two users
        self.user1 = User.objects.create_user(email='alice@task.com', password='alicepass',username='alice')
        self.user2 = User.objects.create_user(email='bob@task.com', password='bobpass',username='bob')
        # create tasks
        self.task1 = Task.objects.create(owner=self.user1, title='Task 1', description='first', completed=False)
        self.task2 = Task.objects.create(owner=self.user2, title='Task 2', description='second', completed=True)

    def obtain_token(self, email, password):
        url = reverse('token_obtain_pair')
        resp = self.client.post(url, {'email': email, 'password': password}, format='json')
        return resp.data.get('access')

    def test_register_and_token(self):
        # register
        url = reverse('signup')
        resp = self.client.post(url, {'email': 'charlie@task.com', 'password': 'charliepass','username':'charlie'}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        # obtain token
        token = self.obtain_token('charlie@task.com', 'charliepass')
        self.assertTrue(token is not None)

    def test_list_tasks_anonymous(self):
        resp = self.client.get('/api/tasks/')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.assertGreaterEqual(len(resp.data['results']), 2)

    def test_create_task_authenticated(self):
        token = self.obtain_token('alice@task.com', 'alicepass')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        resp = self.client.post('/api/tasks/', {'title': 'New', 'description': 'x'}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_201_CREATED)
        self.assertEqual(resp.data['owner'], 'alice')

    def test_create_task_unauthenticated_forbidden(self):
        resp = self.client.post('/api/tasks/', {'title': 'NoAuth'}, format='json')
        self.assertIn(resp.status_code, (status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN))

    def test_update_task_owner_only(self):
        token = self.obtain_token('alice@task.com', 'alicepass')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        url = f'/api/tasks/{self.task1.id}/'
        resp = self.client.put(url, {'title': 'Updated', 'description': 'd', 'completed': True}, format='json')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        self.task1.refresh_from_db()
        self.assertTrue(self.task1.completed)

    def test_update_task_not_owner_forbidden(self):
        token = self.obtain_token('alice@task.com', 'alicepass')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        url = f'/api/tasks/{self.task2.id}/'
        resp = self.client.put(url, {'title': 'X', 'description': 'd', 'completed': False}, format='json')
        self.assertIn(resp.status_code, (status.HTTP_403_FORBIDDEN, status.HTTP_401_UNAUTHORIZED))

    def test_filter_by_completed(self):
        resp = self.client.get('/api/tasks/?completed=true')
        self.assertEqual(resp.status_code, status.HTTP_200_OK)
        # only task2 is completed (from setUp)
        results = resp.data['results']
        self.assertTrue(any(t['id']==self.task2.id for t in results))
