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

    mem_raw = local("""grep -w "MemTotal" /proc/meminfo |awk '{print $2}'""")
    mem_mb = Decimal(mem_raw) / 1024
    os_memory = round(mem_mb,2)

    cpu_type = local("""grep 'model name' /proc/cpuinfo |uniq |awk -F : '{print $2}' |sed 's/^[ \t]*//g' |sed 's/ \+/ /g'""")
    cpu_cores = local("""grep 'processor' /proc/cpuinfo |sort |uniq |wc -l""")

    nics_raw = local("""/sbin/ifconfig |grep "Link encap" |awk '{print $1}' |grep -wv 'lo' |xargs""")
    nics_list = nics_raw.split()
    t_nic_info = ""
    for nic in nics_list:
        ipaddr = local("""/sbin/ifconfig %s |grep -w "inet addr" |cut -d: -f2 |awk '{print $1}'""" % (nic))
        if ipaddr:
            t_nic_info = t_nic_info + nic + ":" + ipaddr

    top_info_raw = local('top -b1 -n1 |head -n 5')
    top_info_list = top_info_raw.split('\n')
    
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
