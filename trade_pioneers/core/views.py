from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.cache import never_cache
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from .forms import CustomUserCreationForm
from .models import SearchStock
from .models import Post, Group, Comment, Like
from .forms import PostForm  
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_protect
import json
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.utils import timezone
from .forms import CommentForm  # You'll need to create a CommentForm
from django.db.models import Exists







def home(request):
    # Fetching all posts to be displayed on the homepage.
    posts = Post.objects.all().order_by('-created_at')  # Display latest post first
    return render(request, 'home.html', {'posts': posts})

def groups(request):
    # Fetching all groups for the groups page.
    groups = Group.objects.all()
    return render(request, 'groups.html', {'groups': groups})

def create_post(request):
    if request.method == 'POST':
        # Logic to create a post (you would typically use Django forms for this)
        title = request.POST.get('title')
        description = request.POST.get('description')
        group_id = request.POST.get('group')  # This should be a dropdown in your form

        # Assuming you have a user logged in (you will need user authentication logic)
        post = Post(title=title, description=description, group_id=group_id, user=request.user)
        post.save()

    # Displaying the create post form
    return render(request, 'create_post.html')

def alerts(request):
    # Fetching only posts made by 'Astro Admin'.
    posts = Post.objects.filter(user__username='Astro Admin').order_by('-created_at')
    return render(request, 'alerts.html', {'posts': posts})

def account(request):
    # Fetching account related info, assuming there's a logged-in user.
    user_posts = Post.objects.filter(user=request.user)
    user_comments = Comment.objects.filter(user=request.user)
    user_likes = Like.objects.filter(user=request.user)
    return render(request, 'account.html', {
        'user_posts': user_posts, 
        'user_comments': user_comments, 
        'user_likes': user_likes
    })


# New view function for the Startup page
def startup_page(request):
    return render(request, 'core/startup_page.html')

# New view function for the login page
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('dashboard_view')
            else:
                messages.error(request, 'Invalid username or password. Please try again.')
        else:
            messages.error(request, 'Invalid username or password. Please try again.')
    else:
        form = AuthenticationForm()
    return render(request, 'core/login.html', {'form': form})

# New view function for the Dashboard page
@never_cache
@login_required
def dashboard_view(request):
    return render(request, 'core/dashboard.html')

# New view function for the AstroBot page
@never_cache
@login_required
def astrobot_view(request):
    return render(request, 'core/astrobot.html')

# New view function for the Community Forum page
@never_cache
@login_required
def community_forum_view(request):
    return render(request, 'core/community_forum.html')

# New view function for the Real-Time Data page
@never_cache
@login_required
def real_time_data_view(request):
    return render(request, 'core/real_time_data.html')

# New view function for the Real-Time Data page
@never_cache
@login_required
def home_view(request):
    return render(request, 'core/home.html')

# New view function for the Top Picks page
@never_cache
@login_required
def top_picks_view(request):
    return render(request, 'core/top_picks.html')

# Registration View
def register(request):
    print("Register view reached.")  # Add this line for debugging
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Account created successfully! Please log in.")
            print("Form is valid.")
            return redirect('login_view')
        else:
            print("Form is invalid.")
            # Add this line to print form errors for debugging
            print(form.errors)
            # Also, print form.cleaned_data to see the data being submitted
            print(form.cleaned_data)
    else:
        form = CustomUserCreationForm()
    return render(request, 'core/registration.html', {'form': form})

# Logout View
def logout_view(request):
    logout(request)
    return redirect('/logout_page/')

def logout_page(request):
    return render(request, 'core/logout.html')

# New view function for the Community Forum Find an Astro Group page
@never_cache
@login_required
def community_forum_find_an_astro_group_view(request):
    return render(request, 'core/community_forum_find_an_astro_group.html')

# New view function for the Top Picks Home page
@never_cache
@login_required
def top_picks_home_view(request):
    return render(request, 'core/top_picks_home.html')

# New view function for the Top Picks Top Pick 1 page
@never_cache
@login_required
def top_picks_top_pick_1_view(request):
    return render(request, 'core/top_picks_top_pick_1.html')

# New view function for the Top Picks Top Pick 2 page
@never_cache
@login_required
def top_picks_top_pick_2_view(request):
    return render(request, 'core/top_picks_top_pick_2.html')
    
# New view function for the Top Picks Top Pick 3 page
@never_cache
@login_required
def top_picks_top_pick_3_view(request):
    return render(request, 'core/top_picks_top_pick_3.html')
    
# New view function for the Top Picks Top Pick 4 page
@never_cache
@login_required
def top_picks_top_pick_4_view(request):
    return render(request, 'core/top_picks_top_pick_4.html')
    
# New view function for the Top Picks Top Pick 5 page
@never_cache
@login_required
def top_picks_top_pick_5_view(request):
    return render(request, 'core/top_picks_top_pick_5.html')
    
# New view function for the Top Picks Top Pick 6 page
@never_cache
@login_required
def top_picks_top_pick_6_view(request):
    return render(request, 'core/top_picks_top_pick_6.html')
    
# New view function for the Top Picks Top Pick 7 page
@never_cache
@login_required
def top_picks_top_pick_7_view(request):
    return render(request, 'core/top_picks_top_pick_7.html')
    
# New view function for the Top Picks Top Pick 8 page
@never_cache
@login_required
def top_picks_top_pick_8_view(request):
    return render(request, 'core/top_picks_top_pick_8.html')
    
# New view function for the Top Picks Top Pick 9 page
@never_cache
@login_required
def top_picks_top_pick_9_view(request):
    return render(request, 'core/top_picks_top_pick_9.html')

# New view function for the Top Picks Top Pick 10 page
@never_cache
@login_required
def top_picks_top_pick_10_view(request):
    return render(request, 'core/top_picks_top_pick_10.html')

#Function for Search Stock database
def search(request):
    query = request.GET.get('query')
    results = SearchStock.objects.filter(name__icontains=query)
    return render(request, 'search_results.html', {'results': results})




#########################
# community forum stuff #
#########################


# Home page view
@csrf_protect
@never_cache
@login_required
def community_forum_forum_home_view(request):
    raw_posts = Post.objects.filter(deleted_at__isnull=True).order_by('-date_posted')
    
    # Add the liked status for each post
    posts = []
    for post in raw_posts:
        liked = post.like_set.filter(user=request.user).exists()
        posts.append({"post": post, "liked": liked})

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string('core/partial_community_forum_forum_home.html', {'posts': posts})
        return HttpResponse(html)
    
    return render(request, 'core/community_forum_forum_home.html', {'posts': posts})


# Groups page view
@never_cache
@login_required
def community_forum_forum_groups_view(request):
    groups = Group.objects.all().annotate(is_member=Exists(Group.users.through.objects.filter(customuser_id=request.user.id)))
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string('core/partial_community_forum_forum_groups.html', {'groups': groups})
        return HttpResponse(html)

    return render(request, 'core/community_forum_forum_groups.html', {'groups': groups})


# Post page view
@csrf_protect
@never_cache
@login_required
def community_forum_forum_post_view(request):
    if request.method == "POST":
        print("POST request received")
        form = PostForm(request.POST)
        print(form.errors)
        if form.is_valid():
            print("Form is valid")
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('community_forum_view')
        else:
            print("Form is not valid")

    else:
        form = PostForm()
    
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string('core/partial_community_forum_forum_post.html', {'form': form})
        return HttpResponse(html)

    return render(request, 'core/community_forum_forum_post.html', {'form': form})

# Alerts page view
@never_cache
@login_required
def community_forum_forum_alerts_view(request):
    alerts = Post.objects.filter(user__username="admin").order_by('-date_posted')
    print(alerts)  # This will print the QuerySet to the console

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string('core/partial_community_forum_forum_alerts.html', {'alerts': alerts})
        return HttpResponse(html)

    return render(request, 'core/community_forum_forum_alerts.html', {'alerts': alerts})

# Account page view
@never_cache
@login_required
def community_forum_forum_account_view(request):
    user_posts = Post.objects.filter(user=request.user)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        html = render_to_string('core/partial_community_forum_forum_account.html', {'user_posts': user_posts})
        return HttpResponse(html)

    return render(request, 'core/community_forum_forum_account.html', {'user_posts': user_posts})


###################
# Endpoint ########
###################


@login_required
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, deleted_at__isnull=True)  # Ensure the post isn't deleted
    
    # Get or create a Like object for the current user and post
    like, created = Like.objects.get_or_create(user=request.user, post=post)

    if created:
        # A new Like object was created, so the post was liked
        return JsonResponse({"status": "liked"})
    else:
        # A Like object already existed, so delete it to unlike the post
        like.delete()
        return JsonResponse({"status": "unliked"})

@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id, deleted_at__isnull=True)  # Ensure the post isn't deleted
    
    # Check content type to determine how to parse data
    if request.headers.get('Content-Type') == 'application/json':
        body_unicode = request.body.decode('utf-8')
        body_data = json.loads(body_unicode)
        text = body_data.get('text', '').strip()
    else:
        text = request.POST.get('text', '').strip()

    if text:
        comment = Comment.objects.create(user=request.user, post=post, text=text)
        return JsonResponse({
            "status": "comment_added",
            "content": text,
            "username": request.user.username
        })
    
    return JsonResponse({"status": "error"})

@login_required
def create_post(request):
    if request.method == "POST":
        content = request.POST.get('content', '').strip()
        group_id = request.POST.get('group_id', None)  # assuming you have group associated with the post
        if content:
            # Here you'd probably want some validation, e.g. if the group exists, etc.
            group = get_object_or_404(Group, id=group_id)  # assuming CustomGroup is the name of your group model
            post = Post.objects.create(user=request.user, group=group, content=content)
            return JsonResponse({"status": "post_created", "post_id": post.id})
        return JsonResponse({"status": "error"})

    # If you want to also support getting a form for creating a post:
    return render(request, 'core/community_forum_forum_post.html')

@login_required
def get_post(request, post_id):
    post = get_object_or_404(Post, id=post_id, deleted_at__isnull=True)  # Ensure the post isn't deleted
    context = {"post": post}
    return render(request, 'core/community_forum_forum_account.html', context)

@login_required
def list_posts(request):
    user_groups = request.user.custom_groups.all()
    posts = Post.objects.filter(group__in=user_groups, deleted_at__isnull=True).order_by('-date_posted')
    context = {"posts": posts}
    return render(request, 'core/community_forum_forum_account.html', context)

@login_required
def delete_post(request, post_id):
    if request.method != "POST":
        return JsonResponse({"status": "error", "message": "Invalid request method."}, status=405)

    post = get_object_or_404(Post, id=post_id, deleted_at__isnull=True)  # Ensure the post isn't deleted
    
    if post.user != request.user:
        return JsonResponse({"status": "error", "message": "You're not authorized to delete this post."}, status=403)

    post.deleted_at = timezone.now()  # Soft delete
    post.save()

    return JsonResponse({"status": "post_deleted"})

@login_required
def delete_comment(request, comment_id):
    if request.method != "POST":
        return JsonResponse({"status": "error", "message": "Invalid request method."}, status=405)

    comment = get_object_or_404(Comment, id=comment_id, deleted_at__isnull=True)  # Ensure the comment isn't deleted
    
    if comment.user != request.user:
        return JsonResponse({"status": "error", "message": "You're not authorized to delete this comment."}, status=403)

    comment.deleted_at = timezone.now()  # Soft delete
    comment.save()

    return JsonResponse({"status": "comment_deleted"})

@login_required
def edit_comment(request, comment_id):
    if request.method == 'POST':
        comment = get_object_or_404(Comment, id=comment_id, deleted_at__isnull=True)

        if comment.user == request.user:
            comment.text = request.POST.get('text')
            comment.save()
            return JsonResponse({"status": "comment_edited", "text": comment.text})
        else:
            return JsonResponse({"status": "error", "message": "You're not authorized to edit this comment."}, status=403)

    return JsonResponse({"status": "error", "message": "Invalid request method."}, status=405) 

@login_required
def edit_post(request, post_id):
    if request.method == 'POST':
        post = Post.objects.get(pk=post_id)
        
        # get data from request
        title = request.POST['title']
        description = request.POST['description']
        
        # save the edited post details
        post.title = title
        post.description = description
        post.save()

        return JsonResponse({
            'status': 'post_edited',
            'title': title,
            'description': description
        })
    return JsonResponse({'status': 'error'})

@login_required
def join_group(request):
    if request.method == "POST":
        group_id = request.POST.get('group_id')
        group = get_object_or_404(Group, id=group_id)
        
        # Add the user to the group's members
        group.users.add(request.user)
        group.save()

        return JsonResponse({"status": "joined"})

    return JsonResponse({"status": "error"})

@login_required
def leave_group(request):
    if request.method == "POST":
        group_id = request.POST.get('group_id')
        group = get_object_or_404(Group, id=group_id)
        
        # Remove the user from the group's members
        group.users.remove(request.user)
        group.save()

        return JsonResponse({"status": "left"})

    return JsonResponse({"status": "error"})

@login_required
def get_group_posts(request):
    group_id = request.GET.get('group_id')
    group = get_object_or_404(Group, id=group_id)
    posts = group.post_set.all()

    return render(request, 'core/group_posts.html', {'posts': posts})

from django.http import JsonResponse

@login_required
def edit_info(request):
    if request.method == 'POST':
        # ... (rest of your code to update user info)
        return JsonResponse({'status': 'success', 'message': 'Your account information has been updated!'})
    return JsonResponse({'status': 'error', 'message': 'Invalid request method'})

from .forms import CustomUserUpdateForm

@login_required
def update_account(request):
    if request.method == 'POST':
        form = CustomUserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            user = form.save()
            # Send back the updated user data
            return JsonResponse({
                'status': 'success', 
                'message': 'Your account has been updated!',
                'user': {
                    'username': user.username,
                    'email': user.email,
                    'first_name': user.first_name,
                    'last_name': user.last_name
                }
            })
        else:
            # Form is invalid, return error messages
            error_messages = {field: errors for field, errors in form.errors.items()}
            return JsonResponse({'status': 'error', 'errors': error_messages}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

@login_required
def user_interactions(request):
    interaction = request.GET.get('interaction', 'posts')

    if interaction == 'posts':
        data = {'user_posts': request.user.posts.all()}
    elif interaction == 'comments':
        data = {'user_comments': request.user.comments.all()}
    elif interaction == 'likes':
        data = {'user_likes': request.user.likes.all()}
    else:
        data = {'user_posts': request.user.posts.all()}  # Default to posts

    return render(request, 'my_interactions.html', data)

@login_required
def get_user_posts(request):
    posts = [{
        'content': post.description, 
        'title': post.title, 
        'date_posted': post.date_posted
    } for post in request.user.posts.all()]
    return JsonResponse(posts, safe=False)

@login_required
def get_user_comments(request):
    comments = [{
        'content': comment.text,  # Ensure this matches the field name in your Comment model
        'post_title': comment.post.title,  # Use the related Post's title
        'date_commented': comment.date_commented
    } for comment in request.user.comments.all()]
    return JsonResponse(comments, safe=False)

@login_required
def get_user_likes(request):
    likes = [{
        'post_title': like.post.title,  # Use the related Post's title
        'created_at': like.created_at
    } for like in request.user.likes.all()]
    return JsonResponse(likes, safe=False)