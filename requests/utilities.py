from datetime import datetime
import os

def rename_image(instance, filename):
    ext = filename.split('.')[-1]
    new_filename = "%s %s-%s-%s.%s" % (datetime.now().date(), datetime.now().time().hour, datetime.now().time().minute, datetime.now().time().second, ext)
    return os.path.join('images', new_filename)