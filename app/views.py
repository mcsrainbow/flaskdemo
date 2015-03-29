from flask import render_template, flash, redirect, session, url_for, request, g
from flask.ext.login import login_user, logout_user, current_user, login_required
from datetime import datetime
from app import app, db, lm, oid
from .forms import LoginForm, EditForm
from .models import User


@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.before_request
def before_request():
    g.user = current_user
    if g.user.is_authenticated():
        g.user.last_seen = datetime.utcnow()
        db.session.add(g.user)
        db.session.commit()


@app.route('/')
@app.route('/index')
@login_required
def index():
    user = g.user
    posts = [
        {
            'author': { 'nickname': 'John' },
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': { 'nickname': 'Susan' },
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html',
                           title='Home',
                           user=user,
                           posts=posts)


@app.route('/user/<nickname>')
@login_required
def user(nickname):
    user = User.query.filter_by(nickname=nickname).first()
    if user is None:
        flash('User %s not found.' % nickname)
        return redirect(url_for('index'))
    posts = [
        {'author': user, 'body': 'BEC Notes - Ways of working'},
        {'author': user, 'body': 'Setup GlusterFS with Distributed Replicated Volumes and Native client'}
    ]
    return render_template('user.html',
                           user=user,
                           posts=posts)


@app.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
    form = EditForm()
    if form.validate_on_submit():
        g.user.nickname = form.nickname.data
        g.user.about_me = form.about_me.data
        db.session.add(g.user)
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit'))
    else:
        form.nickname.data = g.user.nickname
        form.about_me.data = g.user.about_me
    return render_template('edit.html', form=form)


@app.route('/status')
@login_required
def status():
    from app.utils.operations import local
    from decimal import Decimal

    os_release = local('cat /etc/*-release |head -n 1 |cut -d= -f2 |sed s/\\"//g')

    mem_output = local("""grep -w "MemTotal" /proc/meminfo |awk '{print $2}'""")
    mem_mb = Decimal(mem_output) / 1024
    os_memory = round(mem_mb,2)

    cpu_type = local("""grep 'model name' /proc/cpuinfo |uniq |awk -F : '{print $2}' |sed 's/^[ \t]*//g' |sed 's/ \+/ /g'""")
    cpu_cores = local("""grep 'processor' /proc/cpuinfo |sort |uniq |wc -l""")

    nics_output = local("""/sbin/ifconfig |grep "Link encap" |awk '{print $1}' |grep -wv 'lo' |xargs""")
    nics_list = nics_output.split()
    t_nic_info = ""
    for nic in nics_list:
        ipaddr = local("""/sbin/ifconfig %s |grep -w "inet addr" |cut -d: -f2 |awk '{print $1}'""" % (nic))
        if ipaddr:
            t_nic_info = t_nic_info + nic + ":" + ipaddr

    disk_usage = local("""df -h |grep lv_root |awk -F 'G' '{print $2" "$3" "$5}' |awk '{print $3"/"$2"G "$4}'""")

    top_info_output = local('top -b1 -n1 |head -n 5')
    top_info_list = top_info_output.split('\n')
    
    return render_template('status.html',
                            os_release=os_release,
                            os_memory=os_memory,
                            cpu_type=cpu_type,
                            cpu_cores=cpu_cores,
                            os_network = t_nic_info,
                            disk_usage = disk_usage,
                            top_info_list = top_info_list)


@app.route('/login', methods = ['GET', 'POST'])
@oid.loginhandler
def login():
    if g.user is not None and g.user.is_authenticated():
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        session['remember_me'] = form.remember_me.data
        return oid.try_login(form.openid.data, ask_for=['nickname', 'email'])
    return render_template('login.html',
                           title='Sign In',
                           form=form,
                           providers=app.config['OPENID_PROVIDERS'])


@oid.after_login
def after_login(resp):
    if resp.email is None or resp.email == "":
        flash('Invalid login. Please try again.')
        return redirect(url_for('login'))
    user = User.query.filter_by(email=resp.email).first()
    if user is None:
        nickname = resp.nickname
        if nickname is None or nickname == "":
            nickname = resp.email.split('@')[0]
        user = User(nickname=nickname, email=resp.email)
        db.session.add(user)
        db.session.commit()
    remember_me = False
    if 'remember_me' in session:
        remember_me = session['remember_me']
        session.pop('remember_me', None)
    login_user(user, remember=remember_me)
    return redirect(request.args.get('next') or url_for('index'))


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
