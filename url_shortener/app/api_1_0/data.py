from .url import Url
from .runningurl import RunningURL
from .freeurl import freeURL
from .. import db
from .. import cache
from datetime import datetime
from .decorators import isolation_level
import json


#@cache.memoize(timeout=3600)
@isolation_level("READ COMMITTED")
def get_short_urls(long_url):
    urls = Url.query.filter_by(long_url = long_url).all()
    return urls


@isolation_level("AUTOCOMMIT")
def get_long_url(code, domain):
    # url =  Url.query.filter_by(short_url = code , domain = domain).first() #.long_url
    # if(url == None):
    #     return "No such url"
    # url.click_count += 1
    # url.added_datetime = datetime.now()
    # db.session.add(url)
    # db.session.commit()
    return get_long_url2(code, domain)

@isolation_level("AUTOCOMMIT")
def add_url(url):
    db.session.add(url)
    db.session.commit()

@isolation_level("READ COMMITTED")
def get_url_from_pool():
    short_url = freeURL.query.first()
    short_url_str = None
    if short_url != None:
        short_url_str = short_url.short_url
        db.session.delete(short_url)
    return short_url_str

@isolation_level("AUTOCOMMIT")
def get_current_id():
    number_obj = RunningURL.query.first()
    number = number_obj.current_id
    number_obj.current_id += 1
    db.session.add(number_obj)
    db.session.commit()
    return number

def delete_cache_get_long_url(code , domain):
    cache.delete_memoized(get_long_url2, code, domain)
    #cache.clear()
    # try: 
    #     cache.delete_memoized(get_long_url , code, domain)
    # except:
    #     pass

#@cache.memoize(timeout = 3600)
def get_long_url2(code, domain):
    url =  Url.query.filter_by(short_url = code , domain = domain).first() #.long_url
    if(url == None):
        return "No such url"
    url.click_count += 1
    url.added_datetime = datetime.now()
    print("hello")
    db.session.add(url)
    db.session.commit()
    return url.long_url

# @cache.memoize(timeout = 3600)
# def get_short_urls_memoize(long_url):
