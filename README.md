This is the source code of my blog at [arthurkoziel.com](http://arthurkoziel.com).

## Requirements

- Python 2.5
- [Django](http://www.djangoproject.com/) 1.1 alpha 1
- [Pygments](http://pygments.org/) 1.0
- [python-markdown](http://www.freewisdom.org/projects/python-markdown/) 2.0-rc1
- [django-tagging](http://code.google.com/p/django-tagging/) r154
- [django-disqus](http://github.com/arthurk/django-disqus) trunk

## Installation

1. Clone the repository.
2. Run `python manage.py syncdb` to initialize the database. Per default,
   a SQLite database will be created in the project directory.
3. Start the development server by executing `python manage.py startserver`.
4. Navigate to `http://localhost:8000/` in your web browser. The backend can
   be found at `http://localhost:8000/admin/`.

## Static Media

During development (when the `DEBUG` setting is set to `True`) Django's 
static serve view will be used to serve static media. If you want run the 
application on a production system you need to:

1. Create a `settings_local.py` file in the project directory.
2. Add the [MEDIA\_URL](http://docs.djangoproject.com/en/dev/ref/settings/#media-url) setting to it and set it to the location where 
   the static files are hosted.

## Comments

To enable comments you need to have a [DISQUS](http://disqus.com) account and 
a website registered with DISQUS. Edit the `settings_local.py` file and 
assign the shortname of your website to the `DISQUS_WEBSITE_SHORTNAME` variable:

    DISQUS_WEBSITE_SHORTNAME = 'foobar'