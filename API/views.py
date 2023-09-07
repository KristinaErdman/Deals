import codecs
import csv

from django.db import transaction
from django.db.models import Sum
from rest_framework import status
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Customer, Deal, Gem
from .serializers import CustomersTopSerializer, FileSerializer


class APITopCustomers(APIView):

    def get(self, request, limit):
        # применяю агрегатную функцию чтобы опеределить потраченную покупателями сумму
        # сортирую покупателей по размеру потраченной ими суммы и оставляю первые limit из них
        customers = Customer.objects.annotate(Sum('deals__total')).order_by('-deals__total__sum')[:limit]

        customers_info = list()
        all_gems = list()
        # формирую список из словарей нужных значений для каждого покупателя и список всех камней
        for customer in customers:
            info = {
                'username': customer.username,
                'spent_money': customer.deals__total__sum,
                'gems': customer.get_gems_names(),
            }
            customers_info.append(info)
            all_gems.extend(info['gems'])

        del (customers)
        # формирую множество уникальных камней
        unique_gems = set([gem for gem in all_gems if all_gems.count(gem) == 1])
        del (all_gems)

        # у каждого покупателя убираю уникальные камни
        for customer in customers_info:
            customer['gems'] = customer['gems'] - unique_gems

        serializer = CustomersTopSerializer(customers_info, many=True)
        return Response({'response': serializer.data}, status=status.HTTP_200_OK)


class APIDeals(APIView):
    def save_deals_from_file(self, input_file):
        try:
            reader = csv.DictReader(codecs.iterdecode(input_file, 'utf-8'))
            for line in reader:
                line['customer'] = line['customer'].strip()
                new_customer, created = Customer.objects.get_or_create(
                    username__iexact=line['customer'],
                    defaults={'username': line['customer']}
                )

                line['item'] = line['item'].strip()
                new_item, created = Gem.objects.get_or_create(
                    name__iexact=line['item'],
                    defaults={'name': line['item']}
                )

                new_deal = Deal.objects.create(
                    customer=new_customer,
                    item=new_item,
                    total=line['total'],
                    quantity=line['quantity'],
                    date=line['date']
                )
                new_deal.save()
        except KeyError:
            raise KeyError('The file content does not match the desired format')

    @transaction.atomic()
    def post(self, request):
        file_serializer = FileSerializer(data=request.data)
        if file_serializer.is_valid(raise_exception=True):
            file = request.data['deals']

            # очищаю БД, т.к. ранее загруженные версии файла не должны влиять на результат обработки новых
            Customer.objects.all().delete()
            Gem.objects.all().delete()
            Deal.objects.all().delete()

            # считываю информаию из файла и заношу в БД
            try:
                self.save_deals_from_file(file)
            except Exception as error:
                raise ValidationError(detail=error)

            return Response({'Status': 'OK'}, status=status.HTTP_201_CREATED)
