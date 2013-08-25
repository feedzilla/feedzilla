from __future__ import with_statement
from fabric import api
from fabric.contrib import django
import os

# Configuration
ENV_DIR = '.env'
REMOTE_ROOT = ''
api.env.user = 'web'
api.env.hosts = []

# Activate the virtualenv
try:
    activate_this = ENV_DIR + '/bin/activate_this.py'
    execfile(activate_this, dict(__file__=activate_this))
except IOError:
    pass
else:
    django.settings_module('settings')


def _database_name():
    "Return name of default database"

    import settings

    return settings.DATABASES['default']['NAME']


def _database_engine():
    "Return engine of default database"

    import settings

    return settings.DATABASES['default']['ENGINE']


def reset():
    """
    Drop databse, create new, then do syncdb and migrate.
    """

    import settings

    if getattr(settings, 'DATABASE_RESET_SILENTLY', None):
        response = 'yes'
    else:
        response = raw_input('Are you sure you want to reset site\'s database? Enter yes to continue: ')

    if response == 'yes':
        dbname = _database_name()
        engine = _database_engine()
        with api.settings(warn_only=True):
            if 'psycopg' in engine:
                api.local('dropdb %s' % dbname)
            elif 'sqlite' in engine:
                api.local('rm %s' % dbname)
            else:
                raise Exception('Unknown engine: %s' % engine)
        if 'psycopg' in engine:
            api.local('createdb %s' % dbname)
        elif 'sqlite' in engine:
            if not os.path.exists(os.path.split(dbname)[0]):
                os.makedirs(os.path.split(dbname)[0])
        api.local('./manage.py syncdb --noinput')
        if 'south' in settings.INSTALLED_APPS:
            api.local('./manage.py migrate')
    else:
        print 'Cancelling'


def run():
    "Run debug server"

    api.local('./manage.py runserver 0.0.0.0:8000')


def run_plus():
    "Run debug server with werkzeug debugger"

    api.local('./manage.py runserver_plus 0.0.0.0:8000')


def buildenv():
    # Ignore "IOError: [Errno 26] Text file busy: 'var/.env/bin/python'"
    # when debug server is live
    with api.settings(warn_only=True):
        api.local('virtualenv --no-site-packages %s' % ENV_DIR, capture=False)
    api.local('%s/bin/easy_install pip' % ENV_DIR, capture=False)
    api.local('%s/bin/pip install --use-mirrors -r requirements.txt' % ENV_DIR, capture=False)


def dbdump():
    "Create dump of database"

    api.local('pg_dump -Fc -Z9 -x -f /tmp/dump.pack %s' % _database_name())


def dbsync():
    """
    Download remote database dump and load it into local database.
    """

    with api.cd(REMOTE_ROOT):
        api.run('fab dbdump')
    api.get('/tmp/dump.pack', '/tmp/dump.pack')
    dbload()


def dbload(path='/tmp/dump.pack'):
    with api.settings(warn_only=True):
        api.local('dropdb %s' % _database_name())
        api.local('createdb %s' % _database_name())
    with api.settings(warn_only=True):
        api.local('pg_restore -v -c -x -d %s %s' % (_database_name(), path))


def shell():
    "Run shell_plus management command."

    api.local('./manage.py shell_plus')


def deploy():
    import settings

    api.local('hg push')
    with api.cd(REMOTE_ROOT):
        api.run('hg up')
        api.run('./manage.py syncdb --noinput')
        if 'south' in settings.INSTALLED_APPS:
            api.run('./manage.py migrate')
        api.run('touch app.py')


def update_lib(name):
    """
    Update dependency which has record in requirements.txt matched to given ``name``.
    """
    
    for line in open('requirements.txt'):
        if name in line:
            line = line.strip()
            if not line.startswith('#'):
                api.local('%s/bin/pip install --use-mirrors -U %s' % (ENV_DIR, line.strip()))


def startapp(name):
    """
    Create application files from template.
    """

    api.local('cp -r .app_template %s' % name)


def automig(name):
    """
    Create auto south migration and apply it to database.
    """

    api.local('./manage.py schemamigration %s --auto' % name)
    api.local('./manage.py migrate %s' % name)
