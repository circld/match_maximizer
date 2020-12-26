import sys

import cli

if __name__ == "__main__":
    args = cli.parse_args()
    sys.exit(print(cli.format_output(*cli.main(args))))
