from django.test import TestCase
from posts.models import Question
from accounts.models import CustomUser, CustomUserManager


class QuestionModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):       
        user = CustomUser.objects.create_user(
            'gooduser', 'gooduser@mail.com', 'password')
        Question.objects.create(question_text='is groundhog good to eat?', user=user)

    def test_q_text_content(self):
        question = Question.objects.get(id=1)
        expected_object_text = f'{question.question_text}'
        self.assertEqual(expected_object_text, 'is groundhog good to eat?')

    def test_q_user_content(self):
        question = Question.objects.get(id=1)
        expected_object_user = f'{question.user.username}'
        self.assertEqual(expected_object_user, 'gooduser')
