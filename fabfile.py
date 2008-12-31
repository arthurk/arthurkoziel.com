set(
    fab_hosts = ['arthurk.webfactional.com'],
    fab_user = 'arthurk',
    host_dir = '/home/arthurk/webapps/djangowsgi/',
    project_dir = '/home/arthurk/webapps/djangowsgi/shellfish/',
    media_dir = '/home/arthurk/webapps/media/arthurkoziel.com/',
    log_dir = '/home/arthurk/webapps/djangowsgi/apache2/logs/',
    apache_bin = '/home/arthurk/webapps/djangowsgi/apache2/bin/',
)

def deploy():
    "Deploy the app to the target environment"
    run("cd $(project_dir); git pull; cp -R site_media/* /home/arthurk/webapps/media/arthurkoziel.com/;")

def restart():
    "Restart the apache webserver"
    run("$(apache_bin)restart;")

def gc():
    "Run git gc in project dir"
    run("cd $(project_dir); git gc;")

def error_log():
    "Tail the servers error logfile."
    run('tail -f $(log_dir)error_log')

def access_log():
    "Tail the servers access logfile."
    run('tail -f $(log_dir)access_log')