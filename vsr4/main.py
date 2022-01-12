from eve import Eve

DOMAIN = {
    'users': {
        'schema': {
            'name': {
                'type': 'string',
                'minlength': 1,
                'maxlength': 10,
            },
            'email': {
                'type': 'string',
                'regex': '^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$',
                'minlength': 1,
                'maxlength': 10,
            },
        },
        'resource_methods': ['GET', 'POST'],
    },
    'polls': {
        'schema': {
            'title': {
                'type': 'string',
                'minlength': 1,
                'maxlength': 10,
            }
        },
        'resource_methods': ['GET', 'POST', 'PATCH'],
    },
}


def main():
    app = Eve()
    app.run()


if __name__ == '__main__':
    main()
