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

import time

import pytest

import angus

__updated__ = "2015-05-29"
__author__ = "Aurélien Moreau"
__copyright__ = "Copyright 2015, Angus.ai"
__credits__ = ["Aurélien Moreau", "Gwennael Gate"]
__license__ = "Apache v2.0"
__maintainer__ = "Aurélien Moreau"
__status__ = "Production"

IMG_1 = 'Angus-6.jpg'


@pytest.fixture(scope="module")
def root():
    return angus.connect()


@pytest.fixture(scope="module")
def all_services(root):
    return root.services.get_services()


@pytest.fixture(scope="module")
def select_services(root):
    return root.services.get_services(['face_detection', 'dummy'])


@pytest.fixture(scope="module")
def select_version_services(root):
    return root.services.get_services([('face_detection', 1), ('dummy', 1)])


@pytest.fixture(scope="module")
def image_res(root):
    return root.blobs.create(open(IMG_1))


def check_result_res(result_res, howmany=1):
    isinstance(result_res, angus.rest.Resource)
    assert result_res.status == 200
    assert result_res.representation == result_res.result
    assert 'composite' in result_res.representation


def check_result_res_eventually(result_res, howmany=1):
    isinstance(result_res, angus.rest.Resource)

    if result_res.status == angus.rest.Resource.ACCEPTED:
        time.sleep(10)
        result_res.fetch()

    check_result_res(result_res, howmany)


def delegate(service, image):
    result_res = service.process(
        parameters={
            'image': image},
        callback=check_result_res)
    check_result_res_eventually(result_res)


def test_embeded_all(all_services):
    delegate(all_services, open(IMG_1))


def test_href_all(all_services, image_res):
    delegate(all_services, image_res)


def test_embeded_select(select_services):
    delegate(select_services, open(IMG_1))


def test_href_select(select_services, image_res):
    delegate(select_services, image_res)


def test_embeded_select_version(select_version_services):
    delegate(select_version_services, open(IMG_1))


def test_href_select_version(select_version_services, image_res):
    delegate(select_version_services, image_res)