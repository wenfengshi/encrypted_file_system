import client
import sys
sys.path.insert(0, '/home/henchill/Documents/Workspace/encrypted_file_system/server')

from server import *
from encrypt import *

if __name__ == "__main__":
 	
    resp = client.signIn('aakriti')
    print "RESPONSE REGISTER: ", resp

    resp = client.setPerm('foo', 'rw', ['henchill'])

    resp = client.createDirectory("foo")
    print "RESPONSE CREATE_DIR: ", resp

    resp = client.createFile("foo/test.txt")
    print "RESPONSE CREATE_FILE1: ", resp

    resp = client.createFile("foo/test2.txt")
    print "RESPONSE CREATE_FILE2: ", resp

    resp = client.createFile("test3.txt")
    print "RESPONSE CREATE_FILE3", resp

    resp = client.setPerm('test3.txt', 'rw', ['henchill'])
    resp = client.setPerm('foo/test.txt', 'rw', ['henchill'])
    print "RESPONSE SETPERM: ", resp