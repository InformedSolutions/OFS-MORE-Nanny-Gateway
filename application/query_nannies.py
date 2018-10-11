import re

from django.db.models import Q


def get_nannies_query(name, date_of_birth, home_postcode, care_location_postcode, application_reference):
    query = Q()

    if name:
        query.add(
            Q(
                Q(applicantpersonaldetails__first_name__icontains=name) |
                Q(applicantpersonaldetails__last_name__icontains=name)
            ), Q.AND
        )

    if date_of_birth:
        dob_query = get_dob_query(date_of_birth)

        if dob_query:
            query.add(dob_query, Q.AND)

    if home_postcode:
        query.add(Q(applicanthomeaddress__postcode__icontains=home_postcode), Q.AND)

    if care_location_postcode:
        query.add(Q(childcareaddress__postcode__icontains=care_location_postcode), Q.AND)

    if application_reference:
        query.add(Q(application_reference__icontains=application_reference), Q.AND)

    return query


def get_dob_query(dob):
    split_dob = re.split(r"[^0-9]", dob)

    if split_dob is not None:
        dob_query = Q()
        for dob_str in split_dob:
            dob_query.add(Q(applicantpersonaldetails__date_of_birth__icontains=int(dob_str)), Q.AND)

        return dob_query

    else:
        return None
