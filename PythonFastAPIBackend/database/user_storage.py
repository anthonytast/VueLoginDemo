from passlib.context import CryptContext

class UserDB():
    username: str
    first_name: str
    last_name: str
    phone_number: str
    password: str

    def __init__(self, username, first_name, last_name, phone_number, password):
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.phone_number = phone_number
        self.password = password

bcrypt_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

users = {
    "anthonytast": UserDB(
        username="anthonytast",
        first_name="Anthony",
        last_name="Tast",
        phone_number="631-925-7508",
        password=bcrypt_context.hash("SuperSecretPW")
    ),
    "testuser": UserDB(
        username="testuser",
        first_name="Dev",
        last_name="Tester",
        phone_number="1-800",
        password=bcrypt_context.hash("test")
    )
}
