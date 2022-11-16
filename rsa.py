#import rsa
from Crypto.PublicKey import RSA
#Create a function to generate a public/private key pair
def generate_keys():
    #Generate a public/private key pair using 4096 bits key length (512 bytes)
    new_key = RSA.generate(4096, e=65537)
    #The private key in PEM format
    private_key = new_key.exportKey("PEM")
    #The public key in PEM Format
    public_key = new_key.publickey().exportKey("PEM")
    #Return both the private and the public key
    return private_key, public_key