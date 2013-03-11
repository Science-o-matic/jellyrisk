import os
from fabric.api import *
from fabric.operations import get, put
from fabric.contrib.console import confirm
from fab_settings import SUDOER_USER


env.roledefs = {
    'jellyrisk': ['jellyrisk@jellyrisk.com'],
    'sudoer': ['%s@jellyrisk.com' % SUDOER_USER]
    }
env.hosts = ['jellyrisk.com']
env['project_path'] = "/home/jellyrisk/www/jellyrisk/"
env['python_path'] = "/home/jellyrisk/.virtualenvs/jellyrisk/bin/python"
env['pip_path'] = "/home/jellyrisk/.virtualenvs/jellyrisk/bin/pip"


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
    sudo('supervisorctl restart jellyrisk', shell=False)
    sudo('service nginx reload', shell=False) 


@roles('sudoer')
def release(migrate=True, static=True):
    with settings(user='jellyrisk'):
        pushpull()
        run('%s install -r %spip-requirements.txt' % 
            (env['pip_path'], env['project_path']))
    with cd(env['project_path']):
        if migrate:
            migrate()
        if static:
            _run_manage('collectstatic')
    reload_app()


@roles('jellyrisk')
def migrate():
    with cd(env['project_path']):
        _run_manage('migrate')


@roles('jellyrisk')
def pull_db():
    with cd(env['project_path']):
        filename = 'dump_data.json'
        dump_file = os.path.join(env['project_path'], filename)
        _run_manage('%s' % _dump_cms_data(dump_file))
        get(dump_file, '.')
        run('rm %s' % dump_file)
        if confirm("Load dumped remote data into local DB?"):
            local('./manage.py loaddata %s' % filename)
            

@roles('jellyrisk')
def push_db():
    local_file = 'dump_data.json'
    remote_file = os.path.join(env['project_path'], local_file)
    local('./manage.py %s' % _dump_cms_data(local_file))
    put(local_file, remote_file)
    if confirm("Load dumped local data into remote DB?"):
        with cd(env['project_path']):        
            _run_manage('loaddata %s' % remote_file)


def _run_manage(command):
    run("%s ./manage.py %s" % (env['python_path'], command))


def _dump_cms_data(file_path):
    plugins = ('text', 'picture', 'link', 'file', 'snippet', 'googlemap',
               'cmsplugin_embeddedpages')
    return 'dumpdata cms %s --natural > %s' % (' '.join(plugins), file_path)
