import configparser
import os

config = configparser.ConfigParser()
config.sections()
#homedir = os.path.dirname(os.path.realpath(__file__))
homedir="D:\\Codes\\PycharmProjects\\Exportdata\\dist"
dstsavefolder="D:\\autostoredata\\"
config.read(homedir+'\\config.ini')

logonusername=config["DEFAULT"]["UserName"]
logonpassword=config["DEFAULT"]["Password"]
print("read ini finished.")
