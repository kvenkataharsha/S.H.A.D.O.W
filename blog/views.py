from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse, Http404
from django.contrib.auth.decorators import login_required
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView
)
from .models import Post, Comment, registerCamera, City, Country
from .forms import CommentForm, CameraForm
from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status



def linkgraph(request):
    context = {}
    return render(request, 'blog/linktographs.html', context)

def indianmap(request):
    context={}
    return render(request, 'blog/D3india.html', context)

def linegraph(request):
    return render(request, 'blog/linegraph.html', {})

def piechart(request):
    return render(request, 'blog/pie.html',{})

def donut(request):
    return render(request, 'blog/donut.html',{})

def home(request):
    context = {
        'posts': Post.objects.all()
    }
    return render(request, 'blog/home.html', context)

def landing_page(request):
    return render(request,'blog/index.html')


class PostListView(ListView):
    model = Post
    template_name = 'blog/home.html'
    context_object_name = 'posts'
    ordering = ['-date_posted']


class PostDetailView(DetailView):
    model = Post
    # is_liked = False

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     post = context['post']
    #     if post.likes.filter(id=self.request.user.id).exists():
    #         context['is_liked'] = True
    #     return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Post
    fields = ['title', 'location', 'pincode', 'country', 'city',
              'state',  'content', 'crimetype', 'photo1', 'photo2', 'photo3', 'photo4']

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.fields['city'].queryset = City.objects.none()

    #     if 'country' in self.data:
    #         try:
    #             country_id = int(self.data.get('country'))
    #             self.fields['city'].queryset = City.objects.filter(
    #                 country_id=country_id).order_by('name')
    #         except (ValueError, TypeError):
    #             pass  # invalid input from the client; ignore and fallback to empty City queryset
    #     elif self.instance.pk:
    #         self.fields['city'].queryset = self.instance.country.city_set.order_by(
    #             'name')

    def form_valid(self, form):
        form.instance.author = self.request.user
        return super().form_valid(form)


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Post
    fields = ['title', 'location', 'pincode', 'city',
              'state', 'country', 'content', 'crimetype', 'photo1', 'photo2', 'photo3', 'photo4']

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
    success_url = '/blog/home'

    def test_func(self):
        post = self.get_object()
        if self.request.user == post.author:
            return True
        return False


@login_required
def RegisterCamera(request):
    # cam = get_object_or_404(registerCamera)
    # if request.method == "POST":
        # form = CameraForm(request.POST)
        #     if form.is_valid():
        #         camera = form.save(commit=False)
        #         camera.cam = cam
        #         camera.author = request.user
        #         camera.save()
        #         return redirect('blog-home')
        # else:
        #     form = CameraForm()
        # return render(request, 'blog/registerCamera.html', {'form': form})
    form = CameraForm(request.POST)
    if form.is_valid():
        form.save()
    context = {
        'form': form,
    }
    return render(request, 'blog/registerCamera.html', context)


@login_required
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            return redirect('post-detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form})


@login_required
def comment_approve(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.approve()
    return redirect('post-detail', pk=comment.post.pk)


@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if comment.author == request.user:
        comment.delete()
        return redirect('post-detail', pk=comment.post.pk)


is_upvoted = False
is_downvoted = False


@login_required
def upvote_post(request):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))
    if post.upvotes.filter(id=request.user.id).exists():
        post.upvotes.remove(request.user)
        is_upvoted = False
    else:
        post.upvotes.add(request.user)
        post.downvotes.remove(request.user)
        is_downvoted = False
        is_upvoted = True

    context = {
        'post': post,
        'is_upvoted': is_upvoted,
        'total_upvotes': post.total_upvotes(),
    }
    if request.is_ajax():
        html = render_to_string(
            'blog/upvotepost_section.html', context, request=request)
        return JsonResponse({'form': html})
    return redirect(post.get_absolute_url())


@login_required
def downvote_post(request):
    post = get_object_or_404(Post, id=request.POST.get('post_id'))

    # is_downvoted = False
    if post.downvotes.filter(id=request.user.id).exists():
        post.downvotes.remove(request.user)
        is_downvoted = False
    else:
        post.downvotes.add(request.user)
        post.upvotes.remove(request.user)
        is_upvoted = False
        is_downvoted = True

    context = {
        'post': post,
        'is_downvoted': is_downvoted,
        'total_downvotes': post.total_downvotes(),
    }
    if request.is_ajax():
        html = render_to_string(
            'blog/downvotepost_section.html', context, request=request)
        return JsonResponse({'form': html})
    return redirect(post.get_absolute_url())



def cameraslist(request):
    context = {
        'cameras': registerCamera.objects.all()
    }
    return render(request, 'blog/cameralist.html', context)


def load_cities(request):
    country_id = request.GET.get('country')
    cities = City.objects.filter(country_id=country_id).order_by('name')
    return render(request, 'blog/city_dropdown_list_options.html', {'cities': cities})


# Create your views here.

class post_rest(APIView):

    def get(self,request):

        data=Post.objects.all()
        list1=[]
        for each in data:
            var={
                'title':each.title,
                'location':each.location,
                'content':each.content,
                'crimetype':each.crimetype,
                'state':each.state,
                'city':each.city
            }
            list1.append(var)
        return Response(list1)
