import argparse 
import ast
from importlib.metadata import version

def option_parser():
    parser = argparse.ArgumentParser(
        description = "Create master catalogue from multiple resolution inputs",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
)

    parser.add_argument('--version', action = 'version', version = version('vlbi-cat-creation'))

    parser.add_argument('-b', '--basic',
        help = "Basic processing of one image",
        action = 'store_true')

    parser.add_argument('-i', '--images',
        help = "Input radio images",
        type = arg_as_str_or_list, 
        default = ["test.fits"])

    return parser.parse_args()


def arg_as_list(s):
    v = ast.literal_eval(s)
    if type(v) is not list:
        raise argparse.ArgumentTypeError("Argument \"%s\" is not a list" % (s))
    return v


def arg_as_str_or_list(s):
    if "[" not in s and "]" not in s:
        return str(s)

    v = ast.literal_eval(s)
    if isinstance(v, list):
        return v

    raise argparse.ArgumentTypeError(f'Argument "{s}" is not a string or list')


def main():
    options = option_parser()
    global args
    args = vars(options)

    if args['basic']:
        from vlbi_cat_creation.create_bdsf_cat import basic_processing

        for image in args['images']:
            basic_processing(image)


if __name__ == "__main__":
    main()