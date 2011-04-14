import os
from fabric.api import env, run, cd, sudo, open_shell
import settings

env.host_string = settings.HOST_STRING
env.password = settings.PASS

def shell():
    open_shell('cd '+ settings.GIT_DIR)

def deploy_dataset(dataset, list = True):
    with cd(settings.GIT_DIR):
        dataset_path = os.path.join(settings.WWW_DIR, dataset)
        
        sudo('rm -rf ' + dataset_path)
        sudo('mkdir -p %s' % dataset_path)
        sudo('cp datasets/'+ dataset + '/raw/* ' + dataset_path)
        if list:
            run('ls '+ dataset_path)
        
def deploy_all():
    for dataset in settings.DATASET_LIST:
        deploy_dataset(dataset, list = False) 
    run('tree -d '+ settings.WWW_DIR)

def server_restart():
    sudo('/etc/init.d/lighttpd restart')
    
def server_stop():
    sudo('/etc/init.d/lighttpd stop')

def clone_repository():
    with cd(settings.GIT_DIR):
        run('rm -rf * .git*')
        run('ls -a')
        run('git clone %s .' % settings.GIT_REPO_URL)
        run('tree -d .')
        
def checkout_remote_branch(branch):
    with cd(settings.GIT_DIR):
        run('git branch -a')
        run('git checkout -b %s origin/%s' % (branch,branch))
        run('git branch')
        
def checkout_branch(branch):
    with cd(settings.GIT_DIR):
        run('git branch -a')
        run('git checkout %s' % branch)
        run('git branch')