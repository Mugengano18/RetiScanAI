import requests
import os

def send_sms(patient):

    data	=	{	
            'recipients':patient.phone_number,	
            'message'	:patient.description,		
            'sender':str(os.getenv('SENDER')),	
            'dlrurl':str(os.getenv('DLRURL'))
        }
      

    response = requests.post(str(os.getenv('SMS_URL')),	
        data,
        auth=(str(os.getenv('SMS_USERNAME')), str(os.getenv('SMS_PASSWORD')))	
        )
    return response.status_code
    