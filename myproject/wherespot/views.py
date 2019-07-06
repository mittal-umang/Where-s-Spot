from django.http import HttpResponse
from django.template import loader


def index(request):
    template=loader.get_template('wherespot/index.html')
    title = "Where's Spot?"
    context={'title':title}
    return HttpResponse(template.render(context,request))
