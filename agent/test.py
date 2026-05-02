import psutil, datetime, ipaddress, ifaddr

def getActiveUsers() -> set[str]:
		activeUsers = []
		for user in psutil.users():
			activeUsers.append(user[0])
		return activeUsers

print(getActiveUsers())