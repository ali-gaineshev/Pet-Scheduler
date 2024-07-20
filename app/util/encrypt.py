# app/util/encrypt

import bcrypt


class Encrypt:
    """ Password encrypter (using hashing) """

    @staticmethod
    def hash_password(password: str) -> str:
        """
        Hashes a password to store in a database.

        Args:
            password (str): The password to hash.

        Returns:
            str: The hashed password.
        """
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed_password.decode()

    @staticmethod
    def match_password(password: str, hashed_password: str) -> bool:
        """
        Verifies a password against a hashed password.

        Args:
            password (str): The plain text password to verify.
            hashed_password (str): The hashed password to verify against.

        Returns:
            bool: True if the password matches the hashed password, False otherwise.
        """

        return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))
