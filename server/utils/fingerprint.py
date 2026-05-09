import hashlib


def fingerprint(uuid, machineid):
	fingerprint = "|".join([
	    str(machineid),
	    str(uuid),
	])
	id = hashlib.sha256(fingerprint.encode()).hexdigest()
	return id
