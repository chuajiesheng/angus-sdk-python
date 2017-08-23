#! /usr/bin/env python
# -*- coding: utf-8 -*-

# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.

import angus.client
import time

__updated__ = "2017-01-02"
__author__ = "Gwennael Gate"
__copyright__ = "Copyright 2015-2017, Angus.ai"
__credits__ = ["Aurélien Moreau", "Gwennael Gate"]
__license__ = "Apache v2.0"
__maintainer__ = "Aurélien Moreau"
__status__ = "Production"


def async_res(job):
    # Print the result of the job.
    print(job.result['faces'])

def main():
    # Get the conn resource of Angus Cloud
    conn = angus.client.connect()

    # Get the service 'face_detection' in version 1
    service = conn.services.get_service('face_detection', version=1)

    # Submit a new job to the service, and get the result asynchronously
    job = service.process({'image': open('macgyver.jpg')}, callback=async_res)

    # Wait for the asynchronous result to be printed
    time.sleep(10)


if __name__ == '__main__':
    main()
