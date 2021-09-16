from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('answer/<int:question_obj>', views.answer_question, name='answer'),
    path('del/a/<int:question_obj>', views.delete_a_question, name="delete_a_question"),
    path('del/b/<int:question_obj>', views.delete_an_answer, name="delete_an_answer"),
    path('answer_sub/<int:sub_question_obj>', views.answer_sub_question, name='sub_question'),
    path('profile/<int:user_id>', views.profile_handler, name='profile_handler'),
    path('uv/<int:answer_id>', views.up_vote, name='up_vote'),
    path('dv/<int:answer_id>', views.down_vote, name='down_vote'),
    path('q', views.search, name='search'),
    path('q/<int:cat_id>', views.search2, name='search2')
]

