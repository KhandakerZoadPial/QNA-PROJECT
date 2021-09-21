from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('answer/<int:question_obj>', views.answer_question, name='answer'),
    path('answer_sub/<int:sub_question_obj>', views.answer_sub_question, name='sub_question'),
    path('profile/<int:user_id>', views.profile_handler, name='profile_handler'),
    path('profile/<int:profile_id>/edit', views.edit_profile, name='edit_profile'),
    path('uv/<int:answer_id>', views.up_vote, name='up_vote'),
    path('dv/<int:answer_id>', views.down_vote, name='down_vote'),
    path('q', views.search, name='search'),
    path('q/<int:cat_id>', views.search2, name='search2'),
    path('et/<int:answer_id>', views.question_edit, name='question_edit'),
    path('all', views.all_questins, name='all'),
    path('more', views.about_us, name='about_us'),
    path('privacy', views.about_us, name='about_us'),
    path('terms', views.about_us, name='about_us')
]

