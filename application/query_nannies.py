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
        query.add(Q(childcareaddress__icontains=care_location_postcode), Q.AND)

    if application_reference:
        query.add(Q(nannyapplication__application_reference__icontains=application_reference), Q.AND)

    return query


def get_dob_query(dob):
    split_dob = re.split(r"[^0-9]", dob)

    if len(split_dob) == 1:
        # If only one DOB part has been supplied assume it could be day month or year

        # Create four digit year if 2 digit year supplied
        if len(split_dob[0]) == 2:
            previous_century_year = str(19) + split_dob[0]
            current_century_year = str(20) + split_dob[0]
        else:
            # Otherwise allow longer values to be directly issued against query
            previous_century_year = split_dob[0]
            current_century_year = split_dob[0]

        return Q(
            Q(applicantpersonaldetails__birth_day=int(split_dob[0])) |
            Q(applicantpersonaldetails__birth_month=int(split_dob[0])) |
            Q(applicantpersonaldetails__birth_year=int(previous_century_year)) |
            Q(applicantpersonaldetails__birth_year=int(current_century_year))
        )

    elif len(split_dob) == 2:
        # If two DOBs part have been supplied, again assume second part is either a month or a year

        # Create four digit year if 2 digit year supplied
        if len(split_dob[1]) == 2:
            previous_century_year = str(19) + split_dob[1]
            current_century_year = str(20) + split_dob[1]
        else:
            # Otherwise allow longer values to be directly issued against query
            previous_century_year = split_dob[1]
            current_century_year = split_dob[1]

        return Q(
            Q(applicantpersonaldetails__birth_day=int(split_dob[0])),
            Q(applicantpersonaldetails__birth_month=int(split_dob[0])) |
            Q(applicantpersonaldetails__birth_month=int(split_dob[1])) |
            Q(applicantpersonaldetails__birth_year=int(previous_century_year)) |
            Q(applicantpersonaldetails__birth_year=int(current_century_year))
        )

    elif len(split_dob) == 3:

        # Create four digit year if 2 digit year supplied
        if len(split_dob[2]) == 2:
            previous_century_year = str(19) + split_dob[2]
            current_century_year = str(20) + split_dob[2]
        else:
            # Otherwise allow longer values to be directly issued against query
            previous_century_year = split_dob[2]
            current_century_year = split_dob[2]

        return Q(
            Q(applicantpersonaldetails__birth_day=int(split_dob[0])),
            Q(applicantpersonaldetails__birth_month=int(split_dob[0])) |
            Q(applicantpersonaldetails__birth_month=int(split_dob[1])) |
            Q(applicantpersonaldetails__birth_year=int(previous_century_year)) |
            Q(applicantpersonaldetails__birth_year=int(current_century_year))
        )

    else:
        return None
