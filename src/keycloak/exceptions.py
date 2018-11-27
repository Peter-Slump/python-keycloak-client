class KeycloakClientError(Exception):
    def __init__(self, original_exc):
        """

        :param original_exc: Exception
        """
        self.original_exc = original_exc
        super(KeycloakClientError, self).__init__(*original_exc.args)
