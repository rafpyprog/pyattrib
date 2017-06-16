import os
import subprocess
from subprocess import PIPE
import sys

sys.getfilesystemencoding()



TEST_DIR = os.path.join(os.getcwd(), 'test_rules')
attributes = ['A', 'H', 'R', 'S']
os.mkdir(TEST_DIR)

cmd = subprocess.run(['attrib', '+h', TEST_DIR], stderr=PIPE, stdout=PIPE)
cmd.stderr
cmd = subprocess.run(['attrib', '+s', TEST_DIR], stderr=PIPE, stdout=PIPE)
cmd.stderr
cmd.stdout

os.popen('attrib -h -a -r -s {}'.format(TEST_DIR)).read()
os.popen('attrib {}'.format(TEST_DIR)).read()

''' S '''
os.popen('attrib +s {}'.format(TEST_DIR)).read()
os.popen('attrib +a {}'.format(TEST_DIR)).read()
os.popen('attrib +r {}'.format(TEST_DIR)).read()
os.popen('attrib +h {}'.format(TEST_DIR)).read()
os.popen('attrib -s {}'.format(TEST_DIR)).read()
os.popen('attrib {}'.format(TEST_DIR)).read()

'''A '''
os.popen('attrib +a {}'.format(TEST_DIR)).read()
os.popen('attrib +r {}'.format(TEST_DIR)).read()
os.popen('attrib +s {}'.format(TEST_DIR)).read()
os.popen('attrib +h {}'.format(TEST_DIR)).read()
os.popen('attrib -h -a -r -s {}'.format(TEST_DIR)).read()


'''R '''
os.popen('attrib +r {}'.format(TEST_DIR)).read()
os.popen('attrib +a {}'.format(TEST_DIR)).read()
os.popen('attrib +h {}'.format(TEST_DIR)).read()

os.popen('attrib +r {}'.format(TEST_DIR)).read()
os.popen('attrib +s {}'.format(TEST_DIR)).read()
os.popen('attrib -s {}'.format(TEST_DIR)).read()

os.popen('attrib -h -a -r -s {}'.format(TEST_DIR)).read()
os.popen('attrib {}'.format(TEST_DIR)).read()


if self.is_hidden

''' H '''
os.popen('attrib +h {}'.format(TEST_DIR)).read()
os.popen('attrib +r {}'.format(TEST_DIR)).read()
os.popen('attrib +a {}'.format(TEST_DIR)).read()
os.popen('attrib +s {}'.format(TEST_DIR)).read()
os.popen('attrib -h -a -r -s {}'.format(TEST_DIR)).read()
os.popen('attrib +h +a {}'.format(TEST_DIR)).read()

def test(*args):
    print(args)

test("")
