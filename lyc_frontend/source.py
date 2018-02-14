from flask import Flask, render_template, request, redirect,url_for
import requests

app = Flask('frontend')
DEBUG = True

api = 'https://nikitonsky.tk/'

if DEBUG:
    api = 'http://127.0.0.1:55556/'



@app.route('/')
def root():
    try:
        username = request.cookies['token']
        return redirect(url_for('feed'))
    except:
        return redirect(url_for('login'))

@app.route('/feed')
def feed():
    try:
        token = request.cookies['token']
    except KeyError:
        return redirect(url_for('login'))
    resp = requests.get(api+'get_user/'+token).text.split()
    if resp[0] != 'OK':
            return redirect(url_for('login'))
    username = resp[1]
    ids = requests.get(api+'get_posts/'+token).text.split('\n')
    posts=[]
    begin = request.args.get('begin', '')
    if begin == '':
        begin = 0
    else:
        begin = int(begin)
    if '' in ids:
        ids.remove('')
    for id in ids[begin:begin+25]:

        post = requests.get(api+'get_post/'+id).text.split('\n')
        posts.append({'head' : post[0], 'text' : post[1], 'url' : post[2]})

    return render_template('index.html', posts = posts, username=username, begin = begin, cnt  =len(posts))



@app.route('/auth')
def auth():
    login = request.args.get('login', '')
    password = request.args.get('pass', '')
    res = requests.get(api+'login/'+login+'/'+password)
    res = res.text.split('\n')
    if(res[0]=='OK'):
        token = res[2]
        token = token[1:]
        resp = redirect(url_for('feed'))
        resp.set_cookie('token', token)
    else:
        resp = redirect(url_for('login', lerror='Неправильный логин/пароль'))
    return resp

@app.route('/logout')
def logout():
    resp = redirect(url_for('login'))
    resp.set_cookie('token', '', expires=0)
    return resp
@app.route('/login')
def login():
    rerror = request.args.get('rerror', '')
    if rerror==None:
        rerror=''
    lerror = request.args.get('lerror', '')
    if lerror==None:
        lerror=''
    return render_template('auth.html', rerror=rerror, lerror=lerror)

@app.route('/registration')
def registration():
    #src = ''
    #for arg in request.args:
    #    if arg[:3]=='rss':
    #        src+=arg[3:]+';'
    login = request.args.get('login','')
    name = request.args.get('name', '')
    pass1 = request.args.get('pass', '')
    pass2 = request.args.get('pass1', '')
    email = request.args.get('email', '')
    if pass1 != pass2:
        return redirect(url_for('login', rerror='Пароли не совпадают'))
    resp = requests.get(api+'register/' + login+'/'+pass1+'/'+name+'/'+email).text.split('\n')
    if resp[0]=='OK':
        return redirect(url_for('login'))
    elif resp[1]=='Login':
        return  redirect(url_for('login', rerror='Такой логин занят'))
    else:
        return  redirect(url_for('login', rerror='Такая почта уже используется'))

@app.route('/add')
def add():
    try:
        token = request.cookies['token']
    except KeyError:
        return redirect(url_for('login'))
    url = request.args.get('url', '')
    resp = requests.get(api+'add_src/'+url.replace('/', '%2')).text
    if resp == 'OK':
        return redirect(url_for('feed'))
    elif resp=='Exists':
        return redirect(url_for('new_src', error='Такая лента уже существует'))
    else:
        return 'Ban'

@app.route('/new_src')
def new_src():
    try:
        token = request.cookies['token']
    except KeyError:
        return redirect(url_for('login'))
    resp = requests.get(api+'get_user/'+token).text.split()
    if resp[0] != 'OK':
            return redirect(url_for('login'))
    username = resp[1]
    error=request.args.get('error', '')
    return render_template('add_rss.html', username=username, error=error)


@app.route('/set_src')
def set():
    try:
        token = request.cookies['token']
    except KeyError:
        return redirect(url_for('login'))
    src = ''
    for arg in request.args:
        if arg[:3]=='rss':
            src+=arg[3:]+';'
    resp = requests.get(api+'set_src/'+token+'/'+src)
    return redirect(url_for('feed'))


@app.route('/settings')
def settings():
    try:
        token = request.cookies['token']
    except KeyError:
        return redirect(url_for('login'))
    resp = requests.get(api+'get_user/'+token).text.split()
    if resp[0] != 'OK':
            return redirect(url_for('login'))
    username = resp[1]
    sources = requests.get(api+'get_sources').text.split('\n')
    tags = requests.get(api+'get_tags/'+token).text.split(';')
    return render_template('settings.html', sources = sources[:len(sources)-1], username=username, tags = tags)

@app.errorhandler(404)
def not_found_error(error):
    return redirect(url_for('feed'))

app.run(host = '127.0.0.1', port = 55555)
