



import requests

api_key = 'ab94318200074509bde56c4e37081464' # https://app.abstractapi.com/api/email-validation
api_url = 'https://emailvalidation.abstractapi.com/v1/?api_key=' + api_key                                                                                                                                                                               

def validate_email(email):
    response = requests.get(api_url + f"&email={email}")
    data = response.json()

    if (
    data['is_valid_format']['value'] and
    data['is_mx_found']['value'] and
    data['is_smtp_valid']['value'] and
    not data['is_catchall_email']['value'] and
    not data['is_role_email']['value'] and
    data['is_free_email']['value']):
        return True
    else:
        return False






"""
data={'email': 'parvezhossen81@gmail.com', 'autocorrect': '', 'deliverability': 'DELIVERABLE', 'quality_score': '0.95',
           'is_valid_format': {'value': True, 'text': 'TRUE'}, 'is_free_email': {'value': True, 'text': 'TRUE'},
            'is_disposable_email': {'value': False, 'text': 'FALSE'}, 'is_role_email': {'value': False, 'text': 'FALSE'},
              'is_catchall_email': {'value': False, 'text': 'FALSE'}, 'is_mx_found': {'value': True, 'text': 'TRUE'},
                'is_smtp_valid': {'value': True, 'text': 'TRUE'}}

data={'email': 'ph.cse.bd@gmail.com', 'autocorrect': '', 'deliverability': 'DELIVERABLE', 'quality_score': '0.95',
       'is_valid_format': {'value': True, 'text': 'TRUE'}, 'is_free_email': {'value': True, 'text': 'TRUE'},
         'is_disposable_email': {'value': False, 'text': 'FALSE'}, 'is_role_email': {'value': False, 'text': 'FALSE'},
           'is_catchall_email': {'value': False, 'text': 'FALSE'}, 'is_mx_found': {'value': True, 'text': 'TRUE'},
             'is_smtp_valid': {'value': True, 'text': 'TRUE'}}

data={'email': 'ph.cse.bdzzzzzzzzz@gmail.com', 'autocorrect': '', 'deliverability': 'UNDELIVERABLE', 'quality_score': '0.00',
       'is_valid_format': {'value': True, 'text': 'TRUE'}, 'is_free_email': {'value': True, 'text': 'TRUE'},
         'is_disposable_email': {'value': False, 'text': 'FALSE'}, 'is_role_email': {'value': False, 'text': 'FALSE'},
           'is_catchall_email': {'value': False, 'text': 'FALSE'}, 'is_mx_found': {'value': True, 'text': 'TRUE'},
             'is_smtp_valid': {'value': False, 'text': 'FALSE'}}
"""
