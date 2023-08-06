from kavenegar import *

def send_otp_code(phone_number, code):
    try:
        api = KavenegarAPI('2F77537067544365733452714E42516D69344B6176456854354732787363716B4B7848316F5165525155553D')
        params = {
            'sender': '',
            'receptor': phone_number,
            'message': f'validations code : {code}',
        }
        response = api.sms_send(params)
        print(response)
    except APIException as ex:
        print(ex)
    except HTTPException as ex:
        print(ex)