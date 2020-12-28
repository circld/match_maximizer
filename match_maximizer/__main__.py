import sys

import match_maximizer.cli as cli

args = cli.parse_args()
sys.exit(print(cli.format_output(*cli.main(args))))
