import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('action', help='Need an action command.')
    args = parser.parse_args()
    print(args.action)


if __name__ == "__main__":
    main()
