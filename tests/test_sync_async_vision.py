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

import datetime
import io
import time

import pytest

import angus.client
from angus.client.rest import Resource
import fake_camera


__updated__ = "2017-08-23"
__author__ = "Gwennael Gate"
__copyright__ = "Copyright 2015-2017, Angus.ai"
__credits__ = ["Aurélien Moreau", "Gwennael Gate", "Raphaël Lumbroso"]
__license__ = "Apache v2.0"
__maintainer__ = "Aurélien Moreau"
__status__ = "Production"

IMG_1 = 'Angus-6.jpg'
IMG_3 = 'Angus-24.jpg'
IMG_LARGE = 'large.jpg'

SERVICES=["scene_analysis",
          "upper_body_detection",
          "age_and_gender_estimation",
          "face_expression_estimation",
          "face_detection",
          "gaze_analysis",
          "motion_detection",
          "qrcode_decoder",
          "dummy"
          ]

@pytest.fixture(scope="module", params=SERVICES)
def service_name(request):
    return request.param

@pytest.fixture(scope="module")
def root(server, client, token, verify):
    return angus.client.connect(
        url=server, client_id=client, access_token=token, verify=verify)

@pytest.fixture(scope="module")
def service(root, service_name):
    return root.services.get_service(service_name, version=1)


@pytest.fixture(scope="module")
def image_res(root):
    return root.blobs.create(open(IMG_1, 'rb'))


@pytest.fixture(scope="module")
def image_res_3(root):
    return root.blobs.create(open(IMG_3, 'rb'))


@pytest.fixture(scope="module")
def session(service):
    return service.create_session()


def check_result_res(result_res, howmany=1):
    isinstance(result_res, Resource)
    assert result_res.status == Resource.CREATED
    assert result_res.representation == result_res.result


def check_result_res_eventually(result_res, howmany=1):
    isinstance(result_res, Resource)

    if result_res.status == Resource.ACCEPTED:
        time.sleep(10)
        result_res.fetch()

    check_result_res(result_res, howmany)


def check_result_res_none(result_res):
    assert result_res == None


def test_connect(server, client, token, verify, service_name):
    conn = angus.client.connect(
        url=server,
        client_id=client,
        access_token=token,
        verify=verify)
    service = conn.services.get_service(service_name, version=1)
    assert service is not None


def test_embedded_sync_client_sync_server(service):
    result_res = service.process(
        parameters={
            'image': open(IMG_1, 'rb')},
        async=False)
    check_result_res(result_res)


def test_embedded_sync_client_async_server(service):
    result_res = service.process(
        parameters={
            'image': open(IMG_1, 'rb')},
        async=True)
    check_result_res_eventually(result_res)


def test_embedded_async_client_sync_server(service):
    result_res_fut = service.process_async(
        parameters={
            'image': open(IMG_1, 'rb')},
        async=False)
    res = result_res_fut.result()
    check_result_res(res)

def test_embedded_async_client_async_server(service):
    result_res_fut = service.process_async(
        parameters={
            'image': open(IMG_1, 'rb')},
        async = True)
    res = result_res_fut.result()
    check_result_res_eventually(res)


def test_embedded_async_client_2(service):
    result_res_fut = service.process_async(
        parameters={
            'image': open(IMG_3, 'rb')},
        async=False)
    res = result_res_fut.result()
    check_result_res(res, 3)


def test_default_session(service):
    service.enable_session()
    camera = fake_camera.Camera("./video1")
    dt = datetime.timedelta(seconds=0.1)
    date = datetime.datetime.now()
    while camera.has_next():
        img = io.BytesIO(camera.next())
        result_res = service.process(
            parameters={
                'image': img,
                'timestamp': date.isoformat(),
            })
        date = date + dt
        check_result_res_eventually(result_res)

    service.disable_session()
