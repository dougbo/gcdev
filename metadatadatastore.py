
import json
import os

# xxx(orr) convert to a per-user metadata store (created on init time)
USER_MDS_DIR = "%s/.config" % os.environ['HOME']
USER_MDS = "%s/%s" % (USER_MDS_DIR, "gcloud.MDS")

class MetadataDataStore(object):
    def __init__(self):
        # start with whatever the current state of the data are
        try:
            os.mkdir(USER_MDS_DIR)
        except:
            pass
        try:
            fd = open(USER_MDS, "r")
            self._dict = json.loads(fd.read())
            fd.close()
        except IOError:
            pass
    
    def store(self, key, value):
        print "Store %s -> %s" % (key, value)
        self._dict[key] = value

        # xxx(orr) -- incredibly temporary
        fd = open(USER_MDS, "w")
        fd.write(json.dumps(self._dict))
        fd.close()
        

    def get(self, key):
        return dict.get(key, None)
        
