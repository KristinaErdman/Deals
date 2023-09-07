import codecs
import csv

from .models import Customer, Deal, Gem


def from_fileDeals_to_db(input_file):
    error = None
    try:
        reader = csv.DictReader(codecs.iterdecode(input_file, 'utf-8'))
        for line in reader:
            new_customer, created = Customer.objects.get_or_create(username=line['customer'].lower().strip())
            new_item, created = Gem.objects.get_or_create(name=line['item'].lower().strip())
            new_deal = Deal.objects.create(customer=new_customer, item=new_item, total=line['total'],
                                           quantity=line['quantity'], date=line['date'])
            new_deal.save()
    except KeyError:
        error = KeyError('The file content does not match the desired format')
    finally:
        return error

