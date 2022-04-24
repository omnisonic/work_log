from django.shortcuts import render, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.models import User
from django.db.models import Sum

from django.views.generic import (
    ListView, 
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    )

from django.views.generic.dates import MonthArchiveView

from .models import Post
# from django.http import HttpResponse
    
def home(request):
    context = {
        'posts': Post.objects.all()
    }

    return render(request, 'blog/home.html', context)

class PostListView(LoginRequiredMixin, ListView):  #added LoginRequiredMixin to make login required
    model = Post
    template_name = 'blog/home.html' # <app>/<model>_<veiwtype.html>
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

# month, from documentation
class PostMonthArchiveView(LoginRequiredMixin, MonthArchiveView):
    queryset = Post.objects.all()
    date_field = "date_posted"
    allow_future = False

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')
    
# https://stackoverflow.com/questions/42696048/get-queryset-in-montharchiveview-returns-all-objects-instead-objects-created-o

    def get_context_data(self, *args, **kwargs,):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        context = super().get_context_data( **kwargs)
        month = self.get_month()
        context['total_hours'] = self.queryset.filter(author=user).filter(date_posted__month=month).aggregate(Sum('hours_worked')).get('hours_worked__sum')
        # context['total_hours'] = self.queryset.filter(author=self.request.user).filter(date_posted__month=month).aggregate(Sum('hours_worked')).get('hours_worked__sum')
        return context


class UserPostListView(LoginRequiredMixin, ListView, MonthArchiveView): #added LoginRequiredMixin to make login required
    model = Post
    template_name = 'blog/user_posts.html' # <app>/<model>_<veiwtype.html>
    context_object_name = 'posts'
    ordering = ['-date_posted']
    paginate_by = 5

    def get_queryset(self):
        user = get_object_or_404(User, username=self.kwargs.get('username'))
        return Post.objects.filter(author=user).order_by('-date_posted')

class PostDetailView(DetailView):
    model = Post

class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title','content','hours_worked','screen_shot' ]
    # fields = ['title', 'content','hours_worked','screen_shot' ]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)




class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['date_posted', 'content',]

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)
    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False

class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Post 
    success_url = '/'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True 
        return False

def about(request):
    return render(request, 'blog/about.html', {'title':'About'})



# class Hours(MonthArchiveView):

#     def get(self, *args, **kwargs):
#        sum_a = Post.objects.aggregate(Sum('hours_worked')).filter(user=self.request.user)

#        context = {
#            'sum_a':sum_a,

#        }
#        return render(self.request, 'post_archive_month.html', context)