#-*- coding:utf-8 -*-
import datetime
from flask import g, session, request, redirect

from rrd import app
from rrd.view.utils import get_usertoken_from_session, get_current_user_profile

@app.template_filter('fmt_time')
def fmt_time_filter(value, pattern="%Y-%m-%d %H:%M"):
    if not value:
        return ''
    return datetime.datetime.fromtimestamp(value).strftime(pattern)

@app.teardown_request
def app_teardown(exception):
    from rrd.store import db
    db.commit()

@app.before_request
def app_before():
    g.user_token = get_usertoken_from_session(session)
    g.user = get_current_user_profile(g.user_token)

    path = request.path
    if not g.user and not path.startswith("/auth/login") and not path.startswith("/static/"):
        return redirect("/auth/login")

    if path.startswith("/screen"):
        g.nav_menu = "nav_screen"
    elif path.startswith("/portal/hostgroup"):
        g.nav_menu = "p_hostgroup"
    elif path.startswith("/portal/template"):
        g.nav_menu = "p_template"
    elif path.startswith("/portal/expression"):
        g.nav_menu = "p_expression"
    elif path.startswith("/portal/nodata"):
        g.nav_menu = "p_nodata"
    elif path.startswith("/portal/alarm-dash"):
        g.nav_menu = "p_alarm-dash"
    else:
        g.nav_menu = "nav_dashboard"
