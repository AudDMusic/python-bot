from aiohttp import ClientResponse


_errors_dict = {
    901: 'No api_token passed and the limit was reached (api_token)',
    900: 'Wrong API token (api_token)',
    600: 'Incorrect audio URL (url)',
    500: 'Incorrect audio file',
    400: 'Too big audio file or too big audio. 10M or 25 seconds is maximum, we recommend '
         'to record no more than 20 seconds (usually it takes less than one megabyte)',
    300: 'Neural network returned error: there was a problem with the fingerprint creation.'
         ' Most likely, the audio file is too small',
    100: 'Unknown error'
}


class AudDApiError(Exception):
    def __init__(self, response_code):
        self.status = 'error'

        self.code = response_code
        error = _errors_dict.get(response_code)
        if not error:
            self.status = 'ok'

    def __repr__(self):
        return _errors_dict.get(self.code, self.status)

    def __str__(self):
        return self.__repr__()


def is_ok(server_response: ClientResponse or int):
    exception = AudDApiError(getattr(server_response, 'status', server_response))
    if exception.status == 'ok':
        return 'ok'
    raise exception
