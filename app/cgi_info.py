#!/usr/bin/env python

import os, cgi, cgitb

# Settings were made accordingly to http://con.appspot.com/console/help/integration

# Set this to true if you want to hide the console from non-authorized users
# by returning HTTP 404 (file not found), instead of the normal behavior.
hide_from_invalid_users = True

# In production mode, only administrators may use the console. However, if you
# really want to allow any regular logged-in user to use the console, you can
# set this variable to True.
allow_any_user = False

# In production mode (hosted at Google), anonymous users may not use the console.
# But in development mode, anonymous users may.  If you still want to disallow
# anonymous users from using the console from the development SDK, set this
# variable to True.
require_login_during_development = False



development = os.environ.get('SERVER_SOFTWARE', '').lower().startswith('development')

if development and not require_login_during_development:
    authorized = True
else:
    authorized = False

    from google.appengine.api import users

    if users.get_current_user() and (allow_any_user or users.is_current_user_admin()):
        authorized = True
    elif hide_from_invalid_users:
        print 'Status: 404 Not Found'
    else:
        print 'Status: 302 Found'
        print 'Location: %s' %  users.create_login_url(os.environ.get('PATH_INFO', '/'))


if authorized:

    cgitb.enable()

    print 'Content-Type: text/html'
    print                         

    print '<!doctype html>'
    print '<html>'
    print '<head>'
    print '<title>Request info</title>'
    print '</head>'
    print '<body>'
    print '<h1>Request info</h1>'
    print

    cgi.test()

    print
    print '<h3>OS Environment:</h3>'
    print '<dl>'
    print '\n'.join([ '<dt> %s <dd> %s' % (k, cgi.escape(os.environ[k])) for k in sorted(os.environ) ])
    print '</dl>'
    print
    print '</body>'
    print '</html>'
