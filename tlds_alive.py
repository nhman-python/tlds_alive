import httpx
import asyncio
import sys
from tqdm import tqdm


def tlds_file(path):
    """

    :param path: the path to the tlds file
    :return: the list of tlds
    """
    try:
        with open(path, 'r') as f:
            tlds = f.read().splitlines()
            return tlds
    except PermissionError:
        print("Permission denied. Try running as root.")
    except IOError:
        print("File not found.")
    except Exception as error_load:
        raise error_load


async def check_url(base, tlds, pbar):
    """

    :param base: the base url to check
    :param tlds: the list of tlds to check
    :param pbar: the progress
    :return: the result of the check
    """
    for tld in tlds:
        url = f'https://{base}.{tld}'
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(url)
                if response:
                    pbar.write(f'alive {url}')
                else:
                    pbar.write(f'dead {url}')
        except:
            pass
        pbar.update(1)


async def main():
    """
    take the base url via sys argv and load into the check_url function
    and url run all the functions for the async the proses
    :return:
    """
    if len(sys.argv) != 3:
        print(f'Usage: {sys.argv[0]} <base_url_to_check> <number_of_urls>')
        sys.exit(1)
    else:
        base_url = sys.argv[1]
        tlds_load = tlds_file(sys.argv[2])

    total_urls = len(tlds_load)
    with tqdm(total=total_urls, desc='Checking URLs') as pbar:
        await check_url(base_url, tlds_load, pbar)


asyncio.run(main())
