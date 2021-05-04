from django.http import HttpResponse
from django.views import View

class SessionView(View):
    def get(self, request):
        session = str(self.request.session.session_key)
        cookie = str(request.COOKIES.get('csrftoken'))
        return HttpResponse('<b>Session: </b>' + session + ' <br />' + '<b>Cookie: </b>' + cookie)
