from fastapi import Body

payments_example = Body(
    ...,
    examples={
        "normal": {
            "sumary": "A Normal example",
            "description": "A **normal** item works correctly.",
            "value": {
                "paid": "True or False",
                "payment_made": "Cash, card or cash_card"
            }
        }
    }
)

price_list_example = Body(
    ...,
    examples={
        "normal": {
            "sumary": "A Normal example",
            "description": "A **normal** item works correctly.",
            "value": {
                "service": "Example Orthopedic surgeries",
                "medical_service": "Example Ankle arthroscopy surgery",
                "price_of_service": "Enter price in RSD",
                "time_for_exam": "You can enter the number of minutes"
                                 " required for particular exam "
            }
        }
    }
)

user_example = Body(
    ...,
    examples={
        "normal": {
            "sumary": "A Normal example",
            "description": "A **normal** item works correctly.",
            "value": {
                "email": "Please enter a valid email.",
                "password": "Do not show your password to anyone",
                "name": "Enter name and surname",
                "role": "Choose role for User it can be doctor, admin or finance"
            }
        }
    }
)

customer_example = Body(
    ...,
    examples={
        "normal": {
            "sumary": "A Normal example",
            "description": "A **normal** item works correctly.",
            "value": {
                "email": "Please enter a valid email.",
                "date_of_birth": "Please enter in form yyyy-mm-dd",
                "personal_medical_history": "You can enter here blood "
                                            " type or information about allergies",
                "family_medical_history": "You can enter here record of "
                                          " the diseases and health condition in patient family",
                "company_name": "Name of the company",
                "company_PIB": "Unique 8 digits number",
                "company_address": "Address of the company",
                "name": "Enter name and surname of patient",
                "jmbg": "Unique 13 digits number",
                "address": "Patient address, not required",
                "phone": "Patient phone number, not required"

            }
        }
    }
)

