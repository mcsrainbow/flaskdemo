### Instruction

#### 1. Install OS packages

```
[dong@flaskdemo ~]$ sudo yum groupinstall "Development tools"
[dong@flaskdemo ~]$ sudo yum install zlib-devel bzip2-devel openssl-devel ncurses-devel
[dong@flaskdemo ~]$ sudo yum install python-setuptools
[dong@flaskdemo ~]$ sudo yum install http://dl.fedoraproject.org/pub/epel/6/x86_64/epel-release-6-8.noarch.rpm
[dong@flaskdemo ~]$ sudo yum install python-pip
```  

#### 2. Create workspace environment

```
[dong@flaskdemo ~]$ sudo easy_install virtualenv
[dong@flaskdemo ~]$ mkdir flaskdemo
[dong@flaskdemo ~]$ cd flaskdemo
  
[dong@flaskdemo flaskdemo]$ virtualenv flask
New python executable in flask/bin/python
Installing setuptools, pip...done.
  
[dong@flaskdemo flaskdemo]$ . flask/bin/activate
(flask)[dong@flaskdemo flaskdemo]$ 
```

#### 3. Install Python packages

```
(flask)[dong@flaskdemo flaskdemo]$ vi flask/requirements.txt
flask
flask-login
flask-openid
flask-mail
flask-sqlalchemy
sqlalchemy-migrate
flask-whooshalchemy
flask-wtf
flask-babel
guess_language
flipflop
coverage
  
(flask)[dong@flaskdemo flaskdemo]$ pip install -r flask/requirements.txt
...
Successfully installed Babel-1.3 Jinja2-2.7.3 SQLAlchemy-0.9.9 Tempita-0.5.2 WTForms-2.0.2 Werkzeug-0.10.4 Whoosh-2.6.0 blinker-1.3 coverage-3.7.1 decorator-3.4.2 flask-0.10.1 flask-babel-0.9 flask-login-0.2.11 flask-mail-0.9.1 flask-openid-1.2.4 flask-sqlalchemy-2.0 flask-whooshalchemy-0.56 flask-wtf-0.11 flipflop-1.0 guess-language-0.2 itsdangerous-0.24 markupsafe-0.23 ordereddict-1.1 pbr-0.10.8 python-openid-2.2.5 pytz-2015.2 six-1.9.0 speaklater-1.3 sqlalchemy-migrate-0.9.6 sqlparse-0.1.15

(flask)[dong@flaskdemo flaskdemo]$ mkdir -p app/{static,templates}
(flask)[dong@flaskdemo flaskdemo]$ mkdir tmp
```

#### 4. Download Bootstrap package

```
(flask)[dong@flaskdemo flaskdemo]$ wget http://d.bootcss.com/bootstrap-3.3.4-dist.zip -O ~/bootstrap-3.3.4-dist.zip
(flask)[dong@flaskdemo flaskdemo]$ cd app/static
(flask)[dong@flaskdemo static]$ unzip ~/bootstrap-3.3.4-dist.zip
```

#### 5. Run Flask Demo

```
(flask)[dong@flaskdemo static]$ cd ~/flaskdemo
  
(flask)[dong@flaskdemo flaskdemo]$ ./run.py
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
 * Restarting with stat
```
