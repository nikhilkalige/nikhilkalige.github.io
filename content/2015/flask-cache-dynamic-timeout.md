Title: Flask-Cache dynamic timeout
Category: Python
Tags: Python, Flask, Flask-cache
Slug: flask-cache-dynamic-timeout
Summary: Setting dynamic timeouts for cached flask view functions


If you have used [Flask] [1] and are in need of caching views, then you will be familiar with [Flask-cache][2]. [Flask-cache][2] provides you with a very simple interface in order to setup cache for your application.

[Flask-cache][2] extension provides you with a way to set a specific time-out for your view function when you enable cache for that view as follows.

```python
@cache.cached(timeout=50)
def index():
  return render_template('index.html')
```

But it does not provide you the ability to set time-outs dynamically. I came across a use case where I was calling a view function with different parameters and wanted the view to be cached until a fixed specific time and in my case it was midnight.

Below is the implementation of the cached decorator in [Flask-cache][2]

```python
def cached(self, timeout=None, key_prefix='view/%s', unless=None):
    def decorator(f):
        @functools.wraps(f)
        def decorated_function(*args, **kwargs):
            ....
            if rv is None:
                rv = f(*args, **kwargs)
                try:
                self.cache.set(cache_key, rv,
                    timeout=decorated_function.cache_timeout)
            ....

        decorated_function.uncached = f
        decorated_function.cache_timeout = timeout
        decorated_function.make_cache_key = make_cache_key

        return decorated_function
    return decorator

```
You can see that the decorator directly passes the ```timeout``` parameter as a parameter to the ```cache.set``` function. So this removes the possibility of passing a function to dynamically set the timeout.

So I decided to write a decorator which decorates the ```cached``` decorator. Below is the decorator function I wrote that sets the time-out to 23:59 hours.

```python
def cache_timeout(f):
    @functools.wraps(f)
    def decorated_function(*args, **kwargs):
        now = datetime.datetime.now()
        deadline = now.replace(hour=23, minute=59)
        period = (deadline - now)
        f.cache_timeout = period.seconds
        return f(*args, **kwargs)
    return decorated_function
```

The ```cache_timeout``` decorator can then be used as

```python
@app.route('/stats', methods=['GET'])
@cache_timeout
@cache.cached()
def stats():
    return render_template('index.html')
```

Please note that location of ```@cache_timeout``` and ```@cache.cached()``` cannot be interchanged.

Currently the decorator does not accept any parameters, but it can be easily extended to include parameters and perform cache time-out operations to your satisfaction.

  [1]: http://flask.pocoo.org/ "Flask"
  [2]: https://pythonhosted.org/Flask-Cache/ "Flask-cache"
