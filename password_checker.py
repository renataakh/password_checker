import requests # module for work with https(s) protocols
import hashlib	# module with hash algorithms
import sys 		# module for work with comandline (terminal)




def request_api_data(query_char):
	# API service pwnedpasswords from haveibeenpwned takes first  
	# 5 simbols of hash passord (SHA-1) and returns list of hacked poasswords
	# which start from this 5 simbols
	# https://haveibeenpwned.com/API/v2#PwnedPasswords
	
	# crates url address  (watch instruction on the link above)
	url = 'https://api.pwnedpasswords.com/range/' + query_char

	# recieves the address to the get method which
	# returns result of the type response object
	res = requests.get(url) 

	# checkes that operation passed without any errors (error status_code - 400)
	if res.status_code != 200:
		raise RuntimeError(f'Error fetching: {res.status_code}, check the API and try again')

	# returns result
	return res

def password_leaks_counter(hashes, hash_to_check):
	pass
	# recieves tuple of "tails" of hacked passworda
	# and "tail" of our password
	for h, count in hashes:
		if h == hash_to_check:
			return count
	return 0

# checkes password if it exixts in API response
def pwned_api_check(password):

	# encode - transforms stringobject to the binary representation of utf-8 encoding
	# sha1 - hashes object using the sha1 protocol returns a sha1 HASH object
	# hexdigest - returns the hexadecimal representation of the sha1 HASH object
	# upper - converts all letters to uppercase
	sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()

	# variables contain first 5 simbols of hash-password 
	# and the remaining simbols "tail"
	first5_char, tail = sha1password[:5], sha1password[5:]

	# calles the request_api_data function
	response = request_api_data(first5_char)

	# response.text returns text (objext str) representation of objext response
	# response.text.split() - split text on the strings
	# for each string (line): 
	# line.split(':') - split the recieved string by the seporator ':'
	# () - returns tuple of lists - [tail, counter]
	response_tuple = (line.split(':') for line in response.text.split())

	# returns result
	return password_leaks_counter(response_tuple, tail)



def main(args):
	for password in args:
		result = pwned_api_check(password)
		hidden_password = '*' * len(password) 
		if result:
			print(f'Your password {hidden_password} was leaked {result} times')
		else:
			print(f'Your password {hidden_password} wasn\'t leaked')

	return('done!')


if __name__ == '__main__':
	# sys.exit() - in the case, if sth will go wrong
	# stops the process and shows the result of main function
	sys.exit(main(sys.argv[1:]))




