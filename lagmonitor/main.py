"""

Usage:
    main [options]

Options:
    --config-file=<file>        Config file path.
"""
import os
import yaml
import threading
from time import sleep
from docopt import docopt
from lagmonitor.monitor import Monitor


def main(arguments=None):
    if not arguments:
        arguments = docopt(__doc__)
    app_config = configure(arguments['--config-file'])
    check_interval = app_config['monitor']['check_interval']
    start_timer(check_interval, app_config)


def configure(filename):
    if os.path.exists(filename) is False:
        raise IOError("{0} does not exist".format(filename))

    with open(filename) as config_file:
        config_data = yaml.load(config_file)

    return config_data


def start_timer(interval, app_config):
    threading.Timer(interval, report, args=(interval, app_config)).start()


def report(interval, app_config):
    sleep(interval)
    monitor = Monitor(app_config)
    monitor.report()
    threading.Timer(interval, report, args=(interval, app_config)).start()

if __name__ == "__main__":
    main()
