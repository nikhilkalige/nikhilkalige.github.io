Title: Flask-Cache Stats
Project: True
Category: Python
Tags: Python, Flask, Flask-cache
Date: 2016-08-25
Slug: flask-cache-stats

Flask-cache-stats is an extension for [flask](http://flask.pocoo.org/) that extends [flask-cache](http://pythonhosted.org/Flask-Cache/) extension in order to provide modest amount of cache usage statistics. It hooks into the existing getter and setter methods of the cache backends to update a log file. The extension can then be registered as a blueprint so that the stats can be viewed as a table.

##Usage
Flask-cache-stats provides the same API's as flask-cache extension, so you just need to replace all the imports and you are good to go.
```python
# replace
from flask_cache import Cache
# with
from flask_cache_stats import Cache
```
The view for displaying the data table can be registered using the `CacheStats` blueprint. The blueprint is extensible that you can completely customize the behavior of the view. The class provides a `delete` rest API that can be used to clear a key from the cache. In order to make use of this API, you would need to install and setup [flask-login](https://flask-login.readthedocs.io/en/latest/) extension.
```python
class CacheStats(Blueprint):
    def __init__(self, cache_obj, base_template="base.html",
                 enable_clear_api=False, protect_api=True,
                 cache_template="stats_view.html",
                 url_prefix='/cache_stats')

# Usage
app = Flask(__name__)
app.config['CACHE_TYPE'] = 'simple'
cache = Cache(app)
stats_bp = CacheStats(cache, enable_clear_api=False)
```

Below is an example showing the usage of flask-cache-stats.

![Msldata cache usage example]({filename}/images/2016/flask-cache-stats.png)

### References and Links
1. [Flask-cache-stats](https://github.com/nikhilkalige/flask-cache-stats "Flask-cache-stats")
