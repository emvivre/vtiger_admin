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


import vtiger
import sys
import json

VTIGER_ENPOINT = 'http://localhost/emvivre/vtigercrm/webservice.php'
VTIGER_USERNAME = 'admin'
VTIGER_ACCESSKEY = 'xND4DIvOivgtxVrg'

if len(sys.argv) < 2:
    print('''Usage: %(scriptname)s -c <CMD> [<OPTIONS>]
<CMD> :
   types : get all types name
   fields : get all fields name : -t <TYPE>
   create : create a record : -t <TYPE> -d '<JSON_DATA>'
   delete : delete a record : -i <OBJECT_ID>
   export : export content of type or id : -t <TYPE> | -i <OBJECT_ID>
   import : import content stdin : -t <TYPE>

ex:
   python3 %(scriptname)s -c types
   python3 %(scriptname)s -c fields -t Contacts
   python3 %(scriptname)s -c create -t Accounts -d '{"accountname":"CompanyTest2","website":"https://companytest2.com"}'
   python3 %(scriptname)s -c delete -i 11x4
   python3 %(scriptname)s -c export -t Accounts > accounts.json
   python3 %(scriptname)s -c export -t ModComments
   cat contacts.json | python3 %(scriptname)s -c import -t Contacts
   echo '[{"firstname":"F0","lastname":"B0","accountname":"C0"}]' | python3 %(scriptname)s -c import -t Contacts
''' % {'scriptname': sys.argv[0]})
    quit(1)

if len(sys.argv) % 2 != 1:
    print('ERROR: invalid argument given !')
    quit(1)



arguments = {}
for i in range(1,len(sys.argv),2):
    (k,v) = (sys.argv[i],sys.argv[i+1])
    arguments[k] = v

if '-c' not in arguments:
    print('ERROR: no cmd indicated !')
    quit(1)
cmd_name = arguments['-c']

v = vtiger.VTigerAdmin(VTIGER_ENPOINT, VTIGER_USERNAME, VTIGER_ACCESSKEY)

if cmd_name == 'types':
    types_name = v.list_types()
    j = json.dumps(types_name, indent=2)
    print(j)
elif cmd_name == 'fields':
    if '-t' not in arguments:
        print('ERROR: please set a type name !')
        quit(1)
    type_name = arguments['-t']
    fields_name = v.list_fields(type_name)
    j = json.dumps(fields_name, indent=2)
    print(j)
elif cmd_name == 'export':
    if '-t' in arguments:
        type_name = arguments['-t']
        content = v.get_content(type_name)
        j = json.dumps(content, indent=2)
        print(j)
    elif '-i' in arguments:
        object_id = arguments['-i']
        content = v.get_content_from_object_id(object_id)
        j = json.dumps(content, indent=2)
        print(j)
    else:
        print('ERROR: please set either a type name or an object id !')
        quit(1)
elif cmd_name == 'create':
    if '-t' not in arguments:
        print('ERROR: please set a type name !')
        quit(1)
    type_name = arguments['-t']
    if '-d' not in arguments:
        print('ERROR: please set data record !')
        quit(1)
    data_record_str = arguments['-d']
    data_record = json.loads(data_record_str)
    j = v.create_record(type_name, data_record)
    print(j)
elif cmd_name == 'delete':
    if '-i' not in arguments:
        print('ERROR: please set an object id !')
        quit(1)
    object_id = arguments['-i']
    j = v.delete_record( object_id )
    print(j)
elif cmd_name == 'import':
    if '-t' not in arguments:
        print('ERROR: please set a type name !')
        quit(1)
    type_name = arguments['-t']
    json_str = sys.stdin.read()
    data = json.loads(json_str)
    print('Adding %d records ...' % len(data))
    for data_record in data:
        # patch for import Contacts : seek Accounts id from accountname
        if type_name == 'Contacts' and 'accountname' in data_record:
            data_record['account_id'] = v.query("select id from Accounts where accountname='%s';" % data_record['accountname'])[0]['id']
            del data_record['accountname']
        j = v.create_record(type_name, data_record)
        print(j)
else:
    print('ERROR: unknown command given !')
    quit(1)
