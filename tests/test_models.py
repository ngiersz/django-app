from django.test import TestCase
from hansweb.models import Order, Address
from django.utils import timezone
from django.contrib.auth.models import User

class AddressTestCase(TestCase):

    def setUp(self):
        Address.objects.create(country='US', city='Austin, TX', street='N Lamar Blvd', number='5540', zip_code='75751')
        Address.objects.create(country='Poland', city='Poznań', street='Półwiejska', number='5', zip_code='61-885')
        Address.objects.create(country='Poland', city='Warsaw', street='Stary Rynek', number='75B/6', zip_code='61-772')

    def test_address_is_formatted(self):
        address1 = Address.objects.get(country='US')
        address2 = Address.objects.get(country='Poland', city='Poznań')
        address3 = Address.objects.get(country='Poland', city='Warsaw')

        self.assertEqual(address1.get_formatted(), 'N Lamar Blvd 5540, Austin, TX, US')
        self.assertEqual(address2.get_formatted(), 'Półwiejska 5, Poznań, Poland')
        self.assertEqual(address3.get_formatted(), 'Stary Rynek 75B, Warsaw, Poland')


class OrderTestCase(TestCase):

    def setUp(self):
        User.objects.create_user(
            username='the_best_user_ever',
            email=None,
            password=None
        )

        User.objects.create_user(
            username='king-of-the-users',
            email=None,
            password=None
        )

        Address.objects.create(country='US', city='Austin, TX', street='N Lamar Blvd', number='5540', zip_code='75751')
        Address.objects.create(country='Poland', city='Poznań', street='Półwiejska', number='5', zip_code='61-885')

        Order.objects.create(
            client=User.objects.get(username='the_best_user_ever'),
            deliverer=None,
            status=Order.StatusType.waiting,
            pickupAddress=Address.objects.get(country='US'),
            deliveryAddress=Address.objects.get(country='Poland'),
            title='Bed',
            description='King size bed frame, without a mattress',
            created_date=timezone.now(),
            price=257.4,
            weight=15,
            dimensions=Order.DimensionType.pickup,
            isPaid=False
        )

    def test_order_is_accepted(self):
        order = Order.objects.get(title='Bed')
        deliverer = User.objects.get(username='king-of-the-users')
        order.accept(deliverer)
        self.assertEqual(Order.StatusType.transit, order.status)
        self.assertEqual(deliverer.username, order.deliverer.username)

    def test_order_can_be_deleted(self):
        order = Order.objects.get(title='Bed')
        self.assertTrue(order.can_delete())

    def test_order_cannot_be_deleted(self):
        order = Order.objects.get(title='Bed')
        order.accept(User.objects.get(username='king-of-the-users'))
        self.assertFalse(order.can_delete())

    def test_order_is_closed(self):
        order = Order.objects.get(title='Bed')
        order.close()
        self.assertEqual(Order.StatusType.closed, order.status)
        self.assertTrue(order.isPaid)
