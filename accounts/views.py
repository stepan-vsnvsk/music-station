from django.shortcuts import get_object_or_404, render
from django.urls import reverse, reverse_lazy
from django.http import HttpResponseRedirect
from django.utils import timezone
from django.db import transaction
from django.views import generic
from django.contrib import messages
from django.contrib.messages.views import SuccessMessageMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.core.exceptions import PermissionDenied
from django.conf import settings
from posts.models import Post
from .forms import CustomUserCreationForm, CustomUserChangeForm,\
    MessageForm, EmptyForm
from .models import CustomUser, Message


class HomePageTemplateView(generic.TemplateView):
    # render home page
    template_name = 'accounts/home.html'


class SignUpView(generic.CreateView):
    # register new user
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('accounts:login')
    template_name = 'accounts/registration/signup.html'


class ProfileView(LoginRequiredMixin, generic.DetailView):
    # user's profile page
    model = CustomUser
    template_name = 'accounts/profile/user_profile.html'
    context_object_name = 'user_profile'
    form_class = EmptyForm
    
    def get_context_data(self, **kwargs):
        # pass to template 
        # posts made by user and messages that send to him
        context = super().get_context_data(**kwargs)
        user = get_object_or_404(CustomUser, pk=self.kwargs['pk'])                        
        context['new_private_messages'] = Message.objects.filter(
            recipient=user).filter(timestamp__gte=user.read_message_last_time)
        posts = Post.objects.filter(user=user).order_by('-timestamp')        
        page_number = self.request.GET.get('page')    
        context['posts_paginated'] = Paginator(posts, 5).get_page(page_number)
        return context
    
    def post(self, request, *args, **kwargs):
        # accept "follow user" as post request
        form = self.form_class(request.POST)
        user_to_follow = get_object_or_404(CustomUser, pk=self.kwargs['pk'])        
        user_made_request = CustomUser.objects.get(id=request.user.id)     
        
        if form.is_valid():# 'follow' request
            if user_made_request not in user_to_follow.follower.all():                
                with transaction.atomic():
                    user_to_follow.follower.add(user_made_request)
                    user_to_follow.save()                
                messages.success(
                    request, 'You are follow {} now!'.format(user_to_follow.username))
                return HttpResponseRedirect(
                    reverse('accounts:profile', args=(user_to_follow.id,)))
            else: # unfollow request
                user_made_request.customuser_set.remove(user_to_follow)
                messages.success(
                    request, 'You are not following {}!'.format(user_to_follow.username))
                return HttpResponseRedirect(
                    reverse('accounts:profile', args=(user_to_follow.id,)))

        else: # -> back to profile page with error message
            return render(request, reverse('accounts:profile', args=(user_to_follow.id,)),
             {'error_message': "Your request were denied. We are sorry!"})


class EditProfileView(SuccessMessageMixin, generic.UpdateView):
    # edit profile data
    model = CustomUser    
    form_class = CustomUserChangeForm
    template_name = 'accounts/profile/edit_profile.html'    
    success_message = "Profile has been updated successfully"    
        
    def get_object(self, queryset=None):
        user = get_object_or_404(CustomUser, pk=self.kwargs['pk'])
        if not user == self.request.user:
            raise PermissionDenied()        
        return user


class MessageCreateView(SuccessMessageMixin, LoginRequiredMixin, generic.CreateView):
    # send private message for user      
    model = Message
    form_class = MessageForm
    template_name = 'accounts/message/send_message.html'
    login_url = settings.LOGIN_URL 
    success_message = "Your message has been sent" 

    def get_context_data(self, **kwargs):
        # pass to template user-object
        context = super().get_context_data(**kwargs)                
        context['recipient'] = get_object_or_404(
            CustomUser, pk=self.kwargs['pk']).username
        return context

    def form_valid(self, form):
        form.instance.sender = self.request.user
        form.instance.recipient = get_object_or_404(CustomUser, pk=self.kwargs['pk'])        
        return super().form_valid(form)    

    def get_success_url(self):
        return reverse('accounts:profile', args=(self.kwargs['pk'],))       


class MessageListView(generic.ListView):
    # show private messages in user's profile
    template_name = 'accounts/message/messages.html'
    context_object_name = 'messages'
    paginate_by = 3

    def get_queryset(self):
        user = get_object_or_404(CustomUser, pk=self.kwargs['pk'])
        if not user == self.request.user:
            raise PermissionDenied()
        user.read_message_last_time = timezone.now()
        user.save()        
        return Message.objects.filter(recipient=self.kwargs['pk']).\
            order_by('-timestamp').select_related('sender')
        