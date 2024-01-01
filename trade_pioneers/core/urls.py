from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.startup_page, name='startup_page'),
    path('login/', views.login_view, name='login_view'),
    path('dashboard/', views.dashboard_view, name='dashboard_view'),
    path('astrobot/', views.astrobot_view, name='astrobot_view'),
    path('community_forum/', views.community_forum_view, name='community_forum_view'),
    path('real_time_data/', views.real_time_data_view, name='real_time_data_view'),
    path('top_picks/', views.top_picks_view, name='top_picks_view'),
    path('logout/', views.logout_view, name='logout_view'),  # Logout process
    path('logout_page/', views.logout_page, name='logout_page'),  # Logout confirmation page
    path('register/', views.register, name='register'),
    path('community_forum_find_an_astro_group/', views.community_forum_find_an_astro_group_view, name='community_forum_find_an_astro_group_view'),
    path('top_picks_home/', views.top_picks_home_view, name='top_picks_home_view'),
    path('top_picks_top_pick_1/', views.top_picks_top_pick_1_view, name='top_picks_top_pick_1_view'),
    path('top_picks_top_pick_2/', views.top_picks_top_pick_2_view, name='top_picks_top_pick_2_view'),
    path('top_picks_top_pick_3/', views.top_picks_top_pick_3_view, name='top_picks_top_pick_3_view'),
    path('top_picks_top_pick_4/', views.top_picks_top_pick_4_view, name='top_picks_top_pick_4_view'),
    path('top_picks_top_pick_5/', views.top_picks_top_pick_5_view, name='top_picks_top_pick_5_view'),
    path('top_picks_top_pick_6/', views.top_picks_top_pick_6_view, name='top_picks_top_pick_6_view'),
    path('top_picks_top_pick_7/', views.top_picks_top_pick_7_view, name='top_picks_top_pick_7_view'),
    path('top_picks_top_pick_8/', views.top_picks_top_pick_8_view, name='top_picks_top_pick_8_view'),
    path('top_picks_top_pick_9/', views.top_picks_top_pick_9_view, name='top_picks_top_pick_9_view'),
    path('top_picks_top_pick_10/', views.top_picks_top_pick_10_view, name='top_picks_top_pick_10_view'),

    path('community_forum_forum_home/', views.community_forum_forum_home_view, name='community_forum_forum_home_view'),
    path('community_forum_forum_groups/', views.community_forum_forum_groups_view, name='groups'),
    path('community_forum_forum_post/', views.community_forum_forum_post_view, name='community_forum_forum_post_view'),
    path('community_forum_forum_alerts/', views.community_forum_forum_alerts_view, name='alerts'),
    path('community_forum_forum_account/', views.community_forum_forum_account_view, name='account'),



###############
# Endpoint#####
###############
    path('like_post/<int:post_id>/', views.like_post, name='like_post'),
    path('add_comment/<int:post_id>/', views.add_comment, name='add_comment'),
    path('create_post/', views.create_post, name='create_post'),
    path('get_post/<int:post_id>/', views.get_post, name='get_post'),
    path('list_posts/', views.list_posts, name='list_posts'),
    path('post/<int:post_id>/delete/', views.delete_post, name='delete_post'),
    path('comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
    path('comment/<int:comment_id>/edit/', views.edit_comment, name='edit_comment'),
    path('post/<int:post_id>/edit/', views.edit_post, name='edit_post'),
    path('join-group/', views.join_group, name='join-group'),
    path('leave-group/', views.leave_group, name='leave-group'),
    path('get-group-posts/', views.get_group_posts, name='get-group-posts'),
    path('account/edit/', views.edit_info, name='edit_info'),
    path('account/update/', views.update_account, name='update_account'),
    path('interactions/posts/', views.get_user_posts, name='user-posts'),
    path('interactions/comments/', views.get_user_comments, name='user-comments'),
    path('interactions/likes/', views.get_user_likes, name='user-likes'),




]
    

