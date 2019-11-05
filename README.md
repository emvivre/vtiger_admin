# vtiger_admin
Vtiger Admin is a tiny python script to administrate vtiger CRM using the webservice.php endpoint. The primary motivation to create this script was to import and export easily arbitrary data to and from Vtiger CRM. The .json format is used to interact with the Vtiger Admin script.

Available features are the following : 
 - import data from a .json format
 - export data to a .json format
 - create / delete a record
 - list available types (categories)
 - list fields associated to a type name

To display the help message: 
```
$ python3 vtiger_admin.py 
Usage: vtiger_admin.py -c <CMD> [<OPTIONS>]
<CMD> :
   types : get all types name
   fields : get all fields name : -t <TYPE>
   create : create a record : -t <TYPE> -d '<JSON_DATA>'
   delete : delete a record : -i <OBJECT_ID>
   export : export content of type or id : -t <TYPE> | -i <OBJECT_ID>
   import : import content stdin : -t <TYPE>

ex:
   python3 vtiger_admin.py -c types
   python3 vtiger_admin.py -c fields -t Contacts
   python3 vtiger_admin.py -c create -t Accounts -d '{"accountname":"CompanyTest2","website":"https://companytest2.com"}'
   python3 vtiger_admin.py -c delete -i 11x4
   python3 vtiger_admin.py -c export -t Accounts > accounts.json
   python3 vtiger_admin.py -c export -t ModComments
   cat contacts.json | python3 vtiger_admin.py -c import -t Contacts
   echo '[{"firstname":"F0","lastname":"B0","accountname":"C0"}]' | python3 vtiger_admin.py -c import -t Contacts
```

Per instance, to display available types:
```
python3 vtiger_admin.py -c types
[
  "Campaigns",
  "Vendors",
  "Faq",
  "Quotes",
  "PurchaseOrder",
  "SalesOrder",
  "Invoice",
  "PriceBooks",
  "Calendar",
  "Accounts",
  "Contacts",
  "Potentials",
  "Products",
  "Documents",
  "Emails",
  "HelpDesk",
  "Events",
  "Users",
  "Services",
  "ServiceContracts",
  "PBXManager",
  "ProjectMilestone",
  "ProjectTask",
  "Project",
  "SMSNotifier",
  "ModComments",
  "Assets",
  "Groups",
  "Currency",
  "DocumentFolders",
  "CompanyDetails",
  "LineItem",
  "Tax",
  "ProductTaxes"
]
```

With this smart script, you can easily display and delete arbitrary comments : 
```
$ python3 vtiger_admin.py -c export -t ModComments
[
  {
    "commentcontent": "Hello World",
    "assigned_user_id": "19x1",
    "createdtime": "2019-11-05 13:21:37",
    "modifiedtime": "2019-11-05 13:21:37",
    "related_to": "11x14",
    "creator": "19x1",
    "parent_comments": "",
    "source": "CRM",
    "customer": "",
    "userid": "",
    "reasontoedit": "",
    "is_private": "0",
    "filename": "0",
    "related_email_id": "0",
    "id": "31x18"
  },
  {
    "commentcontent": "Please delete this message",
    "assigned_user_id": "19x1",
    "createdtime": "2019-11-05 13:21:59",
    "modifiedtime": "2019-11-05 13:21:59",
    "related_to": "11x14",
    "creator": "19x1",
    "parent_comments": "",
    "source": "CRM",
    "customer": "",
    "userid": "",
    "reasontoedit": "",
    "is_private": "0",
    "filename": "0",
    "related_email_id": "0",
    "id": "31x19"
  }
]

$ python3 vtiger_admin.py -c delete -i 31x19
{'success': True, 'result': {'status': 'successful'}}

$ python3 vtiger_admin.py -c export -t ModComments
[
  {
    "commentcontent": "Hello World",
    "assigned_user_id": "19x1",
    "createdtime": "2019-11-05 13:21:37",
    "modifiedtime": "2019-11-05 13:21:37",
    "related_to": "11x14",
    "creator": "19x1",
    "parent_comments": "",
    "source": "CRM",
    "customer": "",
    "userid": "",
    "reasontoedit": "",
    "is_private": "0",
    "filename": "0",
    "related_email_id": "0",
    "id": "31x18"
  }
]
```
