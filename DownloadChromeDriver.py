import os
import sys
import re
import winreg
import zipfile

import requests
from requests.auth import HTTPProxyAuth
import xmltodict
import json

import globalvar


class DownloadChromeDriver:
    chromeversion = None
    chromemainversion = None
    chromedriverurl=r"http://chromedriver.storage.googleapis.com/?delimiter=/&prefix="
    listchromemainversion=[]
    urlchromedriverversion=None
    urlchromedrivermainversion=None
    pythonpath=None
    chromedrivernotefullname = None
    username=None
    password=None


    def __init__(self):
        self.get_chromeversion()
        self.pythonpath=sys.executable[:-10]
        self.chromedrivernotefullname=self.pythonpath+r"\\chromedrivernote.txt"
        self.urlchromedrivermainversion=self.chromemainversion
        self.username = globalvar.logonusername
        self.password = globalvar.logonpassword
        pass



    def get_chromeversion(self):
        chromeversionkey=winreg.OpenKey(winreg.HKEY_CURRENT_USER,r"Software\Google\Chrome\BLBeacon")
        self.chromeversion=winreg.QueryValueEx(chromeversionkey,r"version")[0]
        repattern=r"(\d{2})."
        self.chromemainversion=re.match(repattern,self.chromeversion).groups()[0]
        print("My chrome version is {}".format(self.chromeversion))


    def getchromedriverurl(self):
        lenth=len(self.listchromemainversion)
        self.urlchromedriverversion=self.listchromemainversion[lenth-1]
        url=r"http://chromedriver.storage.googleapis.com/{0}/chromedriver_win32.zip".format(self.urlchromedriverversion)
        return url


    def isRequiredDownloadChromeDriver(self,urlchromedrivermainversion):
        bchromedrivernote=os.path.exists(self.chromedrivernotefullname)
        if(not bchromedrivernote):
            return True
        with open(self.chromedrivernotefullname,'r') as f:
            curchromedriverversion=f.readline()
            match=re.match(urlchromedrivermainversion,curchromedriverversion)
            if(match==None):
                return True
        return False

    def downloadchromedriver(self):
        sesn=requests.Session()
        proxy={"http":"proxy.huawei.com:8080"}
        auth=HTTPProxyAuth(self.username,self.password)
        rs=sesn.get(self.chromedriverurl,proxies=proxy,auth=auth)
        rsxmltext=rs.text
        jsondata=xmltodict.parse(rsxmltext)
        commonprefixes=jsondata['ListBucketResult']['CommonPrefixes']
        remainversion=self.chromemainversion
        for dordereddict in commonprefixes:
            prefix=dordereddict['Prefix']
            prefix=prefix[:-1]
            match=re.match(remainversion,prefix)
            if(match==None):
                continue
            print("chromedriver version is {}".format(prefix))
            self.listchromemainversion.append(prefix)


        if(not self.isRequiredDownloadChromeDriver(self.urlchromedrivermainversion)):
            return
        urldownloadchromedriver=self.getchromedriverurl()
        rsdownload = sesn.get(urldownloadchromedriver, proxies=proxy, auth=auth)
        savepath=r"{0}chromedriver_win32.zip".format(self.pythonpath)
        with open(savepath, 'wb') as f:
            f.write(rsdownload.content)
        #extract chromedriver_win32.zip file to python path
        zFile = zipfile.ZipFile(savepath, "r")
        # ZipFile.namelist(): 获取ZIP文档内所有文件的名称列表
        for fileM in zFile.namelist():
            zFile.extract(fileM, self.pythonpath)
        zFile.close();

        with open(self.chromedrivernotefullname,"w") as f:
            f.write(self.urlchromedriverversion)

        if os.path.exists(savepath):
            # 删除文件，可使用以下两种方法。
            os.remove(savepath)
            # os.unlink(my_file)

        pass

if __name__ == '__main__':
    dcd=DownloadChromeDriver()
    dcd.downloadchromedriver()
