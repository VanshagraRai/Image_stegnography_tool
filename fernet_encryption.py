import pickle
from cryptography.fernet import Fernet
from PIL import Image

def generate_key():
    return Fernet.generate_key()

def encrypt_merged_image(merged_image, key, output_file='encrypted_merged_image.dat'):
    cipher_suite = Fernet(key)
    merged_image_bytes = pickle.dumps(merged_image)
    encrypted_data = cipher_suite.encrypt(merged_image_bytes)
    with open(output_file, 'wb') as file:
        file.write(encrypted_data)

def decrypt_merged_image(encrypted_file, key):
    cipher_suite = Fernet(key)
    with open(encrypted_file, 'rb') as file:
        encrypted_data = file.read()
    decrypted_data_bytes = cipher_suite.decrypt(encrypted_data)
    decrypted_merged_image = pickle.loads(decrypted_data_bytes)
    return decrypted_merged_image

# Example usage:

