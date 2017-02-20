# -*- coding: utf-8 -*-

import csv

ak_path = "./AccessKeyHolder/test_access_key.csv"

class AccessKeyParser:
    def __init__(self, path=ak_path):
        self.__AccessKeyId, self.__AccessKeySecrect = self.AkParsing(path)

    def AkParsing(self, path):
        with open(path, 'rb') as ak_file:
            reader = csv.reader(ak_file)
            i = 0
            for item in reader:
                if (i == 1):
                    return (item[0], item[1])
                else:
                    i += 1

    def getAccessKeyId(self):
        return self.__AccessKeyId

    def getAccessKeySecrect(self):
        return self.__AccessKeySecrect