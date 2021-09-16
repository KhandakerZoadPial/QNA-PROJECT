from django.shortcuts import redirect, render, HttpResponse
from .models import Question, Answer, Sub_question, User_Profile, category as c
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import enchant


def home(request):
    questions_set = Question.objects.all().order_by('-asked_when')
    if request.method == 'POST':
        the_question = request.POST.get('the_question')

        if sentence_tester(the_question):
            pass
        else:
            messages.error(request, 'Please try asking a meaningful question!')
            return redirect('/')

        category = request.POST.get('category')
        if category == 'Select Category':
            messages.error(request, "Please select a category properly!")
            return redirect('/')

        is_ann = request.POST.get('is_ann')
        if is_ann == 'on':
            is_ann = True
        else:
            is_ann = False


        if((the_question.strip())):
            obj = Question(asked_by=request.user, the_question=the_question, question_category=category, is_anonymous=is_ann)
            obj.save()
            return render(request, 'question/home.html', {'questions_set': questions_set})
        else:
            messages.error(request, "A question can't be empty")
            return redirect('/')
    elif request.method == 'GET':
        # dy#j9CF=
        cats = c.objects.all()
        return render(request, 'question/home.html', {'questions_set': questions_set, 'cats': cats})


def answer_question(request, question_obj):
    user_ = request.user
    if request.method == 'GET':
        try:
            answered = []
            unanswered = []
            the_question = Question.objects.get(pk=question_obj)
            other_answers = Answer.objects.filter(answer_of=the_question).order_by('-answered_when')
            if user_ == the_question.asked_by:
                if Sub_question.objects.filter(main_question=the_question).count() == 0:
                    pass
                else:
                    temp = Sub_question.objects.filter(main_question=the_question)
                    for item in temp:
                        if item.is_answered:
                            answered.append(item)
                        else:
                            unanswered.append(item)
            else:
                temp = Sub_question.objects.filter(main_question=the_question)
                for item in temp:
                    if item.is_answered:
                        answered.append(item)
            cats = c.objects.all()
            return render(request, 'question/answer_page.html', {'the_question': the_question, 'other_answers': other_answers, 'answered': answered, 'unanswered': unanswered, 'cats': cats})
        except:
            messages.error(request, 'The question does not exist!')
            return redirect('/')


    elif request.method == 'POST':
        the_answer = request.POST.get('answer')
        if the_answer == '':
            messages.error(request, "Your answer can't be empty")
            return redirect(f'/answer/{question_obj}')
        try:
            the_question = Question.objects.get(pk=question_obj)
            is_ann = request.POST.get('is_ann')
            if is_ann == 'on':
                is_ann = True
            else:
                is_ann = False
            obj = Answer(answered_by=request.user, answer_of=the_question, the_answer=the_answer, is_anonymous=is_ann)
            obj.save()
            return redirect(f'/answer/{question_obj}')
        except:
            messages.error(request, 'The question does not exist!')
            return redirect('/')


def delete_a_question(request, question_obj):
    pass


def delete_an_answer(request, answer_obj):
    pass


def answer_sub_question(request, sub_question_obj):
    try:
        sub_question_obj = Sub_question.objects.get(pk=sub_question_obj)
    except:
        messages.error(request, 'The question does not exist!')
        return redirect('/')
    
    if request.method == 'GET':
        if request.user == sub_question_obj.main_question.asked_by:
            if Answer.objects.filter(answer_of_sub=sub_question_obj).count() > 0:
                answer = Answer.objects.get(answer_of_sub=sub_question_obj)
                return render(request, 'question/sub_answer.html', {'the_question': sub_question_obj, 'flag': False, 'the_answer': answer})
            else:
                return render(request, 'question/sub_answer.html', {'the_question': sub_question_obj, 'flag': True})
        else:
            answer = Answer.objects.filter(answer_of_sub=sub_question_obj)[0]
            return render(request, 'question/sub_answer.html', {'the_question': sub_question_obj, 'flag': False, 'the_answer': answer})
    elif request.method == 'POST':
        the_answer = request.POST.get('answer')
        obj = Answer(answered_by=request.user, answer_of_sub=sub_question_obj, the_answer=the_answer)
        obj.save()
        sub_question_obj.is_answered = True
        sub_question_obj.save()
        return redirect(f'/answer/{sub_question_obj.main_question.pk}')


def profile_handler(request, user_id):
    try:
        profile_owner_user = User.objects.get(pk=user_id)
        if User_Profile.objects.filter(the_user=profile_owner_user).count() > 0:
            pass
        else:
            obj = User_Profile(the_user=profile_owner_user)
            obj.save()
        obj = User_Profile.objects.get(the_user=profile_owner_user)

        qs = Question.objects.filter(asked_by=profile_owner_user).count()
        ans = Answer.objects.filter(answered_by=profile_owner_user).count()
        
        temp = {
            'qs': qs,
            'ans': ans
        }
        cats = c.objects.all()
        return render(request, 'question/profile.html', {'profile_info': obj, 'temp': temp, 'cats': cats})
    except:
        messages.error(request, 'Something went wrong')
        return redirect('/')


def edit_profile(request, profile_id):
    pass


@login_required()
def up_vote(request, answer_id):
    if Answer.objects.filter(pk=answer_id).count() > 0:
        try:
            the_question_object = Answer.objects.get(pk=answer_id)
            the_question_object = the_question_object.answer_of
        except:
            messages.error(request, 'Something went wrong')
            return redirect('/')


        if Answer.objects.filter(pk=answer_id, upvoted_user=request.user).count() > 0:
            # Upvote already exists
            obj = Answer.objects.get(pk=answer_id)
            obj.rmv_upvote(the_question_object, request.user, answer_id)
            obj.save()
            return redirect(f'/answer/{the_question_object.pk}') # return to the same page
        else:
            obj = Answer.objects.get(pk=answer_id)
            if Answer.objects.filter(pk=answer_id, downvoted_user=request.user):
                # downvote already exists
                obj.rmv_downvote(the_question_object, request.user, answer_id)
                obj.save()
            obj.upvoted(the_question_object, request.user, answer_id)
            obj.save()
            return redirect(f'/answer/{the_question_object.pk}') # return to the same page
    else:
        messages.error(request, 'The Answer does not exist')
        return redirect('/')


@login_required()
def down_vote(request, answer_id):
    if Answer.objects.filter(pk=answer_id).count() > 0:
        try:
            the_question_object = Answer.objects.get(pk=answer_id)
            the_question_object = the_question_object.answer_of
        except:
            messages.error(request, 'Something went wrong')
            return redirect('/')


        if Answer.objects.filter(pk=answer_id, downvoted_user=request.user).count() > 0:
            # Downvote already exists
            obj = Answer.objects.get(pk=answer_id)
            obj.rmv_downvote(the_question_object, request.user, answer_id)
            obj.save()
            return redirect(f'/answer/{the_question_object.pk}')# return to the same page
        else:
            obj = Answer.objects.get(pk=answer_id)
            if Answer.objects.filter(pk=answer_id, upvoted_user=request.user).count() > 0:
                # downvote already exists
                obj.rmv_upvote(the_question_object, request.user, answer_id)
                obj.save()
            obj.downvoted(the_question_object, request.user, answer_id)
            obj.save()
            return redirect(f'/answer/{the_question_object.pk}') # return to the same page
    else:
        messages.error(request, 'The Answer does not exist')
        return redirect('/')


def search(request):
    container = []
    if request.method == 'POST':
        query = request.POST.get('search')
        if query.isspace() or query =='':
            messages.error(request, 'Query can not be empty')
            return redirect('/')
        query_list = query.split(' ')
        ignore_list = ['what', 'how', 'when', 'who', 'where', 'if', 'then']
        for q in query_list:
            if q.lower() in ignore_list:
                query_list.pop(q)
        for q in query_list:
            temp = Question.objects.filter(the_question__contains=q)
            for item in temp:
                if item not in container:
                    container.append(item)
    else:
        messages.error(request, 'Please put your query in the search box!')
        return redirect('/')
    cats = c.objects.all()
    return render(request, 'question/search.html', {'results': container, 'cats': cats})


def search2(request, cat_id):
    container = []
    query = c.objects.get(pk=cat_id)
    query = query.cat
    
    # query_list = query.split(' ')
    # ignore_list = ['what', 'how', 'when', 'who', 'where', 'if', 'then']
    # for q in query_list:
    #     if q.lower() in ignore_list:
    #         query_list.pop(q)
    # for q in query_list:
    #     temp = Question.objects.filter(the_question__contains=q)
    #     for item in temp:
    #         if item not in container:
    #             container.append(item)

    results = Question.objects.filter(question_category=query)

    cats = c.objects.all()
    return render(request, 'question/search.html', {'results': results, 'cats': cats})


d = enchant.Dict("en_US")
def sentence_tester(sentence):
    sentence = sentence.split(' ')
    count = 0
    for word in sentence:
        if d.check(word):
            count+=1

    if count >=2:
        return True
    
    return False