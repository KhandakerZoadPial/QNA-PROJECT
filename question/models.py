from django.db import models
from django.contrib.auth.models import User


class Question(models.Model):
    asked_by = models.ForeignKey(User, on_delete=models.CASCADE)
    the_question = models.TextField()
    asked_when = models.DateTimeField(auto_now_add=True)
    question_category = models.CharField(max_length=30)
    is_anonymous = models.BooleanField(default=False)

    def __str__(self):
        return self.the_question


class Sub_question(models.Model):
    main_question = models.ForeignKey(Question, on_delete=models.CASCADE)
    the_sub_question = models.TextField()
    is_answered = models.BooleanField(default=False)


class Answer(models.Model):
    answered_by = models.ForeignKey(User, on_delete=models.CASCADE)
    answer_of = models.ForeignKey(Question, on_delete=models.CASCADE, blank=True,
                                  null=True, related_name="main")
    answer_of_sub = models.ForeignKey(Sub_question, on_delete=models.CASCADE, blank=True,
                                      null=True, related_name="sub")
    the_answer = models.TextField()
    answered_when = models.DateTimeField(auto_now_add=True)
    is_anonymous = models.BooleanField(default=False)
 
    upvoted_user = models.ManyToManyField(User, related_name='upvotedUser', blank=True)
    downvoted_user = models.ManyToManyField(User, related_name='downvotedUser', blank=True)

    @classmethod
    def upvoted(cls, question, upvoted_user):
        obj = cls.objects.get(answer_of=question)
        obj.upvoted_user.add(upvoted_user)

    @classmethod
    def rmv_upvote(cls, question, upvoted_user):
        obj = cls.objects.get(answer_of=question)
        obj.upvoted_user.remove(upvoted_user)

    @classmethod
    def downvoted(cls, question, downvoted_user):
        obj = cls.objects.get(answer_of=question)
        obj.downvoted_user.add(downvoted_user)

    @classmethod
    def rmv_downvote(cls, question, downvoted_user):
        obj = cls.objects.get(answer_of=question)
        obj.downvoted_user.remove(downvoted_user)


    def __str__(self):
        return self.the_answer


class User_Profile(models.Model):
    the_user = models.OneToOneField(
        User, related_name="the_user_profile", on_delete=models.CASCADE)
    is_verified = models.BooleanField(default=False)
    profession = models.CharField(max_length=15, null=True, blank=True)
    short_bio = models.CharField(max_length=200, null=True, blank=True)
    knows_about = models.TextField(null=True, blank=True)


class category(models.Model):
    cat = models.CharField(max_length=30)