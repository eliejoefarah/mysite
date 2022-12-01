from abc import ABC, abstractmethod


# ------------------------------------------------------------------------------------------------
#
# This is the first part of the bridge design pattern, "Allocations" and its subclasses who are
# just "Savings", where we can set our savings and budget and change them.
#
# ------------------------------------------------------------------------------------------------

class Allocations(ABC):

    @abstractmethod
    def __init__(self, money=0):
        self.money = money

    @abstractmethod
    def get_money(self):
        return self.money

    @abstractmethod
    def set_money(self, n):
        self.money = n


class Savings(Allocations):

    def __init__(self, money=0, *savings):
        self.update = None
        self.sav = None
        self.budget = None
        self.savings = None
        self.current_budget = self.budget

    def get_money(self):
        pass

    def set_money(self, n):
        pass

    def get_savings(self):
        return self.savings

    def set_savings(self, k):
        self.savings = k
        self.money = self.money + self.savings

    def add_savings(self, sav):
        self.sav = sav
        self.savings = self.savings + self.sav
        self.money = self.money + self.savings

    def set_budget(self, b):
        self.budget = b
        self.current_budget = self.budget

    def get_budget(self):
        return self.budget

    def update_budget(self, update):
        self.update = update
        self.current_budget = self.current_budget - self.update

    def how_much_left(self):
        return self.current_budget

    def percentage_left(self):
        return (self.current_budget * 100) / self.budget


# ------------------------------------------------------------------------------------------------
#
# This is the second part of the bridge design pattern, "Expenses" and its subclasses who are
# "Payments" and "Earnings", where we can proceed with payments and manage our expenses and what
# we buy.
#
# ------------------------------------------------------------------------------------------------

class Expenses(ABC):

    @abstractmethod
    def __init__(self, exp):
        s = Savings()
        # We must check if we can make an expense first.
        if exp > s.how_much_left():
            print("Invalid purchase.")
        else:
            print("Purchase made.")
            s.update_budget(exp)


class Earnings(Expenses):
    def __init__(self, exp, *earning):
        s = Savings()
        s.add_savings(earning)


class Payments(Expenses):

    def __init__(self, exp):
        s = Savings()
        # Two list will be used for items, the same index for each list represents in one list
        # the price and the other one the name

        # List for the names of each item
        self.items = []
        # List for the prices of each item
        self.prices = []

        self.Index = 0

    def item_purchase(self, price, name):
        s = Savings()
        if price < s.how_much_left():
            self.prices.insert(self.Index, price)
            self.items.insert(self.Index, name)
            self.Index += 1
        else:
            print("Invalid item purchase")
