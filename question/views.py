from django.shortcuts import redirect, render, HttpResponse
from .models import Question, Answer, Sub_question, User_Profile,fun as f, category as c
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
import enchant
from django.core.paginator import Paginator


def home(request):
    try:
        fun = f.objects.get(pk=1)
        fun.total = fun.total+1
        fun.save()
    except:
        pass

    questions_set = Question.objects.all().order_by('-asked_when')
    cats = c.objects.all()
    if request.method == 'POST' and request.user.is_authenticated:
        the_question = request.POST.get('the_question')
        if not the_question.strip():
            messages.error(request, 'Question can not be empty')
            return redirect('/')
        category = request.POST.get('category')

        if sentence_tester(the_question):
            pass
        else:
            messages.error(request, 'Please try asking a meaningful question!')
            return redirect('/')

        
        if category == 'Select Category':
            messages.error(request, "Please select a category properly!")
            return render(request, 'question/home.html', {'data': the_question, 'cats': cats, 'fun': fun})

        is_ann = request.POST.get('is_ann')
        if is_ann == 'on':
            is_ann = True
        else:
            is_ann = False
        try:
            category = c.objects.get(cat=category)
        except:
            pass
        if the_question.strip():
            obj = Question(asked_by=request.user, the_question=the_question,
                           question_category=category, is_anonymous=is_ann)
            obj.save()
            messages.error(request, "Successfully added the question!")
            return render(request, 'question/home.html', {'questions_set': questions_set, 'cats': cats, 'fun': fun})
        else:
            messages.error(request, "A question can't be empty")
            return redirect('/')
    elif request.method == 'GET':
        # dy#j9CF=
        p = Paginator(questions_set, 10)
        page_number = request.GET.get('page')
        page_obj = p.get_page(page_number)

        return render(request, 'question/home.html', {'questions_set': page_obj, 'cats': cats, 'fun': fun})
    else:
        return redirect('/accounts/login')


@login_required()
def answer_question(request, question_obj):
    user_ = request.user
    if request.method == 'GET':
        try:
            answered = []
            unanswered = []
            the_question = Question.objects.get(pk=question_obj)
            other_answers = Answer.objects.filter(
                answer_of=the_question).order_by('-answered_when')
            if user_ == the_question.asked_by:
                if Sub_question.objects.filter(main_question=the_question).count() == 0:
                    pass
                else:
                    temp = Sub_question.objects.filter(
                        main_question=the_question)
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
            obj = Answer(answered_by=request.user, answer_of=the_question,
                         the_answer=the_answer, is_anonymous=is_ann)
            obj.save()
            return redirect(f'/answer/{question_obj}')
        except:
            messages.error(request, 'The question does not exist!')
            return redirect('/')


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
        obj = Answer(answered_by=request.user,
                     answer_of_sub=sub_question_obj, the_answer=the_answer)
        obj.save()
        sub_question_obj.is_answered = True
        sub_question_obj.save()
        return redirect(f'/answer/{sub_question_obj.main_question.pk}')


def rating_calulator(number):
    if number > 0.0 and number<= 10.0:
        return 4.0
    elif number >10.0 and number<=20.0:
        return 8.0
    elif number >= 30.0:
        return 10.0
    return 0.0


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
        rat_num = rating_calulator(qs)
        print(rat_num)
        obj.rating = rat_num
        obj.save()

        temp = {
            'qs': qs,
            'ans': ans
        }
        
        if profile_owner_user == request.user:
            users_questions = Question.objects.filter(
                asked_by=profile_owner_user, is_anonymous=False)
        else:
            users_questions = Question.objects.filter(
                asked_by=profile_owner_user)
        cats = c.objects.all()
        
        return render(request, 'question/profile.html', {'profile_info': obj, 'temp': temp, 'questions_set': users_questions,'cats': cats})
    except:
        messages.error(request, 'Something went wrong')
        return redirect('/')




@login_required()
def edit_profile(request, profile_id):
    cats = c.objects.all()
    if request.method == 'POST':
        profile_obj = User_Profile.objects.filter(pk=profile_id)
        if profile_obj.count() > 0:
            if request.user == profile_obj[0].the_user:
                prof = request.POST.get('prof', '')
                bio = request.POST.get('bio', '')
                knows = request.POST.get('knows', '')
                profile_obj = profile_obj[0]
                profile_obj.profession = prof
                profile_obj.short_bio = bio
                profile_obj.knows_about = knows
                profile_obj.save()
                messages.success(request, 'Successfully updated info!')
                return redirect(f'/profile/{profile_obj.the_user.pk}')
            else:
                messages.error(request, 'Something went wrong')
                return redirect('/')
        else:
            messages.error(request, 'Something went wrong')
            return redirect('/')
    else:
        profile_obj = User_Profile.objects.filter(pk=profile_id)[0]
        return render(request, 'question/edit_page.html', {'profile_info': profile_obj, 'cats': cats})


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
            # return to the same page
            return redirect(f'/answer/{the_question_object.pk}')
        else:
            obj = Answer.objects.get(pk=answer_id)
            if Answer.objects.filter(pk=answer_id, downvoted_user=request.user):
                # downvote already exists
                obj.rmv_downvote(the_question_object, request.user, answer_id)
                obj.save()
            obj.upvoted(the_question_object, request.user, answer_id)
            obj.save()
            # return to the same page
            return redirect(f'/answer/{the_question_object.pk}')
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
            # return to the same page
            return redirect(f'/answer/{the_question_object.pk}')
        else:
            obj = Answer.objects.get(pk=answer_id)
            if Answer.objects.filter(pk=answer_id, upvoted_user=request.user).count() > 0:
                # downvote already exists
                obj.rmv_upvote(the_question_object, request.user, answer_id)
                obj.save()
            obj.downvoted(the_question_object, request.user, answer_id)
            obj.save()
            # return to the same page
            return redirect(f'/answer/{the_question_object.pk}')
    else:
        messages.error(request, 'The Answer does not exist')
        return redirect('/')


def search(request):
    container = []
    if request.method == 'POST':
        query = request.POST.get('search')
        query_prev = query
        if query.isspace() or query == '':
            messages.error(request, 'Query can not be empty')
            return redirect('/')
        query = query.lower()
        if '?' in query:
            query = query.replace('?', '')
        
        query_list = query.split(' ')
        ignore_list = ['what', 'how', 'when', 'who', 'where', 'if', 'then', 'one', 'in', 'of', 'under', 'like',
                       'a', 'b', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o',
                       'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z', 'c',
                       '.', '?', '!', 'you', 'till']
        
        pial_temp_obj = query_list.copy()

        for item in pial_temp_obj:
            print(item)
            if item in ignore_list:
                try:
                    query_list.remove(item)
                except:
                    pass
        
        print(query_list)

        for q in query_list:
            temp = Question.objects.filter(the_question__contains=q)
            for item in temp:
                if item not in container:
                    container.append(item)

        x = Question.objects.all()

        for item in x:
            habijabi = item.question_category.lower()
            if habijabi in query_list:
                if item not in container:
                    container.append(item)
    else:
        messages.error(request, 'Please put your query in the search box!')
        return redirect('/')
    cats = c.objects.all()
    print(len(container))
    return render(request, 'question/search.html', {'results': container, 'cats': cats, 'fr': query_prev})


def search2(request, cat_id):
    container = []
    query = c.objects.get(pk=cat_id)
    query = query.cat

    results = Question.objects.filter(question_category=query)

    cats = c.objects.all()
    return render(request, 'question/search.html', {'results': results, 'cats': cats, 'fr': query})


d = enchant.Dict("en_US")


def sentence_tester(sentence):
    sentence = sentence.split(' ')
    count = 0
    for word in sentence:
        if d.check(word):
            count += 1

    if count >= 2:
        return True

    return False


def question_edit(request, answer_id):
    cats = c.objects.all()
    if request.method == 'POST':
        edited_answer = request.POST.get('edited_answer')
        if len(edited_answer) > 0 and edited_answer.strip():
            answer_obj = Answer.objects.filter(pk=answer_id)
            if answer_obj.count() > 0 and answer_obj[0].answered_by == request.user:
                answer_obj = answer_obj[0]
                answer_obj.the_answer = edited_answer
                answer_obj.save()
                messages.success(request, 'Succesfully updated your answer!')
                return redirect(f'/answer/{answer_obj.answer_of.pk}')
            else:
                messages.error('Something went wrong!')
                return redirect('/')
        else:
            messages.error(request, 'Answer can not be empty!')
            return redirect(f'/et/{answer_id}')
    elif request.method == 'GET':
        data = Answer.objects.filter(pk=answer_id)
        if data.count() > 0:
            if request.user == data[0].answered_by:
                data = data[0]
                return render(request, 'question/answer_edit_page.html', {'answer': data, 'cats': cats})
            else:
                messages.error(request, 'Something went wrong!')
                return redirect('/')
        else:
            messages.error(request, 'Something went wrong!')
            return redirect('/')


def all_questins(request):
    object_set  = Question.objects.all().order_by('-asked_when')
    cats = c.objects.all()
    p = Paginator(object_set, 10)
    page_number = request.GET.get('page')
    page_obj = p.get_page(page_number)
    return render(request, 'question/all.html', {'questions_set': page_obj, 'cats': cats})
