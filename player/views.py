from django.views import generic
from django.conf import settings
from posts.models import Question
from .utils import shuffle_tracks


class IndexView(generic.ListView):
    template_name = 'player/index.html'
    context_object_name = 'latest_question_list'
    tracks_path = settings.TRACKS_PATH

    def get_queryset(self):
        # return the last published questions
        return Question.objects.order_by('-pub_date')[:12]

    def get_context_data(self, **kwargs):        
        context = super().get_context_data(**kwargs)
        # pass shuffled tracklist to template    
        context['tracklist'] = shuffle_tracks(self.tracks_path)       
        return context