from datetime import datetime

import boto3
from dateutil.tz import tzutc
from mypy_boto3_s3 import S3Client
from argparse import Namespace
import concurrent.futures

AWS_S3_GB_COST = 0.023


def get_size_in_unit(size_in_bytes, unit):
    units = {
        "b": 1,
        "kb": 1024,
        "mb": 1024 * 1024,
        "gb": 1024 * 1024 * 1024,
        "tb": 1024 * 1024 * 1024 * 1024,
    }
    return round(size_in_bytes / units[unit.lower()], 2)


def process_prefix(client, bucket_name, prefix="", storageclass=None):
    local_count = 0
    local_size = 0
    last_modified = datetime.min.replace(tzinfo=tzutc())

    paginator = client.get_paginator("list_objects_v2")

    kwargs = {"Bucket": bucket_name}
    if prefix:
        kwargs["Prefix"] = prefix

    for page in paginator.paginate(**kwargs):
        if not (contents := page.get("Contents")):
            continue

        for obj in contents:
            if obj["StorageClass"] == storageclass or storageclass is None:
                if (new_last_modified := obj["LastModified"]) > last_modified:
                    last_modified = new_last_modified
                local_count += 1
                local_size += obj["Size"]

    return {"count": local_count, "size": local_size, "last_modified": last_modified}


def get_subfolders(client, bucket_name):
    subfolders = set()

    paginator = client.get_paginator("list_objects_v2")
    for page in paginator.paginate(Bucket=bucket_name, Delimiter="/"):
        if "CommonPrefixes" in page:
            for prefix in page["CommonPrefixes"]:
                subfolders.add(prefix["Prefix"])

    return list(subfolders)


def get_bucket(name: str, unit: str, storageclass=None):
    print(f"Getting bucket with name {name}")
    s3 = boto3.resource("s3")
    client = boto3.session.Session().client("s3")

    try:
        creation_date = s3.Bucket(name).creation_date
    except Exception as e:
        print(f"Error getting bucket creation date: {e}")
        creation_date = None

    subfolders = get_subfolders(client, name)
    print(f"Found {len(subfolders)} subfolders in bucket {name}")

    all_prefixes = subfolders

    results = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
        future_to_prefix = {
            executor.submit(process_prefix, client, name, prefix, storageclass): prefix
            for prefix in all_prefixes
        }

        for future in concurrent.futures.as_completed(future_to_prefix):
            prefix = future_to_prefix[future]
            try:
                data = future.result()
                print(
                    f"Finished processing {prefix if prefix else 'root'}: {data['count']} objects"
                )
                results.append(data)
            except Exception as e:
                print(f"Error processing {prefix}: {e}")

    total_count = sum(r["count"] for r in results)
    total_size = sum(r["size"] for r in results)
    last_modified = max(
        (
            r["last_modified"]
            for r in results
            if r["last_modified"] != datetime.min.replace(tzinfo=tzutc())
        ),
        default="NOT FOUND",
    )

    cost = round(AWS_S3_GB_COST * get_size_in_unit(total_size, "gb"), 2)
    formatted_size = get_size_in_unit(total_size, unit)

    return {
        "name": name,
        "creation_date": creation_date,
        "nb_files": f"{int(total_count):,d}",
        "total_size": f"{ formatted_size } {unit}",
        "last_modified": last_modified,
        "cost": cost,
    }


def validate_region(region: str, bucket_name, client):
    bucket_region = (
        client.get_bucket_location(Bucket=bucket_name)["LocationConstraint"]
        or "us-east-1"
    )
    return region == bucket_region


def list_buckets(args: Namespace):
    client: S3Client = boto3.client("s3")

    all_buckets_info = []
    for bucket in client.list_buckets()["Buckets"]:
        bucket_name = bucket["Name"]
        if not validate_region(args.region, bucket_name, client):
            continue
        if bucket_info := get_bucket(bucket_name, args.unit):
            all_buckets_info.append(bucket_info)

    return all_buckets_info
