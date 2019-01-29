from datetime import datetime, timedelta
from flask import session, redirect, url_for, request, Response, jsonify
from . import api
from .decorators import isolation_level
from .. import db, hashing, cache, celery, mail
from .url import Url
from .runningurl import RunningURL
from .freeurl import freeURL
import redis
from flask_mail import Message
from .constants import defaultURL
from .data import * #get_long_url, get_short_urls, add_url
from .algorithms import encode, make_url
import json

@api.route('/get-long-urls', methods = ['GET'])
#@cache.memoize(3600)
def getLongUrls():
    if request.method == 'GET':
        json = request.get_json()
        given_url = json['url']
        short_url = given_url.split('/')
        if len(short_url) != 2:
            return "Invalid Url"
        long_url = get_long_url(code = short_url[1], domain = short_url[0])
        if(long_url == "No such url"):
            print("Hello")
            delete_cache_get_long_url(code = short_url[1], domain = short_url[0])
        return jsonify(long_url)

@api.route('/get-short-url', methods = ['POST'])
def getShortUrl():
    json = request.get_json()
    domain_name = defaultURL

    if 'url' not in json:
        return 'Invalid request: Should have a url field'


    long_url = json['url']

    if 'domain' in json:
        domain_name = json['domain']

    short_urls = get_short_urls(long_url)
    short_urls_with_same_domain = [x for x in short_urls if x.domain == domain_name]


    if len(short_urls_with_same_domain) != 0:
        return make_url(short_urls_with_same_domain[0])
    elif len(short_urls)!=0 and len(short_urls_with_same_domain)==0:
        short_url = short_urls[0]
        if domain_name!=short_url.domain:
            new_url = Url(long_url = long_url, short_url = short_url.short_url, domain = domain_name, added_datetime=datetime.now(), hash_long_url = short_url.hash_long_url, click_count = 0)
            add_url(new_url)
            return make_url(new_url)
        return make_url(short_url)
    
    short_url_str = get_url_from_pool() #freeURL.query.first()
    
    if short_url_str==None:
        number = get_current_id()
        short_url_str = encode(number)

    new_url = Url(long_url=long_url, short_url = short_url_str, domain = domain_name, added_datetime = datetime.now(), hash_long_url = hashing.hash_value(long_url), click_count = 0)
    add_url(new_url)

    return jsonify(make_url(new_url))

@api.route('/delete-expired/<days>', methods = ["GET"])
@isolation_level("AUTOCOMMIT")
#@celery.task
def delete_expired_urls(days):
    if(days == 0):
        result = Url.query.all()
    else:
        yesterday = datetime.now() - timedelta(days = int(days))
        result = Url.query.filter(Url.added_datetime < yesterday).all()
        
    if(result == None):
        return "Nothing to delete"
    for row in result:
        fu = freeURL(short_url = row.short_url)
        db.session.add(fu)
        db.session.commit()
    
    deleted_long_urls = [x.long_url for x in result]
    num_urls = len(deleted_long_urls)
    deleted_long_urls = "\n".join(deleted_long_urls)
    # msg = Message('deleted_long_urls', recipients='naitik.dodia@proptiger.com', sender='naitik.dodia@gmail.com')
    # msg.body = deleted_long_urls
    # mail.send(msg)
    for row in result:
        db.session.delete(row)
    db.session.commit()
    return jsonify(num_urls)

@api.route('/served-clicks', methods = ["GET"])
def served_clicks():
    urls = Url.query.all()
    if (urls == None):
        return "No report as no records exist"
    short_url_clicks = {}
    count_total_clicks = 0
    for row in urls:
        short_url_clicks[str(make_url(row))] = row.click_count
        count_total_clicks += row.click_count

    short_url_clicks['TOTAL CLICKS'] = count_total_clicks
    resp = jsonify(short_url_clicks)
    resp.status_code = 200
    print(resp)
    return resp, 200