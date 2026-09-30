from pwdlib import PasswordHash

pwd_hash = PasswordHash.recommended()


class Hash:

    @staticmethod
    def bcrypt(password):
        return pwd_hash.hash(password)

    @staticmethod
    def verify(hashed_password, plain_password):
        return pwd_hash.verify(plain_password, hashed_password)