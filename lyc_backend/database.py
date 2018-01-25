import sqlite3 as db
import random
import string


class Database:

    def __init__(self):
        self.con=db.connect('base.db')


    def register(self, login, password, name, email):
        l =len(cur.execute('select login from logins where login = \'{login}\''.format(login=login)).fetchall())
        l1 = len(cur.execute('select email from logins where email = \'{email}\''.format(email=email)).fetchall())
        if l== 1:
            return '{result}, {error}'.format(result='error', error='Login')
        elif l1==1:
            return '{result}, {error}'.format(result='error', error='Password')
        elif l==0:
            cur.execute('insert into logins values(\'{login}\', \'{password}\', \'{name}\', \'{email}\',NULL)'.format(login=login, password=password, name=name,email=email))
            con.commit()
            return '{result}, {error}'.format(result='OK', error='')
        else:
            return '{result}, {error}'.format(result='error', error='Database error')
    def check_token(self, token, login):
        res = len(cur.execute('select * from tokens where token = {token}, login = {login}'.format(token=token, login = login)).fetchall())
        if res == 1:
            return '{result}, {error}'.format(result='OK', error='')
        elif res == 0:
            return '{result}, {error}'.format(result='error', error='Not found')
        else:
            return '{result}, {error}'.format(result='error', error='Database error')
    def make_token(self, login):
        random.seed()
        token =''.join(random.choice(string.ascii_letters+string.digits) for i in range(64))
        while len(cur.execute('select token from tokens where token=\'{token}\''.format(token= token)).fetchall()) > 0:
            token =''.join(random.choice(string.ascii_letters+string.digits) for i in range(64))
        cur.execute('insert into tokens values(\'{token}\', \'{login}\');'.format(token = token, login = login))
        return token
    def auth(self, login, password):
        res = len(cur.execute('select login, password from logins where login=\'{login}\' and password=\'{password}\''.format(login=login, password=password)).fetchall())
        if res == 1:
            token = ''
            if len(cur.execute('select login from tokens where login=\'{login}\''.format(login = login)).fetchall())==0:
                token = self.make_token(login)
            else:
                token = cur.execute('select token from tokens where login = \'{login}\''.format(login=login)).fetchall()[0]
                token = list(token)[0]
            return '{result}, {error}, {token}'.format(result='OK', error='', token=token)
        elif res==0:
            return '{result}, {error}'.format(result='error', error='wrong login/password')
        else:
            return '{result}, {error}'.format(result='error', error='Databse error')
    def get_posts(self, token):
        login = list(cur.execute('select login from tokens where token=\'{token}\''.format(token = token)).fetchall())[0][0]
        tags = cur.execute('select tags from logins where login=\'{login}\''.format(login=login)).fetchall()[0]
        if tags[0] == None:
            return []
        tags = tags[0].split(';')
        tag = ''
        for t in tags:
            if t =='':
                continue
            tag+=' source = \'{t}\' or'.format(t=t)
        tag = tag[:len(tag)-2]
        resp = cur.execute('select id from news where {tag} order by date asc'.format(tag=tag)).fetchall()
        for i in range(len(resp)):
            resp[i]=resp[i][0]
        return resp

    def get_post_by_id(self, id):
        return cur.execute('select name,short, url from news where id={id}'.format(id=id)).fetchall()[0]

    def add_post(self, source, date, name, short, url):
        enum = list(cur.execute('select max(id) from news').fetchall()[0])[0]+1
        command= '''insert into news values({id},'{source}','{date}','{name}','{short}', '{url}')'''.format(id=str(enum), source=source, date=date, name=name, short=short, url=url)
        #print(command)
        cur.execute(command)
        con.commit()
    def check_post_by_url(self,url):
        cnt = len(cur.execute('select url from news where url=\'{url}\''.format(url=url)).fetchall())
        return cnt == 1
    def get_login(self, token):
        res = list(cur.execute('select login from tokens where token=\'{token}\''.format(token = token)).fetchall())
        if len(res)==1:
            name = cur.execute('select name from logins where login=\'{login}\''.format(login=res[0][0])).fetchall()[0][0]
            return 'OK {login}'.format(login = name)
        else:
            return 'Error'
    def get_rss(self):
        return cur.execute('select name from rss').fetchall()
    def set_sources(self, token, sources):
        login = list(cur.execute('select login from tokens where token=\'{token}\''.format(token = token)).fetchall())[0][0]
        cur.execute('''update logins set tags = \'{sources}\' where login=\'{login}\''''.format(login=login, sources=sources))
        return
    def add_src(self, url, name):
        if len(cur.execute('''select * from rss where url=\'{url}\''''.format(url=url)).fetchall()) == 0:
            cur.execute('''insert into rss values(\'{url}\',\'{name}\')'''.format(url=url, name=name))
            con.commit()
            return 'OK'
        else:
            return 'Exists'
    def get_tags(self, token):
        login = list(cur.execute('select login from tokens where token=\'{token}\''.format(token = token)).fetchall())[0][0]
        tags = cur.execute('select tags from logins where login=\'{login}\''.format(login=login)).fetchall()[0]
        if tags[0] == None:
            return ''
        else:
            return tags[0]

con = db.connect('base.db')
cur = con.cursor()
#cur.execute('CREATE TABLE tokens (token VARCHAR(1000) PRIMARY KEY, login VARCHAR(100))')
#cur.execute('CREATE TABLE logins(login VARCHAR(100) PRIMARY KEY, password VARCHAR(100), tags TEXT)')
#cur.execute('CREATE TABLE news(id INTEGER PRIMARY KEY, text VARCHAR)')
