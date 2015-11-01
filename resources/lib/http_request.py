import zlib
import httplib
import urllib
import urllib2
import gzip
import StringIO
import json
from urlparse import urlparse


# POST
def post(host, url, params):
    parameters = urllib.urlencode(params)
    headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain",
               "Accept-Encoding": "gzip"}
    connection = httplib.HTTPConnection("%s:80" % host)

    connection.request("POST", url, parameters, headers)
    response = connection.getresponse()

    # Compressed (gzip) response...
    if response.getheader("content-encoding") == "gzip":
        html_gzipped_data = response.read()
        string_io = StringIO.StringIO(html_gzipped_data)
        gzipper = gzip.GzipFile(fileobj=string_io)
        html_data = gzipper.read()
    # Plain text response...
    else:
        html_data = response.read()

    # Cleanup
    connection.close()

    # Return value
    return html_data


def post_json(url, payload):
    json_payload = json.dumps(payload)
    headers = {"Content-type": "application/json; charset=UTF-8",
               "Accept": "application/json, text/javascript, */*; q=0.01",
               "Accept-Encoding": "gzip", "X-Requested-With": "XMLHttpRequest",
               "Content-Length": len(json_payload)}
    # print headers
    print "post_json: %s" % url
    print "payload: %s" % json_payload

    req = urllib2.Request(url, json_payload, headers)
    response = urllib2.urlopen(req)
    resp_info = response.info()

    # Compressed (gzip) response...
    if "Content-Encoding" in resp_info and resp_info["Content-Encoding"] == "gzip":
        html_gzipped_data = response.read()
        string_io = StringIO.StringIO(html_gzipped_data)
        gzipper = gzip.GzipFile(fileobj=string_io)
        response_data = gzipper.read()
    else:
        response_data = response.read()
    response.close()
    print response_data
    return response_data


# GET
def get(url):
    h = urllib2.HTTPHandler(debuglevel=0)
    print "get: %s" % url
    request = urllib2.Request(url)
    request.add_header("Accept-Encoding", "gzip")
    opener = urllib2.build_opener(h)
    f = opener.open(request)

    # Compressed (gzip) response...
    if f.headers.get("content-encoding") == "gzip":
        html_gzipped_data = f.read()
        string_io = StringIO.StringIO(html_gzipped_data)
        gzipper = gzip.GzipFile(fileobj=string_io)
        html_data = gzipper.read()
    # Plain text response...
    else:
        html_data = f.read()

    # Cleanup
    f.close()

    # Return value
    return html_data
