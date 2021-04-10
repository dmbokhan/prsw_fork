import argparse
import ipaddress
import json

from ripe.stat import announced_prefixes
from ripe.stat import rpki_validation_status


def args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-a", "--asn", type=str, required=True, help="Autonomous System Number"
    )
    parser.add_argument("-p", "--prefix", type=str, help="Prefix to validate")

    args = parser.parse_args()

    # Validate Prefix is a valid IP prefix
    if args.prefix:
        prefixes = []

        try:
            for prefix in args.prefix.split(","):
                prefixes.append(ipaddress.ip_network(prefix, strict=False))

        except:
            print("Invalid IPv4 or IPv6 prefix")
            parser.print_help()
            exit()

        args.prefix = prefixes

    return args


def main():
    # Parse arguments
    cli = args()

    # Pull all prefixes for an ASN if needed
    if not cli.prefix:
        prefixes = announced_prefixes(cli.asn)
    else:
        prefixes = cli.prefix

    for prefix in prefixes:
        resp = rpki_validation_status(cli.asn, prefix)
        status = resp.data["status"]
        roas = resp.data["validating_roas"]

        print()
        print("=" * 80)
        print(prefix)
        print("=" * 80)
        print()
        print(f"RPKI Status: {status}")

        if roas:
            print()
            print(f"ROAs:")

            line = 0

            fmt = "{:<4} {:<10} {:<20} {:<5} {:<10} {}"
            print(fmt.format("#", "Origin", "Prefix", "Max", "Validity", "Source"))
            print("-" * 80)

            for roa in roas:
                print(
                    fmt.format(
                        line,
                        roa["origin"],
                        roa["prefix"],
                        roa["max_length"],
                        roa["validity"],
                        roa["source"],
                    )
                )
                line += 1

        print()


if __name__ == "__main__":
    main()
