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

FONT = {
    'sans-serif': 'sans-serif',
    'serif': 'serif',
    'fantasy': 'fantasy',
    'cursive': 'cursive',
    'monospace': 'Monaco, Menlo, Consolas, "Courier New", monospace',
}


def get_theme(theme='default'):
    return THEMES.get(theme, {})


def get_font(font='monospace'):
    return FONT[font] if font in FONT else 'monospace'


def get_settings(theme='default', font='default'):
    return {
        'theme': get_theme(theme),
        'font': get_font(font),
    }
