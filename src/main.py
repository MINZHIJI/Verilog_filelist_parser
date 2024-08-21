
import argparse
import file_list_parser
import logging

def main():
    # NOTE: Get the arguments
    parser = argparse.ArgumentParser(description='Verilog file list to parse the list and flatten the list recursively!')
    parser.add_argument('--file', '-f', type=argparse.FileType('r'), help='Add Verilog File List')
    parser.add_argument('--debug', action='store_true')
    args = parser.parse_args()
    logger = logging.getLogger(__name__)
    FORMAT = "[%(filename)8s:%(lineno)-3s - %(funcName)-20s] %(message)s"
    logging.basicConfig(format=FORMAT)
    if(args.debug):
        logger.setLevel(logging.DEBUG)
        # logging.basicConfig(level=logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)
        # logging.basicConfig(level=logging.INFO)

    f_handler = args.file
    # TODO: Check the file is exist
        # NOTE: The operation is done when type=argparse.FileType('r')
    # TODO: Add logger

    # TODO: load parser package
    flist_parser = file_list_parser.file_list_parser()
    arr = flist_parser.main(f_handler)
    for idx, item in enumerate(arr):
        logging.info(f"[{idx}] {item[0]:<8} {item[1]}")
    print(flist_parser.get_env_var_dict())
if __name__ == "__main__":
    main()