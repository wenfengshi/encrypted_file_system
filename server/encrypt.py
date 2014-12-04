import json
import base64

from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from Crypto.Hash import SHA
from Crypto import Random

def chunk_size(key):
	"""Returns the maximum PKCS1_OAEP encryption length.

	This is the size of the RSA modulus (N) in bytes, minus two
	times the digest (SHA-1) size, minus 2.
	"""

	return (key.size() / 8) - (2 * SHA.digest_size) - 2

def encrypt(key, plaintext, pad=True):
	"""Encypts filenames (an arbitrary string) of any length."""

	ciphertexts = []

	if pad:
		cipher = PKCS1_OAEP.new(key)
		for start in xrange(0, len(plaintext), chunk_size(key)):
			end = start + chunk_size(key)
			chunk = plaintext[start:end]
			ciphertext = cipher.encrypt(chunk)
			ciphertexts.append(base64.b64encode(ciphertext))
	else:
		for start in xrange(0, len(plaintext), chunk_size(key)):
			end = start + chunk_size(key)
			chunk = plaintext[start:end]
			# K=0 is required but ignored parameter
			ciphertext = key.encrypt(chunk, K=0)[0]
			ciphertexts.append(base64.b64encode(ciphertext))

	return ciphertexts

def decrypt(key, ciphertexts, pad=True):
	"""Decrypts file contents from an arbitrary number of chunks."""

	plaintext = ""
	if pad:
		cipher = PKCS1_OAEP.new(key)
		for ciphertext in ciphertexts:
			plaintext += cipher.decrypt(base64.b64decode(ciphertext))
	else:
		for ciphertext in ciphertexts:
			plaintext += key.decrypt(base64.b64decode(ciphertext))

	return plaintext

def encrypt_file(key, filename):
	"""Encrypts the contents of the named file into an array of ciphertexts."""

	ciphertexts = []
	with open(filename, "r") as f:
		ciphertexts = encrypt(key, f.read())

	return ciphertexts

def decrypt_file(key, ciphertexts):
	return decrypt(key, ciphertexts, pad=True)

def encrypt_filename(key, filename):
	"""Encrypts the filename into an array of ciphertexts.

	This does not pad the filename, so two encryptions of the same text
	will yield the same encrypted string.
	"""

	return encrypt(key, filename, pad=False)

def decrypt_filename(key, ciphertext):
	return decrypt(key, ciphertext, pad=False)

