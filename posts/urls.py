from django.urls import path
from . import views

app_name = 'posts' 
urlpatterns = [
    path('add_question', views.AddQuestionView.as_view(),
     name='add_question'),
    path('<int:question_id>/', views.PostListView.as_view(),
     name='discussion'),
    path('<int:question_id>/add_post', views.PostCreateView.as_view(),
     name='add_post'),
    path('<int:post_id>/edit_post', views.PostEditView.as_view(),
     name='edit_post'),
    path('<int:post_id>/delete_post', views.PostDeleteView.as_view(),
     name='delete_post'),
    path('<int:question_id>/vote', views.vote, name='vote'),    
    path('<int:question_id>/vote_results', views.VoteResultsView.as_view(),
     name='vote_results'),
]    