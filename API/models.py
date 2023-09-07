from django.db.models import Model, ForeignKey, CharField, DateTimeField, \
    PositiveIntegerField, PositiveSmallIntegerField
from django.db.models.deletion import CASCADE


class Customer(Model):
    username = CharField(max_length=50, unique=True, verbose_name='логин покупателя')

    class Meta:
        verbose_name = 'Покупатель'
        verbose_name_plural = 'Покупатели'

    def get_gems_names(self) -> set:
        gems = Gem.objects.filter(deals__customer_id__in=(self.id,)).only('name').distinct()
        return set(map(lambda gem: gem.name, gems))

    def __str__(self) -> str:
        return f'{self.username}'


class Gem(Model):
    name = CharField(max_length=20, unique=True, verbose_name='наименование товара')

    class Meta:
        verbose_name = 'Камень'
        verbose_name_plural = 'Камни'

    def __str__(self) -> str:
        return self.name


class Deal(Model):
    customer = ForeignKey(Customer, on_delete=CASCADE, related_name='deals')
    item = ForeignKey(Gem, on_delete=CASCADE, related_name='deals')
    total = PositiveIntegerField(verbose_name='сумма сделки')
    quantity = PositiveSmallIntegerField(verbose_name='количество товара, шт')
    date = DateTimeField(verbose_name='дата и время регистрации сделки')

    class Meta:
        verbose_name = 'Сделка'
        verbose_name_plural = 'Сделки'

    def __str__(self) -> str:
        return f'№{self.pk}\t{self.customer}\t{self.item}\t{self.total}\t{self.quantity}\t{self.date}'
