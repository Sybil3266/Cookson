from collections import deque
from datetime import datetime, timedelta
from django.shortcuts import redirect
from django.conf import settings
from django.contrib import auth
from .__init__ import prelabel, originlabel


class AutoLogout(object):
  def __init__(self, get_response):
    self.get_response = get_response

  def __call__(self, request):
      self.process_request(request)
      response = self.get_response(request)
      return response

  def process_request(self, request):
    if request.user is None :
      #Can't log out if not logged in
      return

    try:
      if datetime.now() - request.session['last_touch'] > timedelta( 0, settings.AUTO_LOGOUT_DELAY * 60, 0):
        print( request.user.username +" USER LOGOUT")
        auth.logout(request)
        prelabel = originlabel.copy()
        del request.session['last_touch']
        return redirect('/')
    except KeyError:
      pass

    request.session['last_touch'] = datetime.now()