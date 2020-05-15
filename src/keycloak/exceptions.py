class KeycloakClientError(Exception):
    def __init__(self, original_exc: Exception):
        """

        :param original_exc: Exception
        """
        self.original_exc: Exception = original_exc
        super(KeycloakClientError, self).__init__(*original_exc.args)
