from django.http import HttpResponse
from django.views import View

class SessionView(View):
    def get(self, request):
        session = self.request.session.session_key
        return HttpResponse(session)
