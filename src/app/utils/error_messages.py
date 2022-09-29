
def handle_error_messages(field):
    error_message = {
        'required': f'The field {field} is required.',
        'invalid': f'Invalid {field}.'
    }

    return error_message
