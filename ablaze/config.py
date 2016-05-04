
'''
Custom configparser Interpolation to give Bash-style env var access

Adds:
    @{ENV}  - retrieve value from environment
    @{ENV:-word} - default to 'word' if unset
    @{ENV:+word} - use 'word' if set, else nothing
    @{ENV:?word} - show error 'word' if unset

'''

import os
import re
from configparser import Interpolation


PATTERN = re.compile(r'@{(?P<name>\w+)(?:%s)?}' % (
    '|'.join([
        r':-(?P<default>.+?)',
        r':\+(?P<test>.+?)',
        r':\?(?P<error>.+?)',
    ]),
))


class EnvironInterpolation(Interpolation):

    def before_get(self, parser, section, option, value, defaults):
        return self._interpolate(value)

    def _interpolate(self, value):
        def _handle(m):
            g = m.groupdict()
            if g['error']:
                if g['name'] not in os.environ:
                    raise RuntimeError('Missing env var %r: %s' % (g['name'], g['error']))
                return ''
            if g['test']:
                if os.environ.get(g['name'], None):
                    return g['test']
                else:
                    return ''
            # default or ''
            return os.environ.get(g['name'], g['default'] or '')

        return PATTERN.sub(_handle, value)


if __name__ == '__main__':
    import configparser

    c = configparser.ConfigParser(interpolation=EnvironInterpolation())
    c.read_dict({
        'section': {
            'plain': 'plain',
            'error': '@{MISSING:?Value missing}ok',
            'test': '@{PRESENT:+Value found}',
            'default': '@{DEFAULT:-Default value}',
        },
    })

    # No env var
    assert c['section']['plain'] == 'plain'

    # @{...:?error}
    try:
        c['section']['error']
    except RuntimeError:
        pass
    else:
        assert False, "@{MISSING:?...} should raise RuntimeError"
    os.environ['MISSING'] = '1'
    assert c['section']['error'] == 'ok'

    # @{...:+Set if found}
    assert c['section']['test'] == ''
    os.environ['PRESENT'] = 'yes'
    assert c['section']['test'] == 'Value found'

    # @{...:-Set if absent}
    assert c['section']['default'] == 'Default value'
    os.environ['DEFAULT'] = 'Set value'
    assert c['section']['default'] == 'Set value'
