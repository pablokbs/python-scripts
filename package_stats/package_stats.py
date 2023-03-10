import argparse
import urllib.request
import gzip
import io
from collections import defaultdict

DEBIAN_MIRROR_URL = "http://ftp.uk.debian.org/debian/dists/stable/main/"

def download_contents(arch):
    url = f"http://ftp.uk.debian.org/debian/dists/stable/main/Contents-{arch}.gz"
    print("Downloading Contents file from %s for arch %s\n" % (url,arch))
    response = urllib.request.urlopen(url)
    contents = gzip.decompress(response.read()).decode("utf-8")
    return contents

def get_top_packages(contents):
    packages = {}
    for line in contents.splitlines():
        try:
            filename, package = line.split(' ')
            if package in packages:
                packages[package] += 1
            else:
                packages[package] = 1
        except ValueError:
            continue
    return sorted(packages.items(), key=lambda x: x[1], reverse=True)[:10]

def output_stats(top_packages):
    print("Top 10 packages:")
    for i, (package, count) in enumerate(top_packages):
        print(f"{i+1}. {package} {count}")

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('arch', help='The architecture of the Contents index file to download')
    args = parser.parse_args()
    contents = download_contents(args.arch)
    top_packages = get_top_packages(contents)
    output_stats(top_packages)
