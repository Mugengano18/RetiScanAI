import requests
import os

def send_sms(patient):

    message = (
    f"Dear {patient.full_name},\n\n"
    f"This is to inform you that you have been diagnosed with stage {patient.predicted_class_name} of diabetic retinopathy.\n\n"
    f"Your prescribed medicine is: {patient.description}\n\n"
    f"Please follow the prescribed medication and consult your doctor for further information."
)

    data	=	{	
            'recipients':patient.phone_number,	
            'message':message,		
            'sender':str(os.getenv('SENDER')),	
            'dlrurl':str(os.getenv('DLRURL'))
        }
      

    response = requests.post(str(os.getenv('SMS_URL')),	
        data,
        auth=(str(os.getenv('SMS_USERNAME')), str(os.getenv('SMS_PASSWORD')))	
        )
    print("response++++++",response)
    return response.status_code
    