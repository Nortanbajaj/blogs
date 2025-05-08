from django.shortcuts import render, get_object_or_404, redirect
from .models import Blog
from .forms import BlogForm, CommentForm
# from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required

def blog_list(request):
    blogs = Blog.objects.all()
    return render(request, 'blog_list.html', {'blogs': blogs})

@login_required
def blog_detail(request, pk):
    blog = get_object_or_404(Blog, pk=pk)
    comments = blog.comments.all()
    if request.method == 'POST':
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.blog = blog
            comment.author = request.user
            comment.save()
            return redirect('blog_detail', pk=blog.pk)
    else:
        comment_form = CommentForm()
    return render(request, 'blog_detail.html', {'blog': blog, 'comments': comments, 'comment_form': comment_form})

@login_required
def create_blog(request):
    if request.method == 'POST':
        form = BlogForm(request.POST ,request.FILES)
        if form.is_valid():
            blog = form.save(commit=False)
            blog.author = request.user
            blog.save()
            return redirect('blog_list')
    else:
        form = BlogForm()
    return render(request, 'create_blog.html', {'form': form})

# def custom_logout_view(request):
#     logout(request)
#     return redirect('accounts/login/')




def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Redirect to login page after successful signup
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})
