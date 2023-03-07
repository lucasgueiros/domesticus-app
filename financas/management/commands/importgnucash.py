from django.core.management.base import BaseCommand, CommandError
from polls.models import Question as Poll
from xml.dom import minidom

class Command(BaseCommand):
        help = 'Importar arquivo do gnucash'
        
        def add_arguments (self, parser):
            parser.add_argument('file', nargs='+', type=str)
        
        def handle (self, *args, **options):
            file = minidom.parse(options['file'])
            
            # <gnc:account version="2.0.0">
  # <act:name>Ativos</act:name>
  # <act:id type="guid">0c21f13ed05b4e77952554df644c9d34</act:id>
  # <act:type>ASSET</act:type>
  # <act:commodity>
  #   <cmdty:space>CURRENCY</cmdty:space>
   #   <cmdty:id>BRL</cmdty:id>
   # </act:commodity>
   # <act:commodity-scu>100</act:commodity-scu>
   # <act:description>Ativos</act:description>
    # <act:parent type="guid">fdb9f59ccbd240678bbd7eb591db7303</act:parent>
    # </gnc:account>
            accounts = file.getElementsByTagName('gnc:account')
            for account in accounts:
                name = account.find('act:name')
                