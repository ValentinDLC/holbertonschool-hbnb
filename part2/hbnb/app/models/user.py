from base_model import BaseModel


class User(BaseModel):
    """
    User class that inherits from BaseModel.
    """
    def __init__(self, email, password, first_name, last_name, is_admin=False):
        """
        Initialize a User instance with email, password, first name, last name,
        and admin status.

        Args:
            email (str): The user's email address.
            password (str): The user's password.
            first_name (str): The user's first name.
            last_name (str): The user's last name.
            is_admin (bool): Indicates if the user has admin privileges.
                            Default to False.
        """
        super().__init__()
        self.email = email
        self.password = password
        self.first_name = first_name
        self.last_name = last_name
        self.is_admin = is_admin

        #TODO: hash password, print formationg, serialization, check format email, max length first and last name.


