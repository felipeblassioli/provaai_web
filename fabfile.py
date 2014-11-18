from fabric.api import *

def bootstrap():
    run('mkdir -p /var/www/provaai')
    with cd('/var/www/provaai'):
        run('virtualenv env')
        run('. env/bin/activate')
        put('config/provaai.wsgi','provaai.wsgi')
        put('config/provaai.cfg.dev','provaai.cfg')
    put('config/provaai.vhost.dev', '/etc/apache2/sites-available/provaai.conf', use_sudo=True, mirror_local_mode=True)
    run('sudo a2ensite provaai')


def pack():
    local('python setup.py sdist --formats=gztar', capture=False)

def deploy():
    dist = local('python setup.py --fullname', capture=True).strip()
    put('dist/%s.tar.gz' % dist, '/tmp/provaai.tar.gz')
    run('mkdir -p /tmp/provaai')

    with cd('/tmp/provaai'):
        run('tar xzf /tmp/provaai.tar.gz')
        with cd('/tmp/provaai/%s' % dist):
            run('/var/www/provaai/env/bin/python setup.py install')
    run('rm -rf /tmp/provaai /tmp/provaai.tar.gz')
    run('sudo service apache2 reload')