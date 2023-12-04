'''
helper functions for scraping
Nov 2023 SK
Python3.10.12 Ubuntu22

For the module 'googlesearch' install 'google', NOT 'googlesearch-python'
https://python-googlesearch.readthedocs.io/en/latest/

```bash
pip install google
```

'''

import os
import sys
import json
import re
import warnings
# from googlesearch import search


class HelperFunctions:
    '''
    Helper functions for scraping.
    Do not instantiate this class.
    All methods are meant to be called statically.
    Just call it like:
        from helper_functions import HelperFunctions
        HelperFunctions.method_name()
    '''

    @staticmethod
    def filter_str(test_subject, filter_lst=[]):
        '''
        Check test_subject(str) if it contains all the expression in the list.
        Returns True only when all expressions are found.
        '''
        for expression in filter_lst:
            match_obj = re.search(expression, test_subject)

            if match_obj is None:
                return False

        return True


    # @classmethod
    # def get_google_results(cls, keywords, add2end='', filter_phrase=[], stop=500, pause=3, num=5, tld='co.in', max_urls=100):
    #     '''
    #     Get the urls up to max_urls of the top google searches.
    #     Returns empty list if no results are found.
    #     '''
    #     query     = keywords + ' ' + add2end
    #     url_lst   = []
    #     url_count = 0

    #     for url in search(query, tld, num, stop, pause): # https://python-googlesearch.readthedocs.io/en/latest/

    #         # add only urls that pass the filter
    #         if cls.filter_str(url, filter_phrase):
    #             url_lst.append(url)
    #             url_count += 1
    #         else:
    #             print('Filtered out: ' + url)

    #         if (url_count == max_urls):
    #             break

    #     return url_lst

    @staticmethod
    def export_json(out_data, fpath, encode=None, indent=4, force=True):
        '''
        takes list of dictionaries and exports a json file to a specified path with a specified file name
        If directory does not exist, it will be created.
        '''
        # split the path and file name
        directory, _ = os.path.split(fpath)

        # check if directory exists
        if not os.path.exists(directory):
            if not force:
                warnings.warn('Directory not found, exiting: ' + str(directory))
                return
            # create directory if it does not exist
            try:
                os.makedirs(directory)
            except PermissionError:
                warnings.warn('Write permission denied, exiting: ' + str(directory))
                return

        try:
            with open(fpath, 'w', encoding=encode) as file:
                json.dump(out_data, file, indent=indent)
        # write permission error
        except PermissionError:
            warnings.warn('Write permission denied: ' + str(fpath))
        except Exception as err:
            warnings.warn('Unknown error: ' + str(err))


    @staticmethod
    def import_json(fpath, decode=None, content_is_str=False):
        '''
        Takes a json file and imports it
        If you are certain that the content is a string, set content_is_str to True
        '''
        try:
            with open(fpath, 'r', encoding=decode) as file:
                data = json.load(file)
        except FileNotFoundError:
            warnings.warn('File not found: ' + str(fpath))
            return
        except PermissionError:
            warnings.warn('Read permission denied: ' + str(fpath))
            return

        # sometimes data comes out as a str, in that case, convert it to a list/dict
        if not content_is_str and isinstance(data, str):
            data = json.loads(data)

        return data

    @staticmethod
    def camel2snake(phrase):
        '''
        Converts camelCase to snake_case
        '''
        return re.sub(r'(?<!^)(?=[A-Z])', '_', phrase).lower()


class AddPath():
    '''
    safely add a path to sys.path for importing modules

    sys.path.insert might not add the path if it is already there
    and sys.path.remove might remove the wrong path if it occurs

    reference:
    https://stackoverflow.com/questions/17211078/how-to-temporarily-modify-sys-path-in-python

    Parameters
    ----------
    path : str
        path to add to sys.path
        always absolute path

    Example
    -------
    lib_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'path', 'to', 'lib')
    with AddPath(lib_path):
        module = __import__('mymodule')

    '''
    def __init__(self, path):
        self.path = path

    def __enter__(self):
        sys.path.insert(0, self.path)

    def __exit__(self, exc_type, exc_value, traceback):
        try:
            sys.path.remove(self.path)
        except ValueError:
            pass


class JumpDir():
    '''
    change directory for reading/saving files, importing modules and other operations and return to the original directory

    Parameters
    ----------
    target_path : str
        path to change to
        can be relative path

    start_path : str
        path of starting returning directory
        absulute path is recommended

    Example
    -------
    for jupyter notebook, use os.getcwd() instead of __file__
    jupyter notebook cannnot know the location of the script so manually check your path

    with JumpDir(os.path.join('..', 'paht', 'to', 'lib'), os.path.dirname(os.path.abspath(__file__))):
        contents = os.listdir()

    '''
    def __init__(self, target_path, start_path):
        self.path = target_path
        self.home = start_path

    def __enter__(self):

        # check if current directory is the location of the script
        if os.getcwd() != self.home:
            os.chdir(self.home)
            print('current directory is not the location of the script')
            print(f'cd {self.home}')

        try:
            os.chdir(self.path)
        except FileNotFoundError:
            print(f'path does not exist: {self.path}')
            print(f'your current path  : {os.getcwd()}')
            raise

    def __exit__(self, exc_type, exc_value, traceback):
        os.chdir(self.home)