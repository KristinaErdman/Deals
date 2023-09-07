from django.db.models import Sum
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Customer, Deal, Gem
from .serializers import CustomersTopSerializer, FileSerializer
from .services import save_deals_from_file


class APITopCustomers(APIView):

    def get(self, request, limit):
        # применяю агрегатную функцию чтобы опеределить потраченную покупателями сумму
        customers = Customer.objects.annotate(Sum('deals__total'))

        # сортирую покупателей по размеру потраченной ими суммы и оставляю первые limit из них
        customers = customers.order_by('deals__total__sum').reverse()[:limit]

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

    def post(self, request):
        file_serializer = FileSerializer(data=request.data)
        if file_serializer.is_valid():
            file = request.data['deals']

            # очищаю БД, т.к. ранее загруженные версии файла не должны влиять на результат обработки новых
            Customer.objects.all().delete()
            Gem.objects.all().delete()
            Deal.objects.all().delete()

            # считываю информаию из файла и заношу в БД
            try:
                save_deals_from_file(file)
            except Exception as error:
                raise ValidationError(detail=error)

            if error:
                return Response({'Status': 'Error', 'Desc': str(error)}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'Status': 'OK'}, status=status.HTTP_201_CREATED)
        else:
            return Response({'Status': 'Error', 'Desc': file_serializer.errors['deals'], },
                            status=status.HTTP_400_BAD_REQUEST)
