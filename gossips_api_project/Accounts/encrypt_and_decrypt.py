import base64
import random
from Crypto.Cipher import AES
from cryptography.fernet import  InvalidToken
from django.conf import settings
from django.core.signing import BadSignature
from django.core import signing
from cryptography.fernet import  Fernet


class My_crypto_handler:

    key = base64.urlsafe_b64encode(bytes(settings.SECRET_KEY, encoding='utf-8')[:32])

    def encrypt(self,string):
        return  Fernet(self.key).encrypt(bytes(string,encoding='utf-8'))

    def sign_a_string(self,JSON):
        return signing.dumps(JSON)

    def check_signature_of_string(self, string):
        try:
            return signing.loads(string)
        except BadSignature as b:
            return None

    def decrypt(self,cipher_text):
        print(type(cipher_text) , cipher_text)
        try:
            t = Fernet(self.key).decrypt(cipher_text)
            return  t
        except InvalidToken as e:
            print(e)

    def give_otp(self,phone_number):
        otp = random.randint(11111111, 99999999)
        print(otp)
        signed_token = self.sign_a_string({"otp":str(otp) , "phone_number":phone_number})
        encrypted_token = self.encrypt(signed_token).decode('utf-8')
        return encrypted_token,otp


    def verify_otp(self, signed_token, otp_given):
        decrypted_otp = self.decrypt(bytes(signed_token, encoding='utf-8'))
        if not decrypted_otp:
            return  None
        otp_json = self.check_signature_of_string(decrypted_otp.decode('utf-8'))
        if not otp_json:
            return None
        if otp_json.get("otp",None) != str(otp_given) :
            return None
        return otp_json
