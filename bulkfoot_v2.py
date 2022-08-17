#!/usr/bin/env python
# -*- coding: utf-8 -*-

class LineItem:

    def __init__(self,descripiton,weight,price):
        self.description = descripiton
        self.weight = weight
        self.price = price

    def subtotal(self):
        return self.weight * self.price

    @property
    def weight(self):
        return self.__weight

    @weight.setter
    def weight(self,value):
        if value > 0:
            self.__weight = value
        else:
            raise ValueError('value must be > 0')