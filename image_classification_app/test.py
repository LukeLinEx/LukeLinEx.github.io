from sys import argv
from cStringIO import StringIO
import sys
from tensorflow.models.image.imagenet.classify_image import run_inference_on_image
script, file_name = argv


old_stdout = sys.stdout
sys.stdout = mystdout = StringIO()

run_inference_on_image(file_name)

sys.stdout = old_stdout

print 1

f = open('result.txt', 'w')
f.write(mystdout.getvalue())
f.close()