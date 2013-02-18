from fabric.api import *

env.roledefs = {
    'jellyrisk': ['jellyrisk@jellyrisk.com'],
    'nginx': ['jellyrisk.com']
    }
env.hosts = ['jellyrisk.com']
env['project_path'] = "~/www/jellyrisk/"


@roles('jellyrisk')
def git_status():
    with cd(env['project_path']):
        run('git fetch && git status') 


@roles('jellyrisk')
def pushpull():
    local("git push origin master")
    with cd(env['project_path']):
        run('git pull') 


@roles('nginx')
def reload_nginx():
    run('sudo /etc/init.d/nginx reload') 


@roles('jellyrisk')
def release():
    pushpull()
    with cd(env['project_path']):
        run('./manage.py migrate')
	run('sudo supervisorctl restart jellyrisk')
        run('./manage.py collectstatic')
    reload_nginx()
