import datetime

from business_rules.actions import BaseActions, rule_action
from business_rules.fields import FIELD_NUMERIC
from business_rules.variables import BaseVariables, numeric_rule_variable, boolean_rule_variable

BASE_PRICE = 20


class OrderVariables(BaseVariables):
    def __init__(self, order):
        self.order = order

    @numeric_rule_variable()
    def distance(self):
        return self.order.start_location.distance(self.order.end_location) * 100

    @numeric_rule_variable()
    def n_orders(self):
        return self.order.client_user.orders_made.count()

    @numeric_rule_variable()
    def hour(self):
        return self.order.date_time_ordered.hour

    @numeric_rule_variable()
    def weekday(self):
        return self.order.date_time_ordered.weekday()

    @boolean_rule_variable()
    def client_is_premium(self):
        return self.order.client_user.is_premium

    @numeric_rule_variable()
    def n_orders_mod_10(self):
        return self.order.client_user.orders_made.count() % 10

    @numeric_rule_variable()
    def n_orders_this_month(self):
        return self.order.client_user.orders_made.filter(
            date_time_ordered__gte=datetime.date(datetime.datetime.now().year,
                                                 datetime.datetime.now().month, 1)).count()


class OrderActions(BaseActions):
    def __init__(self, order):
        self.order = order

    @rule_action(params={"km_price": FIELD_NUMERIC})
    def extra_kms(self, km_price):
        distance = self.order.start_location.distance(self.order.end_location) * 100 - 2000
        self.order.delivery_price = self.order.delivery_price + distance * km_price

    @rule_action(params={"porc": FIELD_NUMERIC})
    def discount_porc(self, porc):
        self.order.delivery_price = self.order.delivery_price - self.order.delivery_price * porc

    @rule_action(params={"porc": FIELD_NUMERIC})
    def recharge_porc(self, porc):
        self.order.delivery_price = self.order.delivery_price + self.order.delivery_price * porc

    @rule_action(params={"disc": FIELD_NUMERIC})
    def discount_fixed(self, disc):
        self.order.delivery_price = self.order.delivery_price - disc if self.order.delivery_price > disc else 0

    @rule_action()
    def free_order(self):
        self.order.delivery_price = 0
