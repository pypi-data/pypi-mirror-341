from tabulate import tabulate
import argparse
from s3_lister import get_bucket, list_buckets

parser = argparse.ArgumentParser()
parser.add_argument("-b", "--bucket", help="name of the bucket to fetch", type=str)
parser.add_argument(
    "-r",
    "--region",
    help="display only buckets in specified region, ignored if --bucket or -b is specified",
    type=str,
)
parser.add_argument(
    "-u",
    "--unit",
    help="unit to return bucket size in: bytes, kb, mb, gb, tb. Defaults to bytes",
    type=str,
    choices=["b", "kb", "mb", "gb", "tb"],
    default="b",
)
parser.add_argument(
    "-s",
    "--storageclass",
    help="process only objects of a specific storageclass. Defaults to None",
    type=str,
    choices=[
        "STANDARD",
        "REDUCED_REDUNDANCY",
        "STANDARD_IA",
    ],
    default=None,
    # https://docs.aws.amazon.com/AmazonS3/latest/userguide/storage-inventory.html#storage-inventory-contents:~:text=API%20Reference.-,Storage%20class,-%E2%80%93%20The%20storage%20class
)
args = parser.parse_args()


def print_as_table(bucket_information):
    print(tabulate(bucket_information, headers="keys"))


def main():
    if args.bucket:
        if bucket_information := get_bucket(args.bucket, args.unit, args.storageclass):
            print_as_table([bucket_information])
    else:
        print_as_table(list_buckets(args))


if __name__ == "__main__":
    main()
