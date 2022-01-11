from django.urls import path
from .views import QuestionViewSet, PostViewSet
from rest_framework.routers import SimpleRouter


app_name = 'api' 

router = SimpleRouter()
router.register('question', QuestionViewSet, basename='questions')
router.register('post', PostViewSet, basename='posts')
urlpatterns = router.urls