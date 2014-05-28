# Copyright 2013 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import os

# xxx(orr) convert to a per-user project-oriented metadata store (created on init time)
USER_MDS_DIR = "%s/.config" % os.environ['HOME']
USER_MDS = "%s/%s" % (USER_MDS_DIR, "gcloud.MDS")

class MetadataDataStore(object):
    def __init__(self, init=False):
        # start with whatever the current state of the data are
        try:
            os.mkdir(USER_MDS_DIR)
        except:
            pass

        self._dict = {}
        if not init:
            try:
                fd = open(USER_MDS, "r")
                self._dict = json.loads(fd.read())
                fd.close()
            except IOError:
                self._dict = {}

    
    def store(self, key, value):
        # print "Store %s -> %s" % (key, value)
        self._dict[key] = value

        # xxx(orr) -- incredibly temporary
        fd = open(USER_MDS, "w")
        fd.write(json.dumps(self._dict))
        fd.close()
        

    def get(self, key, default=None):
        return self._dict.get(key, default)

    def dump(self):
        print "MDDS: "
        for key in self._dict:
            print "    %s: %s" % (key, self._dict[key])
        
