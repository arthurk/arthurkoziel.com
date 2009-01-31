# Shellfish

This is the source code of my blog at [arthurkoziel.com](http://arthurkoziel.com).

## Requirements

- Python (2.5)
- Django (1.0.2)
- Markdown (2.0-beta, git rev be6891a22f6888af302392bc2dfa1e4a6099fd4f)
- Pygments (1.0)
- django-tagging (0.3-pre, svn rev 154)
- django-disqus (http://github.com/arthurk/django-disqus)

## Installation

1. Checkout the source code with `git clone git://github.com/arthurk/shellfish.git`.
2. Run `python manage.py syncdb` to initialize the database. Per default,
   a SQLite database will be created in the project directory.
3. Start the development server by executing `python manage.py startserver`.
4. Navigate to `http://localhost:8000/` in your web browser. The backend can
   be found at `http://localhost:8000/admin/`.

## Apache Server Configuration

To display the `robots.txt` and `favicon.ico` files, you need to disable the
default handler (which would run those files through the Django engine) and 
tell Apache to look for them on the local filesystem:

    <Location ~ "/(robots.txt|favicon.ico)/">
        SetHandler None
    </Location>
    alias /robots.txt /path/to/robots.txt 
    alias /favicon.ico /path/to/favicon.ico

## Static Media

During development (when the `DEBUG` setting is set to `True`) Django's 
static serve view will be used to serve static media. If you want run the 
application on a production system you need to:

1. Create a `settings_local.py` file in the project directory.
2. Add the [MEDIA\_URL](http://docs.djangoproject.com/en/dev/ref/settings/#media-url) setting to it and set it to the location where 
   the static files are hosted.

## Comments

To enable comments you need to have [DISQUS](http://disqus.com) account and 
a website registered with DISQUS. Edit the `settings_local.py` file and 
assign the shortname of your website to the `DISQUS_WEBSITE_SHORTNAME` variable:

    DISQUS_WEBSITE_SHORTNAME = 'foobar'