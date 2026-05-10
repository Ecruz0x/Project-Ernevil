import hashlib


def fingerprint(machineid):
	fingerprint = hashlib.sha256(machineid.encode()).hexdigest()
	return fingerprint
