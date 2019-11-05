#!/usr/bin/python3
# -*- coding: utf-8 -*-
# -*- mode: Python -*-

"""
  ===========================================================================

  Copyright (C) 2019 Emvivre

  This file is part of VTIGER_ADMIN.

  VTIGER_ADMIN is free software: you can redistribute it and/or modify
  it under the terms of the GNU General Public License as published by
  the Free Software Foundation, either version 3 of the License, or
  (at your option) any later version.

  VTIGER_ADMIN is distributed in the hope that it will be useful,
  but WITHOUT ANY WARRANTY; without even the implied warranty of
  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
  GNU General Public License for more details.

  You should have received a copy of the GNU General Public License
  along with VTIGER_ADMIN.  If not, see <http://www.gnu.org/licenses/>.

  ===========================================================================
*/
"""

import requests
import hashlib
import json

class VTigerAdmin:
    def __init__(self, endpoint, username, access_key):
        self.endpoint = endpoint
        self.username = username
        self.s = requests.session()
        j = self.s.get('%s?operation=getchallenge&username=%s' % (self.endpoint, self.username)).json()
        access_key_md5 = hashlib.md5(bytes(j['result']['token'] + access_key, 'utf-8')).hexdigest()
        data = {
            'operation': 'login',
            'username': self.username,
            'accessKey': access_key_md5
        }
        j = self.s.post(self.endpoint, data=data).json()
        self.session_name = j['result']['sessionName']

    def list_types(self):
        j = self.s.get('%s?operation=listtypes&sessionName=%s' % (self.endpoint, self.session_name)).json()
        types_available = j['result']['types']
        return types_available

    def list_fields(self, type_name):
        j = self.s.get('%s?operation=describe&sessionName=%s&elementType=%s' % (self.endpoint, self.session_name, type_name)).json()
        fields_available = [ f['name'] for f in j['result']['fields'] ]
        return fields_available

    def get_content(self, type_name):
        j = self.s.get('%s?operation=query&sessionName=%s&query=%s' % (self.endpoint, self.session_name, 'select * from %s;' % type_name)).json()
        data = j['result']
        return data

    def get_content_from_object_id(self, object_id):
        j = self.s.get('%s?operation=retrieve&sessionName=%s&id=%s' % (self.endpoint, self.session_name, object_id)).json()
        data = j['result']
        return data

    def get_current_user_id(self):
        j = self.s.get('%s?operation=query&sessionName=%s&query=%s' % (self.endpoint, self.session_name, "select id from Users where user_name='%s';" % self.username)).json()
        user_id = j['result'][0]['id']
        return user_id

    def create_record(self, type_name, data_record):
        # check if assign id need
        fields_name_available = self.list_fields(type_name)
        if 'assigned_user_id' in fields_name_available and 'assigned_user_id' not in data_record:
            # set default assigned id : current user
            user_id = self.get_current_user_id()
            data_record[ 'assigned_user_id' ] = user_id
        data = {
            'operation': 'create',
            'sessionName': self.session_name,
            'element': json.dumps(data_record),
            'elementType': type_name,
        }
        return self.s.post(self.endpoint, data=data).json()

    def delete_record(self, object_id):
        data = {
            'operation': 'delete',
            'sessionName': self.session_name,
            'id': object_id,
        }
        return self.s.post(self.endpoint, data=data).json()

    def query(self, sql):
        j = self.s.get('%s?operation=query&sessionName=%s&query=%s' % (self.endpoint, self.session_name, sql)).json()
        data = j['result']
        return data
