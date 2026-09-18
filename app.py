import argparse

from partner_discount_service import get_partner_with_discount


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("partner_id", type=int)
    arguments = parser.parse_args()
    partner = get_partner_with_discount(arguments.partner_id)
    print(partner)


if __name__ == "__main__":
    main()
