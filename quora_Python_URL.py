__author__ = 'mark'
import re


class PythonURL:
    __REGEX_HOST = re.compile(
        r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'  # domain
        r'localhost|'  # localhost
        r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})',  # ip
        re.IGNORECASE)

    __REGEX_SCHEMA = re.compile(r'^(?:http|ftp)s?', re.IGNORECASE)  # http:// or https:// or ftp://

    __REGEX_PORT = re.compile(r':(\d)+', re.IGNORECASE)  # optional port

    __REGEX_PATH = '(/{1}[a-zA-Z0-9]+)+(\.[a-z]+)?'  # paths

    def __init__(self, url='', delimiter='&'):
        self.__url = url
        self.__param_delimiter = delimiter
        self.protocol = self.__find_protocol(url)
        self.hostname = self.__find_hostname(url)
        self.port = self.__find_port(url)
        self.path = self.__find_path(url)
        self.parameters = self.__get_parameters(url)

    def __find_protocol(self, url):
        """
        Returns the protocol for the given self.url.
        """
        match = self.__REGEX_SCHEMA.search(url)
        if match:
            protocol = match.group(0).split(':')[0]
            return protocol
        return None

    def __find_hostname(self, url):
        """
        Returns the host for the given self.url.
        """
        match = self.__REGEX_HOST.search(url)
        if match:
            return match.group(0)
        return None

    def __find_port(self, url):
        """
        Returns the optional port for the given self.url.
        """
        match = self.__REGEX_PORT.search(url)
        if match:
            port_num = match.group(0).split(':')[1]
            return port_num
        return None

    def __find_path(self, url):
        """
        Returns the path for the given self.url.
        """
        for matches in re.finditer(self.__REGEX_PATH, url):
            matched_groups = matches.group()
            slash_position = url.find(matched_groups) - 1
            if url[slash_position] is not None and url[slash_position] != '/':
                return matched_groups
        return None

    def __get_parameters(self, url):
        """
        Returns the tuple of GET variables for the given self.url. specify delimiter when init class
        """
        rest_url = url.split('?')
        parameter_tuple = ()
        if len(rest_url) > 1:
            target_url = rest_url[1]
            variable_pairs = target_url.split(self.__param_delimiter)
            for one_pair in variable_pairs:
                key_value_pair = one_pair.split("=")
                if len(key_value_pair) == 2:
                    parameter_tuple += (tuple(key_value_pair),)
            return parameter_tuple
        return None

    def get_ftp_user_info(self):
        """
        if url is ftp protocol, get user name and password
        """
        info_dic = {'username': None,
                    'password': None}
        if 'ftp' in self.protocol:
            start = self.__url.find('//') + 2  # Get the char after the '//'
            end = self.__url.find('@')
            if (start >= 0) and (end >= 0) and (end > start):
                info = self.__url[start:end]
                if info[0] is not ':':
                    info_pair = info.split(':')
                    if len(info_pair) > 1:
                        info_dic['username'] = info_pair[0]
                        info_dic['password'] = info_pair[1]
            return info_dic
        else:
            return None

    def get_all_info(self):
        """
        Returns all info.
        """
        basic_items = {'protocol': self.protocol,
                       'hostname': self.hostname,
                       'path': self.path,
                       'params': self.parameters,
                       'delimiter': self.__param_delimiter}
        if 'ftp' in self.protocol:
            return dict(basic_items.items() | self.get_ftp_user_info().items())
        else:
            return basic_items


