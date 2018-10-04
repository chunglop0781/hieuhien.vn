# -*- coding: utf-8 -*-

"""enables to import modules through the web, by adding urls to the python path.
"""
#authors: Jure Vrscaj <jure@codeshift.net> (copyright (c) 2006-10),
#         송영진(MyEvan) <myevan_net@naver.com> (copyright (c) 2010), 
#         Alex Bodnaru <alexbodn@012.net.il> (copyright (c) 2010)

# This is free software; you may use, copy, modify and/or distribute this work
# under the terms of the MIT License.


# import these to avoid trying to import them here
import stringprep, array, unicodedata, _strptime

import sys, os, re
import imp, marshal
from tempfile import mkdtemp
from StringIO import StringIO
from gzip import GzipFile
from datetime import datetime, timedelta
from time import gmtime
from sqlite3 import connect, PARSE_DECLTYPES
from base64 import encodestring
from urlparse import urlsplit, urlunsplit
from httplib import HTTPSConnection
from urllib2 import HTTPDefaultErrorHandler, HTTPSHandler, HTTPError, \
    HTTPRedirectHandler, build_opener, urlopen, Request


DOT_PYO = ".pyo"
DOT_PYC = ".pyc"
DOT_PY = ".py"
PY_FILES = (DOT_PYO, DOT_PYC, DOT_PY)

DYN_SUFIX = [ext for ext, mode, type in imp.get_suffixes() \
             if type == 3 and ext.startswith('.')][0]


settings = sys.__dict__.setdefault('urlimport_settings',
                                   dict(
                                        py_version_string='$PYTHON_VERSION',
                                        ssl_cert='', 
                                        ssl_key='', 
                                        debug=0
                                   )
)

def config(**kwargs):
    """config(key=value) - Set key to value.
       config()          - Display settings.
    """
    settings.update(kwargs)
    for k,v in settings.iteritems():
        debug(" "+str(k)+"="+repr(v), lvl=1 )

def reset():
    """remove the cache contents"""
    cache_dir = settings.get('cache_dir', '')
    if cache_dir:
        for base, dirs, names in os.walk(cache_dir):
            for name in names:
                os.remove(os.path.join(base, name))
        for base, dirs, names in os.walk(cache_dir):
            for name in dirs:
                os.rmdir(os.path.join(base, name))
        os.rmdir(cache_dir)

def debug(s, pf='| |', lvl=1):
    if lvl <= settings.get('debug', 0):
        print ("%s %s" % (pf, s))


# use this to detect unmodified resources
# taken from http://diveintopython.org/http_web_services/etags.html
class DefaultErrorHandler(HTTPDefaultErrorHandler, HTTPRedirectHandler):

    def http_error_301(self, req, fp, code, msg, headers):
        response = \
            HTTPRedirectHandler.http_error_301(self, req, fp, code, msg, headers)
        response.status = code
        return response

    def http_error_304(self, req, fp, code, msg, headers):
        response = HTTPError(req.get_full_url(), code, msg, headers, fp)
        response.status = code
        return response

# use this to open https urls with client certificates.
# taken from http://www.osmonov.com/2009/04/client-certificates-with-urllib2.html
class HTTPSClientAuthHandler(HTTPSHandler, DefaultErrorHandler):

    def __init__(self, key, cert):
        HTTPSHandler.__init__(self)
        self.key = key
        self.cert = cert

    def https_open(self, req):
        # Rather than pass in a reference to a connection class, we pass in
        # a reference to a function which, for all intents and purposes,
        # will behave as a constructor
        return self.do_open(self.getConnection, req)

    def getConnection(self, host, timeout=300):
        return HTTPSConnection(host, key_file=self.key, cert_file=self.cert)


class UrlFinder:

    re_url_ok = re.compile(r'^http://|^ftp://|^https://')
    date_format = '%a, %d %b %Y %H:%M:%S %Z'

    def __init__(self, path):
        if self.re_url_ok.match(path):
            debug("%s: accepting '%s'." % (self.__class__.__name__, path), lvl=2)
            py_version_string = settings.get('py_version_string', None)
            if py_version_string is not None:
                path = path.replace(py_version_string, '%d.%d' % sys.version_info[:2])
            self.path = path.rstrip('/') + '/'
            debug("%s: will check for '%s'." % (self.__class__.__name__, self.path), lvl=4)
            # cache
            self.cache_dir = settings.setdefault('cache_dir', mkdtemp())
            if not os.path.exists(self.cache_dir):
                os.makedirs(self.cache_dir)
            self.cacheIndexDB = os.path.join(self.cache_dir, 'urlimport-cache.sqlite')
            indexConn = connect(self.cacheIndexDB, detect_types=PARSE_DECLTYPES)
            indexCursor = indexConn.cursor()
            table_exist = """select 1 
                             from sqlite_master 
                             where type = 'table' and name = 'module_access'
                          """
            table_create = """create table module_access(
                                module varchar(1024) 
                                    primary key on conflict replace,
                                findpath varchar(1024),
                                url varchar(1024),
                                __path varchar(1024),
                                tail varchar(12),
                                expires timestamp,
                                last_modified varchar(30),
                                etag varchar(30)
                              )
                           """
            if indexCursor.execute(table_exist).fetchone() is None:
                indexCursor.execute(table_create)
            indexConn.close()
        else:
            debug("%s: rejecting non-matching path item: '%s'" % (self.__class__.__name__, path), lvl=5)
            raise ImportError

    def find_module(self, fullname, mpath=None):
        """try to locate the remote module, do this:
         1) check in cache
         2) try to get fullname.py[oc]? from http://self.path/
         3) try to get fullname.DYN_SUFIX from http://self.path/
         4) try to get __init__.py[oc]? from http://self.path/fullname/
         5) update cache if should change
         6) load the module
        """

        debug("find_module %s" % fullname, lvl=2)
        head = self.path + fullname.split('.')[-1]
        file_types = [(ext, None) for ext in PY_FILES] + \
                     [(DYN_SUFIX, None)] + \
                     [('/__init__%s' % ext, head + '/') for ext in PY_FILES]

        cache_tested = False
        for tail, __path in file_types:
            url = head + tail

            use_cache = False
            if not cache_tested: # first time only
                cache_tested = True
                try:
                    cachedFile, fileData, url, __path, tail = \
                        self.read_cache(fullname)
                    debug('got from cache', lvl=1)
                    use_cache = True
                except Exception, e:
                    debug('error reading module %s from cache: %s' % (fullname, e), lvl=4)
                    pass
            try:
                if not use_cache:
                    debug("trying to get '%s'." % url, lvl=1)
                    fileData, cachedFile = \
                        self.caching_get_file(url, fullname, tail, __path)
                if tail.startswith('/__init__'):
                    cachedFile = None
                if url.endswith(DOT_PYO) or url.endswith(DOT_PYC):
                    debug("find_compiled_module: got '%s'." % url, lvl=1)
                    return UrlCompiledLoader(url, __path, cachedFile, fileData)
                elif url.endswith(DOT_PY):
                    debug("find_source_module: got '%s'." % url, lvl=1)
                    return UrlSourceLoader(url, __path, cachedFile, fileData)
                else:
                    debug("find_dynamic_module: got '%s'." % url, lvl=1)
                    return UrlDynamicLoader(url, cachedFile)
            except Exception, e:
                debug("find_module: failed to get '%s'. (%s)" % (url, e), lvl=3)

        debug("not_found_module %s" % fullname, lvl=2)

    def user_agent(self, url, host=None):
        if host is None:
            proto, user, passwd, host, port, path, query, fragment = \
                self.split_url(url)
        user_agent = settings.get('user_agent.%s' % url, 
                                  settings.get('user_agent.%s' % host, 
                                               settings.get('user_agent', None)))
        if user_agent is not None:
            py_version_string = settings.get('py_version_string', None)
            if py_version_string is not None:
                user_agent = user_agent.replace(py_version_string, '%d.%d' % sys.version_info[:2])
        return user_agent

    def no_cache(self, url, host=None):
        if host is None:
            proto, user, passwd, host, port, path, query, fragment = \
                self.split_url(url)
        return settings.get('no_cache.%s' % url, 
                            settings.get('no_cache.%s' % host, 
                                         settings.get('no_cache', False)))

    def cached_file(self, module, tail):
        return os.path.join(self.cache_dir, module.replace('.', os.path.sep)) + \
               tail

    def read_cache(self, module):
        indexConn = connect(self.cacheIndexDB, detect_types=PARSE_DECLTYPES)
        indexCursor = indexConn.cursor()
        select = """select last_modified, etag, url, __path, tail, expires 
                    from module_access 
                    where module = ? and findpath = ?
                 """
        delete = """delete module_access 
                    where module = ?
                 """
        modincache = indexCursor.execute(select, (module, self.path)).fetchone()
        if modincache is not None:
            last_modified, etag, url, __path, tail, expires = modincache
            cachedFile = fileData = None
            try:
                fileData, cachedFile = \
                    self.caching_get_file(url, module, tail, __path, 
                                          last_modified, etag, expires)
                indexConn.close()
                return cachedFile, fileData, url, __path, tail
            except:
                pass
            indexCursor.execute(delete, (module,))
            indexConn.commit()
            cachedFile = self.cached_file(module, tail)
            os.remove(cachedFile)
            os.removedirs(os.path.dirname(cachedFile))
        indexConn.close()
        raise Exception('module "%s" not in cache', module)

    def caching_get_file(self, url, module, tail, __path, \
                         cached_last_modified=None, cached_etag=None, \
                         expires=None):
        """get the file data using cache.
        """
        keep_cached = not_expired = \
            expires is not None and expires > datetime(*gmtime()[:6])
        if not keep_cached:
            fileData, expires, last_modified, keep_cached, etag, url = \
                self.get_file_data(url, cached_last_modified, cached_etag)
        cachedFile = self.cached_file(module, tail)
        if keep_cached: # assumes file is cached
            debug('reading data from cache %s:%s' % (module, cachedFile), lvl=2)
            fileData = open(cachedFile, "rb").read()
        if tail.endswith(DOT_PYC) or tail.endswith(DOT_PYO):
            if fileData[:4] != imp.get_magic():
                raise Exception("%s: incompatible python version" % url)
        if not_expired:
            return fileData, cachedFile

        proto, user, passwd, host, port, path, query, fragment = \
            self.split_url(url)
        no_cache = self.no_cache(url, host)
        if not no_cache or tail.endswith(DYN_SUFIX):
            path = os.path.dirname(cachedFile)
            if not os.path.exists(path):
                os.makedirs(path)
            if fileData is not None:
                open(cachedFile, "wb").write(fileData)
        else:
            cachedFile = None

        if not no_cache or keep_cached:
            indexConn = connect(self.cacheIndexDB, detect_types=PARSE_DECLTYPES)
            indexCursor = indexConn.cursor()
            select = """select 1
                        from module_access 
                        where module = ? and findpath = ?
                     """
            update = """update module_access
                        set 
                        url = ?,
                        __path = ?,
                        tail = ?,
                        expires = ?,
                        last_modified = ?,
                        etag = ?
                        where module = ? and findpath = ?
                     """
            update_cached = """update module_access
                               set 
                               url = ?,
                               expires = ?
                               where module = ? and findpath = ?
                            """
            insert = """insert into module_access
                        (url, __path, tail, expires,
                         last_modified, etag, module, findpath)
                        values(?, ?, ?, ?, ?, ?, ?, ?)
                     """
            if expires is None:
                cache_time = settings.get('cache_time.%s' % self.path, 
                                          settings.get('cache_time.%s' % host,
                                                       settings.get('cache_time', 
                                                                    None)))
                if cache_time is not None:
                    expires = datetime(*gmtime()[:6]) + cache_time
            cmd = fields = None
            if keep_cached:
                debug('updating cache expires to %s for: %s' % (expires, module), pf='|>>>>>|', lvl=2)
                cmd = update_cached
                fields = (url, expires, module, self.path)
            else:
                debug('saving %s in cache at: %s' % (module, cachedFile), pf='|>>>>>|', lvl=2)
                modincache = \
                    indexCursor.execute(select, (module, self.path)).fetchone()
                cmd = update if modincache is not None else insert
                fields = (url, __path, tail, expires, last_modified, etag, 
                          module, self.path)
            indexCursor.execute(cmd, fields)
            indexConn.commit()
            indexConn.close()

        return fileData, cachedFile

    def get_file_data(self, url, cached_last_modified, cached_etag):
        """Download the file data from given url.
        """
        proto, user, passwd, host, port, path, query, fragment = self.split_url(url)
        hostport = ':'.join([host, port]) if port else host
        url = urlunsplit((proto, hostport, path, query, fragment))
        key = settings.get('ssl_key.%s' % self.path, 
                           settings.get('ssl_key.%s' % host,
                                        settings.get('ssl_key', '')))
        cert = settings.get('ssl_cert.%s' % self.path, 
                            settings.get('ssl_cert.%s' % host,
                                         settings.get('ssl_cert', '')))
        opener = settings.get('opener.%s' % self.path, 
                              settings.get('opener.%s' % host,
                                           settings.get('opener', None)))
        request = Request(url)
        debug(cert + ',' + key, pf='|>>>>|', lvl=3)
        if opener is None:
            if proto == 'https' and cert:
                # handle http over ssl with client certificate
                opener = build_opener(HTTPSClientAuthHandler(key, cert))
            else:
                opener = build_opener(DefaultErrorHandler)
        creds = user + ':' + passwd if user and passwd else user
        if creds:
            base64string = encodestring('%s:%s' % (user, passwd))[:-1]
            authheader =  "Basic %s" % base64string
            request.add_header("Authorization", authheader)
        request.add_header('Accept-encoding', 'gzip')
        if cached_etag is not None:
            request.add_header('If-None-Match', cached_etag)
        if cached_last_modified is not None:
            request.add_header('If-Modified-Since', cached_last_modified)
        user_agent = self.user_agent(url, host)
        if user_agent is not None:
            debug("sending user agent:'%s'" % user_agent, pf='****', lvl=4)
            request.add_header('User-agent', user_agent)
        response = opener.open(request)

        if hasattr(response, 'status'):
            debug("got status %d" % response.status, pf='-----------')
            if response.status == 301: # permanent redirection
                if hasattr(response, 'url') and response.url is not None:
                    url = response.url
                    debug('redirected to: %s' % url, lvl=4)
        debug("got code %d" % response.code, pf='****', lvl=4)
        keep_cached = response.code == 304

        expires = response.info().get('Expires', None)
        etag = response.info().get('ETag', None)
        fileData = None

        if not keep_cached:
            fileData = response.read()
            debug('+++++++++ received data length %d: ' % len(fileData), lvl=4)
            if response.info().get('Content-Encoding', None) == 'gzip':
                compressedstream = StringIO(fileData)
                gzipper = GzipFile(fileobj=compressedstream)
                fileData = gzipper.read()
                debug('+++++++++ uncompressed data length %d: ' % len(fileData), lvl=4)
            default_last_modified = datetime(*gmtime()[:6]).strftime(self.date_format)
            last_modified = response.info().get('Last-Modified', default_last_modified)
        else:
            fileData = None
            last_modified = cached_last_modified

        return fileData, \
               self.parse_date(expires), \
               last_modified, \
               keep_cached, \
               etag, \
               url

    def parse_date(self, strdate):
        if strdate is None:
            return None
        try:
            return datetime.strptime(strdate, self.date_format)
        except:
            return None

    def split_url(self, url):
        scheme, netloc, path, query, fragment = urlsplit(url)
        user = passwd = port = ''
        if '@' in netloc:
            auth_part, host_part = netloc.split('@')
            netloc = host_part
            if ':' in auth_part:
                user, passwd = auth_part.split(':')
            else:
                user = auth_part
        if ':' in netloc:
            netloc, port = netloc.split(':')
        return scheme, user, passwd, netloc, port, path, query, fragment


class UrlDynamicLoader:
    def __init__(self, url, cachedFile):
        self.url = url
        self.cachedFile = cachedFile

    def load_module(self, fullname):
        """add the new module to sys.modules,
        execute its source and return it
        """
        #TODO: fails reloading
        mod = imp.load_dynamic(fullname, self.cachedFile)
#        mod.__file__ = self.url
#        mod.__loader__ = self
        return mod

class UrlSourceLoader:
    def __init__(self, url, path, cachedFile, data):
        self.url = url
        self.path = path
        self.cachedFile = cachedFile
        self.source = data.replace("\r\n", "\n").replace('\r', '\n')
        self._files = {}

    def load_module(self, fullname):
        """add the new module to sys.modules,
        execute its source and return it
        """
        if self.cachedFile is not None:
            debug('loading source module %s from %s' % (fullname, self.cachedFile), lvl=2)
            mod = imp.load_source(fullname, self.cachedFile)
            debug("after loading", lvl=4)
        else:
            mod = sys.modules.setdefault(fullname, imp.new_module(fullname))
            debug("load_module: executing %s's source..." % fullname, lvl=2)
            for line in self.source.split('\n'):
                debug(line, pf='|>|', lvl=4)

            exec self.source in mod.__dict__
            debug('source executed', lvl=4)

        mod.__file__ = self.url
        mod.__loader__ = self
        if self.path:
            mod.__path__ = [self.path]

        return mod

class UrlCompiledLoader:
    def __init__(self, url, path, cachedFile, data):
        self.url = url
        self.path = path
        self.cachedFile = cachedFile
        self.code = marshal.loads(data[8:])
        self._files = {}

    def load_module(self, fullname):
        """add the new module to sys.modules,
        execute it and return it
        """
        if self.cachedFile is not None:
            debug('loading compiled module %s from %s' % (fullname, self.cachedFile), lvl=-2)
            try:
                mod = imp.load_compiled(fullname, self.cachedFile)
            except Exception, e:
                debug('error %s loading %s' % (e, self.cachedFile), lvl=-2)
                raise
        else:
            mod = sys.modules.setdefault(fullname, imp.new_module(fullname))
            debug("load_module: executing %s's code..." % fullname, lvl=2)
            debug(repr(self.code), pf='|>|', lvl=4)

            exec self.code in mod.__dict__

            debug(repr(mod), pf='|>|', lvl=4)

        mod.__file__ = self.url
        mod.__loader__ = self
        if self.path:
            mod.__path__ = [self.path]

        return mod

