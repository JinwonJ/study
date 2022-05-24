from functools import update_wrapper

from flask import current_app

def no_cache():
    def decorator(target_function):
        def wrapped_function(*args, **kwargs):
            new_response = current_app.make_default_options_response()
            headers = new_response.headers
            headers['Cache-Control'] = 'no-cache, no-store, must-revalidate, proxy-revalidate'
            headers['Pragma'] = 'no-cache'
            headers['Expires'] = '0'
            return new_response

        target_function.provide_automatic_options = False
        return update_wrapper(wrapped_function, target_function)

    return decorator
