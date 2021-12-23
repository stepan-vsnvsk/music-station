from django.http import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import get_object_or_404, render
from django.views import generic, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.core.paginator import Paginator
from django.core.exceptions import PermissionDenied
from django.conf import settings
from django.db import transaction
from django.utils import timezone
from accounts.models import CustomUser
from .models import Question, Choice, Post
from .forms import AddQuestionForm, AddPostForm, EditPostForm


class AddQuestionView(LoginRequiredMixin, View):
    # create new question with choices
    form_class = AddQuestionForm
    template_name = 'posts/add_question.html'
    login_url = settings.LOGIN_URL

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        user = request.user        
        if form.is_valid():
            with transaction.atomic():
                # save question
                new_question = Question(
                    question_text=form.cleaned_data['question'], user=user)            
                new_question.pub_date = timezone.now()
                new_question.save()
                # save choices
                choices = form.cleaned_data['choice_text_1'],\
                 form.cleaned_data['choice_text_2'], form.cleaned_data['choice_text_3']
                for choice in choices:
                    if choice:
                        new_choice = Choice(question=new_question, choice_text=choice)
                        new_choice.save()
            return HttpResponseRedirect(
                reverse('posts:discussion', args=(new_question.id,)))


class PostListView(generic.ListView):
    # show posts and question
    template_name = 'posts/posts_list.html'
    context_object_name = 'posts'
    paginate_by = 6

    def get_queryset(self):        
        return Post.objects.filter(question=self.kwargs['question_id']).\
        order_by('-timestamp').select_related('user')

    def get_context_data(self, **kwargs): 
        # pass question and form for new posts
        context = super().get_context_data(**kwargs)
        context['addpost_form'] = AddPostForm()        
        context['question'] = Question.objects.get(id=self.kwargs['question_id'])
        return context


class PostCreateView(LoginRequiredMixin, generic.CreateView):
    # process submitted post 
    login_url = settings.LOGIN_URL
    model = Post
    fields = ['body']    

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.question = get_object_or_404(
            Question, pk=self.kwargs['question_id'])        
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('posts:discussion', args=(self.kwargs['question_id'],))


class PostEditView(SuccessMessageMixin, generic.UpdateView):
    # edit post     
    model = Post
    form_class = EditPostForm
    template_name = 'posts/edit_post.html'    
    success_message = "Post has been updated"

    def get_object(self, queryset=None):
        # get user's post
        post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        if not post.user == self.request.user:
            raise PermissionDenied()        
        return post

    def get_success_url(self):
        return self.request.GET.get('next', reverse('accounts:home'))


class PostDeleteView(SuccessMessageMixin, generic.DeleteView):
    # delete post     
    model = Post 
    template_name = 'posts/delete_post.html'
    success_message = "Post has been deleted"

    def get_object(self, queryset=None):
        # get user's post
        post = get_object_or_404(Post, pk=self.kwargs['post_id'])
        if not post.user == self.request.user:
            raise PermissionDenied()        
        return post
    
    def get_success_url(self):
        return self.request.GET.get('next', reverse('accounts:home'))


@login_required(login_url=settings.LOGIN_URL)
def vote(request, question_id):
    # process submitted user's choice
    question = get_object_or_404(Question, pk=question_id)
    user = request.user    
    try:
        # get the choice
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except(KeyError, Choice.DoesNotExist):
        posts = Post.objects.filter(question=int(question.id))        
        return render(request, 'posts/discussion.html', {'question': question,\
            'posts': posts, 'error_message': "You didn't select a choice."})
    else:
        # checking if voted before
        if user not in selected_choice.user.all():
            # save the choice
            with transaction.atomic():
                selected_choice.votes += 1
                selected_choice.user.add(user)
                selected_choice.save()
            return HttpResponseRedirect(
                reverse('posts:vote_results', args=(question.id,)))
        else: # made a choice before -> back to question page with error message
            posts = Post.objects.filter(question=int(question.id))
            return render(request, 'posts/posts_list.html',
                {'question': question, 'posts': posts,\
                'addpost_form': AddPostForm(),
                'error_message': "Only one vote from user!"})


class VoteResultsView(generic.DetailView):
    # show polls results
    pk_url_kwarg = 'question_id'
    model = Question
    template_name = 'posts/vote_results.html'
    