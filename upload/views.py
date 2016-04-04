from django.shortcuts import render
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
from PDFUpload import settings
import os
import random, string


def randomword(length):
   return ''.join(random.choice(string.lowercase + string.uppercase + string.digits) for i in range(length))

# Create your views here.

def index(request):
    return render_to_response('index.html', locals())


@csrf_exempt
def upload(request):
    filename = ""
    if request.method == 'POST':
        filename = save_file(request.FILES['file'], 'drop-pdf')
    return HttpResponse(filename)

def drop(request):
    if 'filename' in request.GET:
        file_path = "%s/%s" % (settings.BASE_DIR + '/upload/' + settings.STATIC_URL + 'drop-pdf', request.GET['filename'])
        os.remove(file_path)

    return HttpResponse("")


def save_file(file, path=''):
    temp = settings.BASE_DIR + '/upload/' + settings.STATIC_URL + str(path)
    print temp

    if not os.path.exists(temp):
        os.makedirs(temp)

    filename = file._get_name()
    filename = '.'.join(filename.split('.')[:-1]) + "-" + randomword(5) + '.pdf'

    fd = open('%s/%s' % (temp, str(filename)), 'wb')
    for chunk in file.chunks():
        fd.write(chunk)
    fd.close()

    return filename;
