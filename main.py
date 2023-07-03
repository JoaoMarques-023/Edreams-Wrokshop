import requests
import json
import schedule
import time

def recall():

    response = requests.get('https://random-data-api.com/api/v2/users?size=100', params={})

    if response.status_code == 200:
        print("Successful connection with API.")
        print('-------------------------------')
        data = response.json()
    elif response.status_code == 404:
        print("Unable to reach URL.")
    else:
        print("Unable to connect API or retrieve data.")

    filtered_data = []
    output_data = []
    priceM = 10
    priceA = 100

    if response.status_code == 200:
        for record in data:
            if record['subscription']['payment_method'] == "Credit card" and record['subscription']['status'] == "Pending" and record['subscription']['term'] == "Monthly" or record['subscription']['term'] == "Annual":
                    record_data = {
                        'first_name': record['first_name'],
                        'last_name': record['last_name'],
                        'email': record['email'],
                        'address': record['address'],
                        'credit_card_number': record['credit_card']['cc_number'],
                        'subscription': {
                            'plan': record['subscription']['plan'],
                            'status': record['subscription']['status'],
                            'payment_method': record['subscription']['payment_method'],
                            'term': record['subscription']['term']
                        }
                    }
                    filtered_data.append(record_data)
                    
                    if record['subscription']['term'] == "Monthly":
                        output_data.append({
                            'credit_card_number': record['credit_card']['cc_number'],
                            'amount': priceM,
                            'plan': record['subscription']['plan']
                        })
                    else:
                        output_data.append({
                            'credit_card_number': record['credit_card']['cc_number'],
                            'amount': priceA,
                            'plan': record['subscription']['plan']
                        })

    print(json.dumps(filtered_data, indent=2))
    print('***************************')
    print(json.dumps(output_data, indent=2))
schedule.every(3).seconds.do(recall)

while True:
    schedule.run_pending()
    time.sleep(1)

