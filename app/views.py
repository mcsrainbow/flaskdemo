from flask import render_template, flash, redirect, send_from_directory
from app import app
from forms import LoginForm

@app.route('/')
@app.route('/index')
def index():
    user = { 'nickname': 'Dong' }
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
    return render_template("index.html",
        title = 'Home',
        user = user,
        posts = posts)

@app.route('/status')
def status():
    from app.utils.operations import local
    from decimal import Decimal

    os_release = local('cat /etc/*-release |head -n 1 |cut -d= -f2 |sed s/\\"//g')

    output = local("""grep -w "MemTotal" /proc/meminfo |awk '{print $2}'""")
    t_mem_m = Decimal(output) / 1024
    os_memory = round(t_mem_m,2)

    cpu_type = local("""grep 'model name' /proc/cpuinfo |uniq |awk -F : '{print $2}' |sed 's/^[ \t]*//g' |sed 's/ \+/ /g'""")
    cpu_cores = local("""grep 'processor' /proc/cpuinfo |sort |uniq |wc -l""")

    output = local("""/sbin/ifconfig |grep "Link encap" |awk '{print $1}' |grep -wv 'lo' |xargs""")
    nics = output.split()
    t_nic_info = ""
    for i in nics:
        ipaddr = local("""/sbin/ifconfig %s |grep -w "inet addr" |cut -d: -f2 | awk '{print $1}'""" % (i))
        if ipaddr:
            t_nic_info = t_nic_info + i + ":" + ipaddr

    top_info = local('top -b1 -n1 |head -n 5')
    top_info_list = top_info.split('\n')
    
    return render_template("status.html",
            os_release = os_release,
            os_memory = os_memory,
            cpu_type = cpu_type,
            cpu_cores = cpu_cores,
            os_network = t_nic_info,
            top_info_list = top_info_list)

@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for OpenID="' + form.openid.data + '", remember_me=' + str(form.remember_me.data))
        return redirect('/index')
    return render_template('login.html',
        title = 'Sign In',
        form = form,
        providers = app.config['OPENID_PROVIDERS'])
