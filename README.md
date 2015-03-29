Instruction
---
1. Install OS packages<br>
  `[dong@flaskdemo ~]$ sudo yum groupinstall "Development tools"`<br>
  `[dong@flaskdemo ~]$ sudo yum install zlib-devel bzip2-devel openssl-devel ncurses-devel`<br>
  `[dong@flaskdemo ~]$ sudo yum install python-setuptools`<br>
  `[dong@flaskdemo ~]$ sudo yum install http://dl.fedoraproject.org/pub/epel/6/x86_64/epel-release-6-8.noarch.rpm`<br>
  `[dong@flaskdemo ~]$ sudo yum install python-pip`<br>

2. Create workspace environment<br>
  `[dong@flaskdemo ~]$ sudo easy_install virtualenv`<br>
  `[dong@flaskdemo ~]$ mkdir flaskdemo`<br>
  `[dong@flaskdemo ~]$ cd flaskdemo`<br>
  
  `[dong@flaskdemo flaskdemo]$ virtualenv flask`<br>
  `New python executable in flask/bin/python`<br>
  `Installing setuptools, pip...done.`<br>
  
  `[dong@flaskdemo flaskdemo]$ . flask/bin/activate`<br>
  `(flask)[dong@flaskdemo flaskdemo]$ `<br>

3. Install Python packages<br>
  `(flask)[dong@flaskdemo flaskdemo]$ vi flask/requirements.txt`<br>
  `flask`<br>
  `flask-login`<br>
  `flask-openid`<br>
  `flask-mail`<br>
  `flask-sqlalchemy`<br>
  `sqlalchemy-migrate`<br>
  `flask-whooshalchemy`<br>
  `flask-wtf`<br>
  `flask-babel`<br>
  `guess_language`<br>
  `flipflop`<br>
  `coverage`<br>
  
  `(flask)[dong@flaskdemo flaskdemo]$ pip install -r flask/requirements.txt`<br>
  `...`<br>
  `Successfully installed Babel-1.3 Jinja2-2.7.3 SQLAlchemy-0.9.9 Tempita-0.5.2 WTForms-2.0.2 Werkzeug-0.10.4 Whoosh-2.6.0 blinker-1.3 coverage-3.7.1 decorator-3.4.2 flask-0.10.1 flask-babel-0.9 flask-login-0.2.11 flask-mail-0.9.1 flask-openid-1.2.4 flask-sqlalchemy-2.0 flask-whooshalchemy-0.56 flask-wtf-0.11 flipflop-1.0 guess-language-0.2 itsdangerous-0.24 markupsafe-0.23 ordereddict-1.1 pbr-0.10.8 python-openid-2.2.5 pytz-2015.2 six-1.9.0 speaklater-1.3 sqlalchemy-migrate-0.9.6 sqlparse-0.1.15`<br>
  
  `(flask)[dong@flaskdemo flaskdemo]$ mkdir -p app/{static,templates}`<br>
  `(flask)[dong@flaskdemo flaskdemo]$ mkdir tmp`<br>

4. Download Bootstrap package<br>
  `(flask)[dong@flaskdemo flaskdemo]$ wget http://d.bootcss.com/bootstrap-3.3.4-dist.zip -O ~/bootstrap-3.3.4-dist.zip`<br>
  `(flask)[dong@flaskdemo flaskdemo]$ cd app/static`<br>
  `(flask)[dong@flaskdemo static]$ unzip ~/bootstrap-3.3.4-dist.zip`<br>

5. Run Flask Demo<br>
  `(flask)[dong@flaskdemo static]$ cd ~/flaskdemo`<br>
  
  `(flask)[dong@flaskdemo flaskdemo]$ ./run.py`<br>
  ` * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)`<br>
  ` * Restarting with stat`<br>
