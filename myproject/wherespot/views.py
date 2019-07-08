from django.http import HttpResponse
from django.template import loader
from django.core.files.storage import FileSystemStorage
import boto3
import os


def index(request):
    template = loader.get_template('wheresspot/index.html')
    title = "Where's Spot?"
    context = {'title': title}
    fs = FileSystemStorage()
    print("request received")
    print(request.content_params)

    if request.POST and request.FILES.get('findBreed', False):
        myfile = request.FILES['findBreed']
        if not fs.exists(myfile.name):
            filename = fs.save(myfile.name, myfile)
            uploaded_file_url_find_breed = fs.url(filename)
            context['uploaded_file_url'] = uploaded_file_url_find_breed
            to_model(uploaded_file_url_find_breed)

    # if request.POST and request.FILES.get('findDog',False):
    #     find_dog = request.FILES['findDog']
    #     if not fs.exists(find_dog.name):
    #         find_dog_name = fs.save(find_dog.name, find_dog)
    #         uploaded_file_url_find_dog = fs.url(find_dog_name)
    #
    # if request.POST and request.FILES.get('lostDog',False):
    #     lost_dog = request.FILES['lostDog']
    #     if not fs.exists(lost_dog.name):
    #         lost_dog_name = fs.save(lost_dog.name, lost_dog)
    #         uploaded_file_url_lost_dog = fs.url(lost_dog_name)

    return HttpResponse(template.render(context, request))


#
# def to_s3(url):
#     s3 = boto3.client()
#     return "hello"


def to_model(url):
    print("hello,world from to_model ", str(os.getcwd() + os.path.abspath(url)))
# TODO Send image URL to image recognition code
