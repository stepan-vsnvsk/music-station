from django.test import TestCase, SimpleTestCase, RequestFactory
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.messages.storage.fallback import FallbackStorage
from .models import CustomUser, CustomUserManager
from .views import ProfileView, MessageCreateView


class PagesSimpleTests(SimpleTestCase):

    pages = ['/accounts/signup/', '/accounts/login/', 
     '/accounts/reset_password/', '/accounts/reset_password_sent/', 
     '/accounts/reset/done']  

    urls = ['accounts:signup', 'accounts:login', 'accounts:reset_password',
        'accounts:password_reset_done', 'accounts:password_reset_complete']

    templates = ['accounts/registration/signup.html',
        'accounts/registration/login.html',
        'accounts/registration/reset_password.html',
        'accounts/registration/password_reset_done.html',
        'accounts/registration/password_reset_complete.html']

    url_template_tuple = tuple(zip(urls, templates))

    def test_page_status_code(self):
        for page in self.pages:
            with self.subTest(page=page):
                response = self.client.get(page)
                self.assertEqual(response.status_code, 200)

    def test_view_url_code_by_name(self):
        for url in self.urls:
            with self.subTest(url=url):
                response = self.client.get(reverse(url))
                self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        for url_template in self.url_template_tuple:
            with self.subTest(url_template=url_template):
                url, template = url_template
                response = self.client.get(reverse(url))                
                self.assertTemplateUsed(response, template)


class SignUpTestCase(TestCase):
    username = 'gooduser'
    email = 'gooduser@mail.com'
    image = SimpleUploadedFile(
            "media/avatars/default.jpg", b"file_content", content_type="image/jpeg")      

    def test_signup_form(self):        
        new_user = CustomUser.objects.create_user(
            self.username, self.email, 'password', avatar=self.image)
        self.assertEqual(CustomUser.objects.all().count(), 1)
        self.assertEqual(CustomUser.objects.all()[0].username, self.username)
        self.assertEqual(CustomUser.objects.all()[0].email, self.email)
                

class AuthTestCase(TestCase):
    def setUp(self):
        self.u = CustomUser.objects.create_user(
            username='gooduser', email='gooduser@mail.com', password='password')       
        self.u.save()

    def test_login(self):
        self.client.login(username='gooduser', password='password')


class TwoUsersBaseTestCase():
    def setUp(self):
        # create two users and instance of RequestFactory
        self.user1 = CustomUser.objects.create_user(
            username='first_user', email='first_user@mail.com', password='password')       
        self.user1.save()
        self.user2 = CustomUser.objects.create_user(
            username='second_user', email='second_user@mail.com', password='password')       
        self.user2.save()
        self.factory = RequestFactory()

    def mock_message_add(self, request):
        # RequestFactory requests can't be used
        # to test views that call messages.add
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        return request


class FollowerTestCase(TwoUsersBaseTestCase, TestCase):
    # call TwoUsersBaseTestCase.setUp()
    # create two users and instance of RequestFactory           
        
    def test_follow_unfollow_user(self):
        url = 'accounts:profile'
        #request to follow
        request = self.factory.post(
            reverse(url, args=(self.user1.id,)))
        request.user = self.user2
        # ProfileView will call message middleware
        # call TwoUsersBaseTestCase.mock_message_add
        self.mock_message_add(request)
        response = ProfileView.as_view()(request, pk=self.user1.id)
        self.assertEqual(self.user1.follower.all()[0], self.user2)
        self.assertEqual(self.user2.customuser_set.all()[0], self.user1)
        
    def test_unfollow_user(self):
        # add user's follower
        self.user1.follower.add(self.user2)
        self.user1.save()        
        self.assertEqual(self.user1.follower.all()[0], self.user2)
        self.assertEqual(self.user2.customuser_set.all()[0], self.user1)
        url = 'accounts:profile'
        # request to unfollow
        request = self.factory.post(
            reverse(url, args=(self.user1.id,)))
        request.user = self.user2
        # call TwoUsersBaseTestCase.mock_message_add
        self.mock_message_add(request)
        response = ProfileView.as_view()(request, pk=self.user1.id)
        self.assertEqual(self.user1.follower.all().count(), 0)
        self.assertEqual(self.user2.customuser_set.all().count(), 0)


class MessageTestCase(TwoUsersBaseTestCase, TestCase):
    # call TwoUsersBaseTestCase.setUp()
    # create two users and instance of RequestFactory     

    def test_private_message(self):
        url = 'accounts:send_message'
        data = {'body': 'Keep it up!'}
        request = self.factory.post(
            reverse(url, args=(self.user1.id,)), data)
        request.user = self.user2
        #call TwoUsersBaseTestCase.mock_message_add
        self.mock_message_add(request)
        response = MessageCreateView.as_view()(request, pk=self.user1.id)        
        self.assertEqual(self.user1.recipient.all().count(), 1)
        self.assertEqual(self.user1.recipient.all()[0].sender, self.user2)
        self.assertEqual(self.user1.recipient.all()[0].body, data['body'])


class ProfilePageTestCase(TestCase):
    def setUp(self):
        # create user and instance of RequestFactory
        self.user1 = CustomUser.objects.create_user(
            username='first_user', email='first_user@mail.com', password='password')       
        self.user1.save()
        self.factory = RequestFactory()
        

    def test_profile_page(self):
        url = 'accounts:profile'      
        template = 'accounts/profile/user_profile.html'  
        request = self.factory.get(
            reverse(url, args=(self.user1.id,)))
        request.user = self.user1
        response = ProfileView.as_view()(request, pk=self.user1.id)
        self.assertEqual(response.status_code, 200)
        



