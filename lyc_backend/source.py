from flask import Flask
import database
import feedparser
class Backend:
    def auth(self, login, password):
        meta = database.login(login, password)
        if not resp:
            return "ERROR"
        else:
            token = make_token(get_id(login))
            return token
    def get_feed(self, token):
        return data.get_posts(token)


app = Flask('backend')
data=database.Database()

backend = Backend()
@app.route('/')
def root():
    return 'FORBIDDEN'
@app.route('/login/<username>/<password>')
def login(username, password):
    meta = data.auth(username, password).split(',')
    return '\n'.join(meta)
@app.route('/register/<username>/<password>/<name>/<email>')
def register(username, password,name,email):
    meta = data.register(username, password, name,email).split(',')
    if meta[0]=='OK':
        return 'OK\nSuccesfully registered'
    else:
        return '\n'.join(meta)

@app.route('/get_user/<token>')
def get_user(token):
    return data.get_login(token)

@app.route('/get_sources')
def get_sources():
    resp=  ''
    for feed in data.get_rss():
        resp+=feed[0]+'\n'
    return resp

@app.route('/get_posts/<token>')
def get_posts(token):
    ids  = data.get_posts(token)
    return '\n'.join(map(str, ids))

@app.route('/get_post/<id>')
def get_post(id):
    return '\n'.join(map(str, data.get_post_by_id(id)))

@app.route('/set_src/<token>/<src>')
def set_src(token, src):
    data.set_sources(token, src)
    return 'OK'

@app.route('/add_src/<src>')
def add_src(src):
    src = src.replace('%2', '/')
    try:
        rss =feedparser.parse(src)
    except:
        return 'Error'
    return data.add_src(src,rss.feed.title)

@app.route('/add_post', methods=['POST'])
def add_post():
    url = request.data.get('url')
    source = request.data.get('src')
    date = request.data.get('date')
    short = request.data.get('short')
    name = request.data.get('title')
    data.add_post(source, date, name, short, url)

@app.route('/get_tags/<token>')
def get_tags(token):
    return data.get_tags(token)

app.run(host='127.0.0.1', port=55556)
