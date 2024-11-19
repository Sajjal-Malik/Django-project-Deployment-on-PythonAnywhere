from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Post, Comment
from .forms import PostForm, CommentForm
from django.http import HttpResponseForbidden
import markdown as md

# List of posts
def post_list(request):
    # Fetch all posts that have been published
    posts = Post.objects.filter(
        published_date__lte=timezone.now()).order_by('-published_date')
    
    # Convert post content from markdown to HTML
    for post in posts:
        post.text = md.markdown(post.text)
    
    # Render the posts in 'post_list.html'
    return render(request, 'blog/post_list.html', {'posts': posts})

# Detail view of a single post
def post_detail(request, pk):
    # Get the specific post by primary key (id)
    post = get_object_or_404(Post, pk=pk)
    
    # Convert post content from markdown to HTML
    post.text = md.markdown(post.text)
    
    # Fetch all comments related to this post
    comments = post.comments.all()
    
    # Render the post and its comments in 'post_detail.html'
    return render(request, 'blog/post_detail.html', {'post': post, 'comments': comments})

# Create a new post
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            # Redirect to the detail view of the newly created post
            return redirect('blog:post_detail', pk=post.pk)
    else:
        form = PostForm()
    
    # Render the form for creating a new post
    return render(request, 'blog/post_edit.html', {'form': form})

# Edit an existing post
def post_edit(request, pk):
    # Fetch the post to be edited
    post = get_object_or_404(Post, pk=pk)
    
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            # Redirect to the detail view of the updated post
            return redirect('blog:post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    
    # Render the form for editing the post
    return render(request, 'blog/post_edit.html', {'form': form})

# Delete a post
def post_delete(request, pk):
    # Fetch the post to be deleted
    post = get_object_or_404(Post, pk=pk)
    # Check if the logged-in user is the author of the post
    if post.author != request.user:
        # Return a 403 Forbidden response if the user is not the author
        return HttpResponseForbidden("You are not allowed to delete this post.")
    
    # Delete the post and redirect to the post list
    post.delete()
    return redirect('blog:post_list')

# Add a comment to a post
def add_comment(request, pk):
    # Fetch the post to which a comment is being added
    post = get_object_or_404(Post, pk=pk)
    
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user
            comment.save()
            # Redirect to the detail view of the post after adding the comment
            return redirect('blog:post_detail', pk=post.pk)
    else:
        form = CommentForm()
    
    # Render the form for adding a comment
    return render(request, 'blog/add_comment.html', {'form': form})
