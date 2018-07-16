#!/usr/bin/python3

# MerLink CLI
import argparse


class MainCli:
    def __init__(self):
        super(MainCli, self).__init__()

        self.parse_options()

    @staticmethod
    def parse_options():
        parser = argparse.ArgumentParser()
        parser.add_argument("-v", "--verbose", help="increase output verbosity",
                            action="store_true")
        args = parser.parse_args()
        if args.verbose:
            print("Merlink verbose option")
