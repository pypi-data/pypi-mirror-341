import argparse
from subdomain_permut.permut_methods import SimplePermut
from subdomain_permut.keywords import SimpleGet
from subdomain_permut import __version__

# globals
global global_keywords, global_args
global_keywords = []
global_args = None
global_arr_buffer_size = 0

def parse_args():
    parser = argparse.ArgumentParser(description="Subdomain permutation tool")
    parser.add_argument('--list', '-l', help='Subdomains list')
    parser.add_argument('--domain', '-d', help="Domain name for the target")
    parser.add_argument('--level', type=int, default=2, help="Number of iterations to run through (default=2)")
    parser.add_argument('--output', '-o', default='permut.txt', help='Output file name (default=permut.txt)')
    parser.add_argument('--enrich', '-e', help='Enrich using given wordlist')
    parser.add_argument('--method', '-m', default='subdotsub', help='Subdomain Permutation methods to use (comma-separated). Run with --ls flag to see the list (default=subdotsub)')
    parser.add_argument('--ls', action='store_true', help='List permutation methods')
    parser.add_argument('--verbose', '-v', action='store_true', help="Verbose output")
    parser.add_argument('--yes', '-y', action='store_true', help="Skip all confirmations shown (if any)")
    parser.add_argument('--version', action='store_true', help='Print version information and exit')
    args = parser.parse_args()
    return args


def main():
    args = parse_args()

    # print version information
    if args.version:
        print(f'Subdomain Permutation Tool v{__version__.__version__}')
        return

    if args.ls:
        print("""Available methods:
- all                : Run all available methods
- subdotsub          : Generate {sub}.{sub} combinations
- subsub             : Generate {sub}{sub} combinations
- subhyphensub       : Generate {sub}-{sub} combinations
- subunderscoresub   : Generate {sub}_{sub} combinations""")
        return
    
    # check if all required options are there or not
    if args.domain == None or args.list == None:
        print('[!] --domain/-d and --list/-l flags are required for permutation')
        exit(1)

    if args.verbose:
        print(f'[i] Domain             : {args.domain}')
        print(f'[i] Output file        : {args.output}')
        print(f'[i] Level              : {args.level}')
    
    # empty the file
    open(args.output, 'w').write('')
    # get keywords from subdomains file
    keywords = SimpleGet.get_keywords(args)

    if args.enrich:
        with open(args.enrich, 'r') as file:
            for line in file:
                line = line.rstrip()
                if line not in keywords:
                    keywords.append(line)
    
    if args.level > 2:
        print(f'[!] Level >2. File size would be huge. Terminate this (ctrl+c) and re-run if unsure about what you\'re doing')
        while True:
            if args.yes == True:
                break
            user_ans = input('[?] Are you sure want to continue [y/n]: ').strip()
            if user_ans == 'n':
                exit(0)
            if user_ans == 'y':
                break
            else:
                print("[!] Please enter either 'y' or 'n'")
                pass
    if args.level > 3:
        print(f'[!] Level >3. Some features are unavailable above level 3. Moreover, the file sizes could be of several terabytes')
        while True:
            if args.yes == True:
                break
            user_ans = input('[?] Are you sure want to continue [y/n]: ').strip()
            if user_ans == 'n':
                exit(0)
            if user_ans == 'y':
                break
            else:
                print("[!] Please enter either 'y' or 'n'")
                pass

    # see which permutation methods are to be done
    methods = args.method.replace(' ', '').split(',')

    if 'all' in methods:
        SimplePermut.permut_sub_dot_sub(args, keywords) # {sub}.{sub} method
        SimplePermut.permut_sub_sub(args, keywords) # {sub}{sub} method
        SimplePermut.permut_sub_hyphen_sub(args, keywords) # {sub}-{sub} method
        return
    if 'subdotsub' in methods:
        # permut subdomains by {sub}.{sub} method
        SimplePermut.permut_sub_dot_sub(args, keywords)
    if 'subsub' in methods:
        # permut subdomains by {sub}{sub} method
        SimplePermut.permut_sub_sub(args, keywords)
    if 'subhyphensub' in methods:
        # permut subdomains by {sub}-{sub} method
        SimplePermut.permut_sub_hyphen_sub(args, keywords)
    if "subunderscoresub" in methods:
        # permut subdomains by {sub}-{sub} method
        SimplePermut.permut_sub_underscore_sub(args, keywords)

if __name__ == "__main__":
    main()