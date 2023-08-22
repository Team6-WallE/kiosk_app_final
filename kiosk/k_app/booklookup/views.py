from django.shortcuts import render, redirect
import itertools
from django.core.mail import send_mail
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Create your views here.

def login_user(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('set_mode')
        else:
            messages.success(request, ("There was an error logging in. Try again"))
            return redirect('/')
    else:
        return render(request, 'authenticate/login.html', {})

def logout_user(request):
    logout(request)
    messages.success(request, ("You were logged out"))
    return redirect('/')

def set_mode(request):
    return render(request, 'set_mode.html', {})

def checkin(request):
    return render(request, 'checkin.html', {})

def patrol_home(request):
    return render(request, 'patrol_home.html')

def assist_home(request):
    if request.method == "POST":
        return render(request, 'patrol_home.html', {})   
    return render(request, 'assist_home.html', {})

def fac_loc(request):
    return render(request, 'fac_loc.html', {})

def req_lib(request):
    import json
    import requests
    
    if request.method == 'POST':
        user_mail = request.POST.get('UserMail')
        subject = request.POST.get('Subject')
        body = request.POST.get('Body')
        help_options = request.POST.get('HelpOptions')
        
        if str(user_mail) == "" or str(subject) == "":
            status = True
        else:
            if str(help_options) == 'HSS':
                send_mail(
                    'I would like to request for extra help by ' + subject, # subject
                    body, # message
                    user_mail, # from email
                    ['saharshini2002@gmail.com'], #to email
                )
                status = False
            elif str(help_options) == 'ENG':
                send_mail(
                    subject, # subject
                    body, # message
                    user_mail, # from email
                    ['dillys00th@gmail.com'], #to email
                )
                status = False
            elif str(help_options) == 'ICT':
                send_mail(
                    subject, # subject
                    body, # message
                    user_mail, # from email
                    ['kenneth2433@gmail.com'], #to email
                )
                status = False
            else:
                send_mail(
                    subject, # subject
                    body, # message
                    user_mail, # from email
                    ['harshini180502@gmail.com'], #to email
                )
                status = False
        
        return render(request, 'req_lib.html', {'status': status, 'name': subject})
        
    else:
        return render(request, 'req_lib.html', {})

def faq(request):
    import json
    import requests
    question_string = None
    query = None
    ans = None

    if request.method == "POST":
        question = request.POST['searchkey']
        question_string = str(question).lower()
        db_questions = requests.get("http://127.0.0.1:8002/question?questions=", question_string.strip())
        db_answers = requests.get("http://127.0.0.1:8002/answer", question_string.strip())
        
        try:
            api_question = json.loads(db_questions.content)
            api_answer = json.loads(db_answers.content)
            query = list()
        
            for faq, answer in itertools.zip_longest(api_question, api_answer):
                if str(faq['questions']).lower().startswith(question_string[0:10]):
                    if str(faq['question_id']) in str(answer['question_id']):
                        faq['answer'] = answer['answers']
                        query.append(faq)

        except Exception as e:
            print("cannot access")

    return render(request, 'faq.html', {'query': query,
                                        'result': question_string})

def book_fac(request):
    return render(request, 'book_fac.html', {})

def search_results(request):
    import json
    import requests
    book_output = None
        
    if request.method == "POST":
        keyword_to_search = str(request.POST['searchkey']).lower()
        api_books = requests.get("http://127.0.0.1:8001/Books?book_name=", keyword_to_search.strip())
        api_borrows = requests.get("http://127.0.0.1:8001/Borrow", keyword_to_search.strip())
        
        try:
            api_book = json.loads(api_books.content)
            api_borrow = json.loads(api_borrows.content)
            book_output = list()
                        
            for item_book, item_borrow in itertools.zip_longest(api_book, api_borrow):
                if not keyword_to_search:
                    if str(item_book['book_id']) in str(item_borrow['book_id']):
                        item_book.update({'status' : item_borrow['status']})
                        book_output.append(item_book)
                elif str(item_book['book_name']).lower().startswith(keyword_to_search[0:4]):
                    if str(item_book['book_id']) in str(item_borrow['book_id']):
                        item_book.update({'status' : item_borrow['status']})
                        book_output.append(item_book)

        except Exception as e:
            api_book =  "Error requesting api book"

        return render(request, 'search_results.html', {'api_book': book_output,
                                                    'result': keyword_to_search})
