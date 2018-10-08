from uuid import uuid4
import inflect
from rest_framework import serializers
from django.db import models
from .nanny_application import NannyApplication


class ChildcareAddress(models.Model):
    """
        Model for Nanny Application table
    """
    # Managers
    objects = models.Manager()

    application_id = models.ForeignKey(NannyApplication, on_delete=models.CASCADE, db_column='application_id')
    date_created = models.DateTimeField(blank=True, null=True)
    childcare_address_id = models.UUIDField(primary_key=True, default=uuid4)
    street_line1 = models.CharField(max_length=100, blank=True, null=True)
    street_line2 = models.CharField(max_length=100, blank=True, null=True)
    town = models.CharField(max_length=100, blank=True, null=True)
    county = models.CharField(max_length=100, blank=True, null=True)
    country = models.CharField(max_length=100, blank=True, null=True)
    postcode = models.CharField(max_length=100, blank=True, null=True)
    number = models.IntegerField(blank=True, null=True)

    @classmethod
    def get_id(cls, childcare_address_id):
        return cls.objects.get(pk=childcare_address_id)

    class Meta:
        db_table = 'CHILDCARE_ADDRESS'


class ChildcareAddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChildcareAddress
        fields = '__all__'

    def get_title_row(self):
        return {"title": "Childcare address", "id": self.data['childcare_address_id'], "index": 0}

    def get_address_ord(self, i):
        """
        get ordinal value of this childcare address
        :param i: index of address
        :return:
        """
        formatter = inflect.engine()
        return formatter.number_to_words(formatter.ordinal(i)).title()

    def get_address(self):
        data = self.data
        return str(data['street_line1']) + ', ' + str(data['street_line2']) + ', ' \
               + str(data['town']) + ', ' + str(data['postcode'])

    def get_summary_table(self, i):
        childcare_address = self.get_address()
        row_name = "Childcare address" if i == 1 else self.get_address_ord(i) + " childcare address"
        return {"name": row_name, "value": childcare_address, 'pk': self.data['childcare_address_id'],
                "reverse": "Childcare-Address-Manual-Entry", 'index': i+1}
