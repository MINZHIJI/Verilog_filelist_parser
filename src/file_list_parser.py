import re
import logging
import sys
import os


class file_list_parser:
    def __init__(self) -> None:
        self.logger = logging.getLogger(__name__)
        FORMAT = "[%(filename)s:%(lineno)s - %(funcName)20s() ] %(message)s"
        logging.basicConfig(format=FORMAT)
        self.logger.setLevel(logging.DEBUG)
        self.__version = "1.0.0"
        self.__auther = "MIN-ZHI"
        self.__description = "The class is for parsing the file list of Verilog file list in VCS simulator and Xcelium."
        self.regex_set = {
            "comments": r'^\s*(#|//).*',
            "file": r'^\s*(.*)\s*',
            "filelist": r'^\s*(-f)\s+(.*)\s*',
            "incdir": r'^\s*(\+incdir\+)(.*)\s*',
            "env_var": r'(\$\w+)'
        }
        self.file_list = []
        self.env_var_dict = {}

    def main(self,f_handler):
        # NOTE: return the list parsed
        self.parse_filelist(f_handler)
        for idx, item in enumerate(self.file_list):
            if(item[0] != "comments"):
                self.logger.debug(f"{item}")
        return self.file_list
    def parse_filelist(self, f_handler):
        lines = f_handler.readlines()
        for line in lines:
            item= self.parse_rule(line)
            # try:
            #     if(item[0] != "comments"):
            #         self.file_list.append(item)
            # except:
            #     pass
    def parse_rule(self, str):
        # NOTE: Comment
        key = "comments"
        pattern = re.compile(self.regex_set[key])
        matches = pattern.match(str)
        if(matches):
            self.logger.debug("[%s] %s"%(key,str.rstrip()))
            self.file_list.append([key, str])
            return None
            # return [key, ""]
        # else:
        #     self.logger.debug("[OTHERS]  %s"%str)
        #     pass

        # NOTE: Filelist
        key = "filelist"
        pattern = re.compile(self.regex_set[key])
        matches = pattern.match(str)
        if(matches):
            str = matches.group(2)
            self.logger.debug("[%s] %s"%(key,str))
            self.parse_path(str)
            self.file_list.append([key, str])
            # NOTE: recursively trace
            try:
                str = self.extend_path_with_env_var(str)
                f_handler = open(str, 'r')
                self.parse_filelist(f_handler)
                # return [key, str]
                return None
            except OSError:
                self.logger.error(f"Can't open file: {str}")
                sys.exit()
            # return [key,matches.group(2).rstrip()]
        # else:
        #     self.logger.debug("[OTHERS]  %s"%str)
        #     pass

        # NOTE: incdir
        key = "incdir"
        pattern = re.compile(self.regex_set[key])
        matches = pattern.match(str)
        if(matches):
            str = matches.group(2).rstrip()
            self.logger.debug("[%s] %s"%(key,str))
            self.parse_path(str)
            self.file_list.append([key, str])
            return None
            # return [key,str]
        else:        
        # NOTE: file
            str = re.sub(r"\s+", "", str)
            if(str != ""):
                self.logger.debug("[%s] %s"%("file",str))
                self.parse_path(str)
                self.file_list.append(["file", str])
                return None
                # return ["file",str]
    def parse_path(self,str):
        # TODO: Parse path with environment variable/absolute path/relative path
        # NOTE: Use regex to get the env var
        pattern = re.compile(self.regex_set["env_var"])
        matches = pattern.findall(str)
        if(matches):
            # The path included the env var
            self.add_env_var(str, matches)
        
    def add_env_var(self,str,env_var_list):
        # NOTE: Check if the environment variable exists
        for item in env_var_list:
            # NOTE: Scan all environment and add them into dict(env_var_dict)
            try:
                self.logger.debug(f"{item}={os.environ[item[1:]]}")
            except Exception as e:
                self.env_var_dict[item[1:]] = None
            self.env_var_dict[item[1:]] = os.environ[item[1:]]

    def extend_path_with_env_var(sel,str):
        # NOTE: Replace the environment variables
        str_path = os.path.expandvars(str)
        return str_path
    def get_env_var_dict(self):
        self.logger.debug(self.env_var_dict)
        return self.env_var_dict
    def get_files(self):
        files = []
        for item in self.file_list:
            if(item[0] == "file"):
                files.append(item[1])
        return files
    def get_incdirs(self):
        idirs = []
        for item in self.file_list:
            if(item[0] == "incdir"):
                idirs.append(item[1])
        return idirs
    def get_full_path(self,str):
        # TODO: Check if the path is absolute path or relative path
        # NOTE: Check if the path is absolute path
        if(os.path.isabs(str)):
            return str
        # NOTE: Check if the path is relative path
        elif(os.path.isfile(str)):
            return os.path.abspath(str)
if __name__ == "__main__":
    pass