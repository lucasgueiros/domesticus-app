from django.core.management.base import BaseCommand, CommandError
from financas.models import Account, Transaction, Entry
from xml.dom import minidom
from datetime import datetime

class Command(BaseCommand):
        help = 'Importar arquivo do gnucash'
        
        def add_arguments (self, parser):
            parser.add_argument('file', nargs='+', type=str)
        
        def handle (self, *args, **options):
            print(options['file'])
            file = minidom.parse(options['file'][0])
            
#<gnc:account version="2.0.0">
#   <act:name>Ativos</act:name>
#   <act:id type="guid">0c21f13ed05b4e77952554df644c9d34</act:id>
#   <act:type>ASSET</act:type>
#   <act:commodity>
#       <cmdty:space>CURRENCY</cmdty:space>
#       <cmdty:id>BRL</cmdty:id>
#   </act:commodity>
#   <act:commodity-scu>100</act:commodity-scu>
#   <act:description>Ativos</act:description>
#   <act:parent type="guid">fdb9f59ccbd240678bbd7eb591db7303</act:parent>
#</gnc:account>
            root_account_id = 0
            accounts_without_parent = {}
            accounts_dict = {}

            accounts = file.getElementsByTagName('gnc:account')
            for account_xml in accounts:
                name = account_xml.getElementsByTagName('act:name')[0].firstChild.data
                id = account_xml.getElementsByTagName('act:id')[0].firstChild.data
                if name == 'Root Account':
                    root_account_id = id
                else:
                    parent_id = account_xml.getElementsByTagName('act:parent')[0].firstChild.data
                    if parent_id in accounts_dict:
                        parent = accounts_dict[parent_id]
                        account = Account(
                            name = name,
                            parent = parent,
                        )
                        account.save()
                        accounts_dict[id] = account
                    elif parent_id in accounts_without_parent:
                        parent = accounts_without_parent[parent_id]
                        account = Account(
                            name = name,
                            parent = parent,
                        )
                        account.save()
                        accounts_dict[id] = account
                    elif parent_id == root_account_id:
                        account = Account(
                            name = name,
                        )
                        account.save()
                        accounts_dict[id] = account
                    else:
                        account = Account(
                            name = name,
                        )
                        account.save()
                        accounts_without_parent[id] = account
            print(accounts_without_parent) 
            transactions = file.getElementsByTagName('gnc:transaction')
            for transaction_xml in transactions:
                try:
                    transaction_description = transaction_xml.getElementsByTagName('trn:description')[0].firstChild.data
                except AttributeError as error:
                    pass
                date_str = transaction_xml.getElementsByTagName('trn:date-posted')[0].getElementsByTagName('ts:date')[0].firstChild.data
                date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S +%f")
                transaction = Transaction(
                    date = date,
                    description = transaction_description,
                )
                transaction.save()
                entries = transaction_xml.getElementsByTagName('trn:split')
                for entry_xml in entries:
                    account_id = entry_xml.getElementsByTagName('split:account')[0].firstChild.data
                    account = accounts_dict[account_id]
                    description_memos = entry_xml.getElementsByTagName('split:memo')
                    description = transaction_description
                    if len(description_memos) > 0:
                        description = description_memos[0].firstChild.data
                    value = entry_xml.getElementsByTagName('split:value')[0].firstChild.data
                    quantity = entry_xml.getElementsByTagName('split:quantity')[0].firstChild.data
                    if value != quantity:
                        print('Value != quantity = ' + entry_xml.getElementsByTagName('split:id')[0].firstChild.data)
                    amount = int(value[:-4]) / 100
                    entry = Entry(
                        account = account,
                        transaction = transaction,
                        description = description,
                        amount = amount,
                    )
                    entry.save()