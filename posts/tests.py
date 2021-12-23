from django.test import TestCase, SimpleTestCase, RequestFactory
from django.urls import reverse
from django.utils import timezone
from django.contrib.messages.storage.fallback import FallbackStorage
from accounts.models import CustomUser, CustomUserManager
from .models import Question, Choice, Post
from .views import AddQuestionView, PostCreateView, PostEditView, PostDeleteView,\
    PostListView, vote


class BaseUserTest():
    # create user, RequestFactory instance
    def setUp(self):
        self.user1 = CustomUser.objects.create_user(
            username='good_user', email='good_user@mail.com', password='good_password')
        self.user1.save()
        self.factory = RequestFactory()

    def mock_message_add(self, request):
        # RequestFactory requests can't be used
        # to test views that call messages.add
        setattr(request, 'session', 'session')
        messages = FallbackStorage(request)
        setattr(request, '_messages', messages)
        return request
        

class BasePostQuestionUserTest(BaseUserTest):
    def setUp(self):
        # create user and RequestFactory instance
        super().setUp()
        self.data_question = {'question': 'How much your cat is sleeping?',\
            'choice_text_1': 'All day long',\
            'choice_text_2': 'I\'ve no idea'}
        # create question        
        self.question1 = Question(
            question_text=self.data_question['question'], user=self.user1)
        self.question1.save()  
        # create choices
        self.choice1 = Choice(
            question=self.question1, choice_text=self.data_question['choice_text_1'])
        self.choice2 = Choice(
            question=self.question1, choice_text=self.data_question['choice_text_2'])      
        # create post
        self.post1 = Post(
            body='Not a very good post', question=self.question1, user=self.user1)
        self.post1.save()


class AddQuestionTest(BaseUserTest, TestCase):
    # call BaseUserTest.setUp()   

    def test_add_question(self):
        # try to create question
        url = 'posts:add_question'
        data_question = {'question': 'How much your cat is sleeping?',\
            'choice_text_1': 'All day long',\
            'choice_text_2': 'I\'ve no idea'}                    
        request = self.factory.post(reverse(url), data_question)
        request.user = self.user1
        response = AddQuestionView.as_view()(request)
        self.assertEqual(Question.objects.all().count(), 1)
        self.assertEqual(
            Question.objects.all()[0].question_text, data_question['question'])
        self.assertEqual(Question.objects.all()[0].user, self.user1)
        self.assertEqual(self.user1.question_set.all().count(), 1)        
        self.assertEqual(Choice.objects.all().count(), 2)
        self.assertEqual(
            Choice.objects.all()[0].choice_text, data_question['choice_text_1'])


class AddPostTest(BaseUserTest, TestCase):
    def setUp(self):
        # create user, RequestFactory instance and question
        super().setUp()
        question_text = 'How much your cat is sleeping?'
        self.question1 = Question(
            question_text=question_text, user=self.user1)
        self.question1.save()

    def test_post_create(self):
        # try to create post
        url_add_post = 'posts:add_post'      
        kwargs = {'question_id': self.question1.id}
        data_from_user = {'body': 'Mine is running all days and nights somewhere outside'}    
        request = self.factory.post(reverse(
            url_add_post,args=(kwargs['question_id'],)), data_from_user)
        request.user = self.user1
        response = PostCreateView.as_view()(request, **kwargs)
        self.assertEqual(Post.objects.all().count(), 1)
        self.assertEqual(Post.objects.all()[0].body, data_from_user['body'])
        self.assertEqual(Post.objects.all()[0].question.id, self.question1.id)
        self.assertEqual(Post.objects.all()[0].user, self.user1)


class UpdatePostTest(BasePostQuestionUserTest, TestCase):
    # call PostQuestionUserBaseTest.setUp()

    def test_post_update(self):
        # update post                        
        url_edit_post = 'posts:edit_post'        
        kwargs = {'post_id': self.post1.id}
        data_update = {'body': 'Good post', 'question': self.question1.id}
        request = self.factory.post(
            reverse(url_edit_post, args=(self.post1.id,)), data_update)        
        request.user = self.user1
        # PostEditView will call message middleware
        # call PostBaseTestCase.mock_message_add
        self.mock_message_add(request)
        response = PostEditView.as_view()(request, **kwargs)
        self.assertEqual(Post.objects.all().count(), 1)
        self.assertEqual(Post.objects.all()[0].body, data_update['body'])
        self.assertEqual(Post.objects.all()[0].question.id, self.question1.id)
        self.assertEqual(Post.objects.all()[0].user, self.user1)
              
        
class DeletePostTest(BasePostQuestionUserTest, TestCase):
    # call BasePostQuestionUserTest.setUp()                
    def test_delete_post(self):
        # delete post
        kwargs = {'post_id': self.post1.id}
        url_delete_post = 'posts:delete_post'     
        request = self.factory.post(reverse(url_delete_post, args=(self.post1.id,)))
        request.user = self.user1
        response = PostDeleteView.as_view()(request, **kwargs)
        self.assertEqual(Post.objects.all().count(), 0)
        self.assertEqual(self.user1.post_set.all().count(), 0)


class PagesCodeURlTest(BasePostQuestionUserTest, TestCase):
    
    def setUp(self):
        super().setUp()

        question_id = str(self.question1.id)
        post_id = str(self.post1.id)

        self.pages = ['/posts/add_question', 
         '/posts/'+question_id,
         '/posts/'+question_id+'/add_post',
         '/posts/'+post_id+'/edit_post', 
         '/posts/'+post_id+'/delete_post', 
         '/posts/'+question_id+'/vote', 
         '/posts/'+question_id+'/vote_results']  

    def test_page_status_code(self):
        for page in self.pages:
            with self.subTest(page=page):
                response = self.client.get(page)
                self.assertNotEqual(response.status_code, 404)
