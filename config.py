import sys

defaults = './config.defaults'


def parse(conf):
    cfg = open(conf, 'r').read()
    exec(cfg, globals())


def init(conf):
    try:
        parse(defaults)
    except:
        sys.stderr.write('can\'t parse config.defaults: <%s>\n' % (defaults,))
        raise
    try:
        parse(conf)
    except:
        sys.stderr.write('can\'t parse configuration file: <%s>\n' % (conf,))
        raise
