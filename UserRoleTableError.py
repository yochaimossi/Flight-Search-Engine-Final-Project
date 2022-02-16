class UserRoleTableError(Exception):
    def __init__(self, msg="More than 3 roles in the User Role table."):
        self.msg = msg
        super().__init__(self.msg)

    def __str__(self):
        return f'{self.msg}'