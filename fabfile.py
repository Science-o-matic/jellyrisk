from fabric.api import *

env.roledefs = {
    'jellyrisk': ['jellyrisk@jellyrisk.com'],
    'sudoer': ['jellyrisk.com']
    }
env.hosts = ['jellyrisk.com']
env['project_path'] = "/home/jellyrisk/www/jellyrisk/"
env['python_path'] = "/home/jellyrisk/.virtualenvs/jellyrisk/bin/python"


@roles('jellyrisk')
def git_status():
    with cd(env['project_path']):
        run('git fetch && git status') 


@roles('jellyrisk')
def pushpull():
    local("git push origin master")
    with cd(env['project_path']):
        run('git pull') 


@roles('sudoer')
def reload_app():
    run('sudo supervisorctl restart jellyrisk')
    run('sudo /etc/init.d/nginx reload') 



@roles('sudoer')
def release(migrate=False, static=True):
    pushpull()
    with cd(env['project_path']):
        if migrate:
            _run_manage('manage.py migrate')
        if static:
            _run_manage('manage.py collectstatic')
    reload_app()


def _run_manage(command):
    run("%s %s" % (env['python_path'], command))
