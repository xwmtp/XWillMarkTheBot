import requests
import logging
import shutil
import os


### File Handling ###

def readjson(url, text_only=False, tries=5):

    for i in range(tries):
        if i > 0:
            logging.info(f"Connecting failed (status {status}), trying again... try ({i})")
        response = requests.get(url)

        status = response.status_code

        if status == 200:
            if text_only:
                return response.text
            else:
                return response.json()
        if status == 404:
            return

    error_message = "Error in accessing api:", status, "(after", tries, "tries)"
    print(error_message)
    logging.critical(error_message)


def copy_file(path, old_file_name, new_file_name):
    try:
        old = os.path.join(path, old_file_name)
        new = os.path.join(path, new_file_name)
        shutil.copy(old, new)
        return True
    except Exception:
        logging.critical(f"Error while copying {old_file_name} to {new_file_name} in {path}")
        return False


### Arithmetic ###


def mean(lst):
    lst = sorted(lst)
    logging.debug(f"Taking average over: {lst}")
    return sum(lst) / len(lst)

def median(lst):
    times = sorted(lst)

    mid = int(len(lst) / 2)

    if len(lst) % 2 == 0:
        median = (lst[mid - 1] + lst[mid]) / 2
    else:
        median = times[mid]

    return median



### List functionality ###

def reverse_dictionary(dict):

    return {value: key for key, values in dict.items() for value in values}


def is_lowercase_elem(item, lst):

    for elem in lst:
        if item.lower() == elem.lower():
            return True
    return False

def complement(lst1, lst2):
    return [x for x in lst1 if x not in lst2]

def flatten(lst):
    return [item for sublst in lst for item in sublst]
