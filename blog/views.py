from django.shortcuts import render

def set_session(request, username='', page='index'):
    request.session['username'] = username
    request.session['page'] = page


def index(request):
    username = request.session.get('username', '')
    set_session(request, username)
    return render(request, 'blog/index.html')