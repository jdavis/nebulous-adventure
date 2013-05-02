THEMES = {
    'default': {
        'body': 'hsla(210, 6.6667%, 11.7647%, 1)',
        'container': 'hsla(216, 6.1728%, 15.8824%, 1)',
    },
    'tomorrow': {
        'body': 'hsla(212, 92%, 20%, 1)',
        'container': 'hsla(210, 87%, 27%, 1)',
    },
    'cobalt': {
        'body': 'hsla(206, 92.5926%, 10.5882%, 1)',
        'container': 'hsla(206, 92.7711%, 16.2745%, 1)',
    },
    'espresso': {
        'body': 'hsla(23, 19.5652%, 18.0392%, 1)',
        'container': 'hsla(21, 12.7820%, 26.0784%, 1)',
    }
}


def get_theme(theme='default'):
    return THEMES.get(theme, {})


def get_settings(theme='default', font='default'):
    return {
        'theme': get_theme(theme),
    }
