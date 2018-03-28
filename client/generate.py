from cryptography.fernet import Fernet
import hashlib

def get_hash(login, password):

    msg = hashlib.sha256()

    msg.update(login.encode("utf-8"))
    msg.update(password.encode("utf-8"))

    h = msg.hexdigest()

    return h

class MessKeys:
    def __init__(self, message):
        self.message = message

    def send_keys(self):
        cipher_key = Fernet.generate_key()
        cipher = Fernet(cipher_key)
        text = self.message.encode()
        encrypted_text = cipher.encrypt(text)
        message = encrypted_text, cipher_key
        message = str(message)
        return message

    def answer_keys(self):
        decripted_text = self.message.split("'")
        cipher = Fernet(decripted_text[3].encode())
        decrypted_text = cipher.decrypt(decripted_text[1].encode())
        message = decrypted_text.decode()
        return message
