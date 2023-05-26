import re


def email_validate(email):
	regex = re.compile(
		'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
	return re.fullmatch(regex, email)


def phone_validate(phone):
	regex = re.compile('\d{10}')
	print(phone, regex)
	return re.fullmatch(regex, phone)


def password_validate(password: str):
	return len(password) > 5


# везде его вставить
def login_validate(login: str):
	return len(login) > 5
