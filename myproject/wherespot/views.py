from django.http import HttpResponse
from django.template import loader
from django.core.files.storage import FileSystemStorage
import os
from google.cloud import storage
import tensorflow.compat.v1 as tf
tf.disable_v2_behavior()


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
            context = to_model(uploaded_file_url_find_breed, context=context)

    # if request.POST and request.FILES.get('findDog',False):
    #     find_dog = request.FILES['findDog']
    #     if not fs.exists(find_dog.name):
    #         find_dog_name = fs.save(find_dog.name, find_dog)
    #         uploaded_file_url_find_dog = fs.url(find_dog_name)
    #

    if request.POST and request.FILES.get('lostDog', False):
        lost_dog = request.FILES['lostDog']
        if not fs.exists(lost_dog.name):
            lost_dog_name = fs.save(lost_dog.name, lost_dog)
            uploaded_file_url_lost_dog = fs.url(lost_dog_name)
            to_cloud(url=uploaded_file_url_lost_dog)

    return HttpResponse(template.render(context, request))


def to_model(url, context):
    # print("hello,world from to_model ", str(os.getcwd() + os.path.abspath(url)))
    actual_path = str(os.getcwd() + os.path.abspath(url))
    saver = tf.train.Saver()
    with tf.Session() as sess:
        saver.restore(sess,'/home/umang.mittal/Where-s-Spot/myproject/wherespot/recon_model.ckpt')

    context["popup_active"] = True

    return context


def to_cloud(url):
    os.environ[
        "GOOGLE_APPLICATION_CREDENTIALS"] = "/Users/umang.mittal/Where-s-Spot/myproject/wherespot/credentials.json"
    file_name = str(os.getcwd() + os.path.abspath(url))
    storage_client = storage.Client()
    bucket = storage_client.get_bucket('regal-subject-244800.appspot.com')
    blob = bucket.blob(url)
    blob.upload_from_filename(file_name)
