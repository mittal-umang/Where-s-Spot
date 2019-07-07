from django.http import HttpResponse
from django.template import loader
from django.core.files.storage import FileSystemStorage


def index(request):
    template = loader.get_template('wheresspot/index.html')
    title = "Where's Spot?"
    context = {'title': title}
    if request.POST and request.FILES['myfile']:
        myfile = request.FILES['myfile']
        fs = FileSystemStorage()
        if not fs.exists(myfile.name):
            filename = fs.save(myfile.name, myfile)
            uploaded_file_url = fs.url(filename)
            context['uploaded_file_url'] = uploaded_file_url

    return HttpResponse(template.render(context, request))
