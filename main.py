import logging
from datetime import datetime
import argparse

from configs.default import DefaultConfig
from frontend.ducky import DuckyOne2RGB


if __name__ == '__main__':
    # ------------------------------------------------ Argparse Setup ------------------------------------------------ #
    parser = argparse.ArgumentParser(description="Optional lighting parameters.")
    parser.add_argument('-l', '--loglevel',
                        dest='loglevel',
                        type=str,
                        default="INFO",
                        help="The logging level for the bot (default: INFO) (options: INFO, WARNING, ERROR, etc.)")
    # parser.add_argument('-c', '--configuration',
    #                     dest='configuration',
    #                     type=str,
    #                     help="The configuration file to load for the lighting (see example, ends with .config)")

    args = parser.parse_args()

    # ------------------------------------- Set up logging level from parameters ------------------------------------- #
    numeric_level = getattr(logging, args.loglevel.upper(), None)
    if not isinstance(numeric_level, int):
        raise ValueError('Invalid log level: %s' % args.loglevel)

    logging.basicConfig(filename=f'_logs/{datetime.now().strftime("%m-%d-%Y %H_%M_%S.log")}',
                        level=args.loglevel,
                        format='%(levelname)s::%(asctime)s::%(message)s',
                        datefmt='%m/%d/%Y %H:%M:%S'
                        )

    # ---------------------------------------- Set up Ducky Keyboard and Run ----------------------------------------- #
    ducky = DuckyOne2RGB()
    ducky.set_config(DefaultConfig())

    ducky.run()
