def get_your_children_header_table(your_children_record):

    def get_live_with_applicant_name_list():
        # This list is reversed due to the order in which the records are pulled from the database being reversed.
        return ", ".join(child.get_full_name for child in reversed(your_children_record) if child.lives_with_applicant)

    return [
        {"title": 'Your Children', "id": 'your_children', "index": 0},

        {"name": "Which of your children live with you?",
         "value": get_live_with_applicant_name_list(),
         "pk": 'your_children',
         "index": 1,
         "reverse": "your-children:Your-Children-Details",
         "change_link_description": "which of your children live with you"}
    ]
