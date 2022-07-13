from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework import status


# ====================================================================
class PostApiTestCase(APITestCase): # теста CRUD-а поста
    # ****************************************************************
    def setUp(self):
        print('setUp')
        data = {
            'first_name': 'test_first_name',
            'last_name': 'test_last_name',
            'email': 'test@gmail.com',
            'password': 'beta_pass123'
        }
        self.user = self.client.post('/auth/users/', data=data)
        print(self.user.data)
        response = self.client.post('/auth/jwt/create/', data={
            'email': 'test@gmail.com',
            'password': 'beta_pass123'
        })
        self.request_create_post_data = {
            'title': 'test_create_post',
            'subtopic': 'test_create_subtopic',
            'text': 'test_create_text',
            'category': '',
        }
        self.token = response.data['access']
        self.api_authentication()
        print('---------------------------------------------------------------------------------------------------')
        print('---------------------------------------------------------------------------------------------------')

    # ****************************************************************
    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    # ****************************************************************
    def test_post_create_response(self):
        print('*********** test_post_create_response ***********')
        post_create_response = self.client.post('/api/post/', self.request_create_post_data)
        post_id = post_create_response.data['id']
        print('response.data ====', post_create_response.data)

        expected_data = {
            'id': post_id,
            'author': self.user.data['id'],
            'title': 'test_create_post',
            'subtopic': 'test_create_subtopic',
            'text': 'test_create_text',
            'published_date_field': post_create_response.data['published_date_field'],
            'image': None,
            'category': None,
            'likes': None,
            'dislikes': None,
            'views': None,
            'comments_count': None,
        }
        print('expected_data ====', expected_data)
        self.assertEqual(post_create_response.data, expected_data)

    # ****************************************************************
    def test_posts_get_response(self):
        print('*********** test_posts_get_response ***********')
        post_create_response = self.client.post('/api/post/', self.request_create_post_data)
        post_id = post_create_response.data['id']
        response = self.client.get('/api/post/')
        response = response.json()
        print('response.data ====', response)

        expected_data = {
            'count': 1,
            'next': None,
            'previous': None,
            'results': [{
                'id': post_id,
                'author': self.user.data['id'],
                'title': 'test_create_post',
                'subtopic': 'test_create_subtopic',
                'text': 'test_create_text',
                'published_date_field': response['results'][0]['published_date_field'],
                'image': None,
                'category': None,
                'likes': 0,
                'dislikes': 0,
                'views': 0,
                'comments_count': 0,
            }]
        }
        print('expected_data ====', expected_data)
        self.assertEqual(response, expected_data)

    # ****************************************************************
    def test_post_pust_response(self):
        print('*********** test_post_put_response ***********')
        post_create_response = self.client.post('/api/post/', self.request_create_post_data)
        post_id = post_create_response.data['id']
        print('post_id', post_id)
        print('user_id', self.user.data['id'])
        request_data = {
            'title': 'test_put',
            'subtopic': 'test_create_subtopic',
            'text': 'test_create_text',
            'category': '',
        }

        response = self.client.put(reverse('post-detail', kwargs={'id': post_id}), data=request_data)
        response = response.json()
        print('response.data ====', response)

        expected_data = {
            'id': post_id,
            'author': self.user.data['id'],
            'title': 'test_put',
            'subtopic': 'test_create_subtopic',
            'text': 'test_create_text',
            'published_date_field': response['published_date_field'],
            'image': None,
            'category': None,
            'likes': 0,
            'dislikes': 0,
            'views': 0,
            'comments_count': 0,
        }
        print('expected_data ====', expected_data)
        self.assertEqual(response, expected_data)

    # ****************************************************************
    def test_post_delete_status(self):
        print('*********** test_post_delete_response ***********')
        post_create_response = self.client.post('/api/post/', self.request_create_post_data)
        post_id = post_create_response.data['id']
        print('post_id', post_id)
        print('user_id', self.user.data['id'])
        response = self.client.delete(reverse('post-detail', kwargs={'id': post_id}))
        print('response.data ====', response)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


# ====================================================================
class CommentApiTestCase(APITestCase): # тест CRUD-а коммента
    # ****************************************************************
    def setUp(self):
        print('setUp')
        data = {
            'first_name': 'test_first_name',
            'last_name': 'test_last_name',
            'email': 'test@gmail.com',
            'password': 'beta_pass123'
        }
        self.user = self.client.post('/auth/users/', data=data)
        print(self.user.data)
        response = self.client.post('/auth/jwt/create/', data={
            'email': 'test@gmail.com',
            'password': 'beta_pass123'
        })
        self.request_create_post_data = {
            'title': 'test_create_post',
            'subtopic': 'test_create_subtopic',
            'text': 'test_create_text',
            'category': '',
        }
        self.token = response.data['access']
        self.api_authentication()

        self.post_create_response = self.client.post('/api/post/', self.request_create_post_data)
        self.post_id = self.post_create_response.data['id']

        request_data = {
            'post': self.post_id,
            'text': 'test_comment_text'
        }
        self.comment_create_response = self.client.post('/api/comment/', data=request_data)
        self.comment_id = self.comment_create_response.data['id']

        print('---------------------------------------------------------------------------------------------------')
        print('---------------------------------------------------------------------------------------------------')

    # ****************************************************************
    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    # ****************************************************************
    def test_comment_create_response(self):
        print('*********** test_comment_create_response ***********')
        print('post_id', self.post_id)
        print('user_id', self.user.data['id'])
        print('response.data ====', self.comment_create_response.data)
        expected_data = {
            "id": self.comment_id,
            "post": self.post_id,
            "user": self.user.data['id'],
            "text": "test_comment_text",
            "created_at": self.comment_create_response.data['created_at']
        }
        print('expected_data ====', expected_data)
        self.assertEqual(self.comment_create_response.data, expected_data)

    # ****************************************************************
    def test_comments_get_response(self):
        print('*********** test_comments_get_response ***********')
        print('post_id', self.post_id)
        print('user_id', self.user.data['id'])
        print('comment_id', self.comment_id)

        response = self.client.get('/api/comment/')
        response = response.json()
        print('response.data ====', response)
        expected_data = {
            "count": 1,
            "next": None,
            "previous": None,
            "results": [
                {
                    "id": self.comment_id,
                    "post": self.post_id,
                    "user": self.user.data['id'],
                    "text": self.comment_create_response.data['text'],
                    "created_at": response['results'][0]['created_at']
                },
            ]
        }
        print('expected_data ====', expected_data)
        self.assertEqual(response, expected_data)

    # ****************************************************************
    def test_comment_put_response(self):
        print('*********** test_comments_put_response ***********')
        print('post_id', self.post_id)
        print('user_id', self.user.data['id'])
        print('comment_id', self.comment_id)
        request_data = {
            'post': self.post_id,
            'text': 'test_put_text'
        }

        response = self.client.put(reverse('comment-detail', kwargs={'pk': self.comment_id}), data=request_data)
        response = response.json()
        print('response.data ====', response)
        expected_data = {
            "id": self.comment_id,
            "post": self.post_id,
            "user": self.user.data['id'],
            "text": 'test_put_text',
            "created_at": response['created_at']
        }
        print('expected_data ====', expected_data)
        self.assertEqual(response, expected_data)

    # ****************************************************************
    def test_comment_delete_status(self):
        print('*********** test_comments_put_response ***********')
        print('post_id', self.post_id)
        print('user_id', self.user.data['id'])
        print('comment_id', self.comment_id)
        response = self.client.delete(reverse('comment-detail', kwargs={'pk': self.comment_id}))
        print('response.data ====', response)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


# ====================================================================
class LikeDislikeOnPostApiTestCase(APITestCase): # тест лайка/дизлайка на пост
    # ****************************************************************
    def setUp(self):
        print('setUp')
        data = {
            'first_name': 'test_first_name',
            'last_name': 'test_last_name',
            'email': 'test@gmail.com',
            'password': 'beta_pass123'
        }
        self.user = self.client.post('/auth/users/', data=data)
        print(self.user.data)
        response = self.client.post('/auth/jwt/create/', data={
            'email': 'test@gmail.com',
            'password': 'beta_pass123'
        })
        self.request_create_post_data = {
            'title': 'test_create_post',
            'subtopic': 'test_create_subtopic',
            'text': 'test_create_text',
            'category': '',
        }
        self.token = response.data['access']
        self.api_authentication()

        self.post_create_response = self.client.post('/api/post/', self.request_create_post_data)
        self.post_id = self.post_create_response.data['id']
        print('---------------------------------------------------------------------------------------------------')
        print('---------------------------------------------------------------------------------------------------')

    # ****************************************************************
    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    # ****************************************************************
    def test_like_on_post_response(self):
        print('*********** test_like_on_post_response ***********')
        print('post_id', self.post_id)
        print('user_id', self.user.data['id'])
        request_data = {'like': True}
        expected_data = {
            'post_id': self.post_id,
            'user_id': self.user.data['id'],
            'like': True
        }
        response = self.client.patch(reverse('like', kwargs={'id': self.post_id}), data=request_data)
        print('response.data ====', response.data)
        print('expected_data ====', expected_data)
        self.assertEqual(response.data, expected_data)

    # ****************************************************************
    def test_dislike_on_post_response(self):
        print('*********** test_dislike_on_post_response ***********')
        print('post_id', self.post_id)
        print('user_id', self.user.data['id'])
        request_data = {'dislike': True}

        expected_data = {
            'post_id': self.post_id,
            'user_id': self.user.data['id'],
            'dislike': True
        }
        response = self.client.patch(reverse('dislike', kwargs={'id': self.post_id}), data=request_data)
        print('response.data ====', response.data)
        print('expected_data ====', expected_data)
        self.assertEqual(response.data, expected_data)


# ====================================================================
# class PostAnalyticsApiTestCase(APITestCase): # тест аналики поста
#     # ****************************************************************
#     def setUp(self):
#         print('setUp')
#         data = {
#             'first_name': 'test_first_name',
#             'last_name': 'test_last_name',
#             'email': 'test@gmail.com',
#             'password': 'beta_pass123'
#         }
#         self.user = self.client.post('/auth/users/', data=data)
#         print(self.user.data)
#         response = self.client.post('/auth/jwt/create/', data={
#             'email': 'test@gmail.com',
#             'password': 'beta_pass123'
#         })
#         self.request_create_post_data = {
#             'title': 'test_create_post',
#             'subtopic': 'test_create_subtopic',
#             'text': 'test_create_text',
#             'category': '',
#         }
#         self.token = response.data['access']
#         self.api_authentication()
#
#         self.post_create_response = self.client.post('/api/post/', self.request_create_post_data)
#         self.post_id = self.post_create_response.data['id']
#         print('---------------------------------------------------------------------------------------------------')
#         print('---------------------------------------------------------------------------------------------------')
#
#     # ****************************************************************
#     def api_authentication(self):
#         self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)
#
#     # ****************************************************************
#     def test_all_posts_activity_response(self):
#         print('*********** test_all_posts_activity_response ***********')
#         print('post_id', self.post_id)
#         print('user_id', self.user.data['id'])
#         expected_data = {
#             'likes_count': 1,
#             'dislike_count': 2,
#             'views_count': 6
#         }
#         response = self.client.get(reverse('post_analytics'))
#         print('response.data ====', response.data)
#         print('expected_data ====', expected_data)
#         self.assertEqual(response.data, expected_data)
#


# ====================================================================
class UserActivityApiTestCase(APITestCase): # тест активности юзера
    # ****************************************************************
    def setUp(self):
        print('setUp')
        data = {
            'first_name': 'test_first_name',
            'last_name': 'test_last_name',
            'email': 'test@gmail.com',
            'password': 'beta_pass123'
        }
        self.user = self.client.post('/auth/users/', data=data)
        print(self.user.data)
        response = self.client.post('/auth/jwt/create/', data={
            'email': 'test@gmail.com',
            'password': 'beta_pass123'
        })
        self.request_create_post_data = {
            'title': 'test_create_post',
            'subtopic': 'test_create_subtopic',
            'text': 'test_create_text',
            'category': '',
        }
        self.token = response.data['access']
        self.api_authentication()

        self.post_create_response = self.client.post('/api/post/', self.request_create_post_data)
        self.post_id = self.post_create_response.data['id']
        print('---------------------------------------------------------------------------------------------------')
        print('---------------------------------------------------------------------------------------------------')

    # ****************************************************************
    def api_authentication(self):
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + self.token)

    # ****************************************************************
    def test_user_activity_response(self):
        print('*********** test_user_activity_response ***********')
        print('post_id', self.post_id)
        print('user_id', self.user.data['id'])
        response = self.client.get(reverse('user_activity', kwargs={'id': self.user.data['id']}))
        expected_data = {
            'first_name': self.user.data['first_name'],
            'last_name': self.user.data['last_name'],
            'email': self.user.data['email'],
            'date_joined': response.data['date_joined'],
            'last_login': response.data['last_login'],
            'last_request': response.data['last_request']
        }
        print('response.data ====', response.data)
        print('expected_data ====', expected_data)
        self.assertEqual(response.data, expected_data)
