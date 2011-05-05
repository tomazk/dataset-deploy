import os
import logging
from fabric.api import env, run, cd, sudo, open_shell, put
import settings

# logging init
log_path = os.path.join(os.getcwd(), 'fabric.log')
logger = logging.getLogger('local_fabric')
logger.addHandler(logging.FileHandler(filename = log_path))
logger.addFilter(logging.Filter('local_fabric'))
logger.setLevel(logging.DEBUG)

# fabric enviroment 
env.host_string = settings.HOST_STRING
env.password = settings.PASS

def gitdir(fun):
    # decorator for cd-ing into git repository directory
    def wrapper(*args, **kwargs):
        with cd(settings.GIT_DIR):
            fun(*args, **kwargs)
    return wrapper

# commands

def copy_log():
    '''Copy log to remote'''
    put(log_path, os.path.join(settings.HOME, 'fabric.log'))
    
def shell():
    '''Open a remote shell'''
    open_shell('cd '+ settings.GIT_DIR)

def home_shell():
    '''Open a shell in home directory'''
    open_shell('cd ' + settings.HOME_DIR)

@gitdir
def deploy_dataset(dataset, list = True):
    '''
    Cleanup any existing files in the dataset endpoint. 
    Copy raw dataset files to the endpoint.
    '''
    dataset_path = os.path.join(settings.WWW_DIR, dataset)
    
    sudo('rm -rf ' + dataset_path)
    sudo('mkdir -p %s' % dataset_path)
    sudo('cp datasets/'+ dataset + '/raw/* ' + dataset_path)
    if list:
        run('ls '+ dataset_path)
    logger.info('deployed dataset %s to %s', dataset , dataset_path )
        
def deploy_all():
    '''Deploy all datasets'''
    logger.info('deploying all datasets')
    for dataset in settings.DATASET_LIST:
        deploy_dataset(dataset, list = False) 
    run('tree -d '+ settings.WWW_DIR)

def server_restart():
    '''Start lighttpd deamon'''
    sudo('/etc/init.d/lighttpd restart')
    logger.info('lighttpd restart')
    
def server_stop():
    '''Stop lighttpd deamon'''
    sudo('/etc/init.d/lighttpd stop')
    logger.info('lighttpd stop')

@gitdir
def clone_repository():
    '''Clone the repository from the remote'''
    run('rm -rf * .git*')
    run('ls -a')
    run('git clone %s .' % settings.GIT_REPO_URL)
    run('tree -d .')
    logger.info('cloned repository from %s', settings.GIT_REPO_URL )
        
@gitdir
def checkout_remote_branch(branch):
    '''Create and checkout a remote git branch'''
    run('git branch -a')
    run('git checkout -b %s origin/%s' % (branch,branch))
    run('git branch')
    logger.info('checkout remote branch %s', branch)
        
@gitdir
def checkout_branch(branch):
    '''Checkout branch'''
    run('git branch -a')
    run('git checkout %s' % branch)
    run('git branch')
    logger.info('checkout branch %s', branch)
        
@gitdir
def pull_branch(branch):
    '''Pull branch'''
    run('git pull origin %s' % branch)
    logger.info('pull from branch %s', branch)
