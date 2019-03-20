#!/usr/bin/env python
#coding=utf-8

#使用注意事项:该脚本基于python2.7
#os 是系统模块，对系统操作必须包含该模块
import os
#commands 模块是shell脚本模块，可以执行shell脚本指令
import commands
#requests是python的一个HTTP客户端库需要独立安装模块,可以通过pip来安装(pip install requests).
#安装pip https://blog.csdn.net/yincodes/article/details/81709162
import requests
#json解析模块
import json
#webbrowser是web浏览器操作模块，一般只执行open().打开一个浏览器
import webbrowser

#Xtrend

IpaPath = '/Users/brain/Desktop/Payload'
IpaBagPath = '/Users/brain/Desktop/ProgramBag'
appFileFullPath ='/Users/brain/Library/Developer/Xcode/DerivedData/XTrend-ejxrvqekaehluefrlumkkxxihrpg/Build/Products/Debug-iphoneos/XTrend.app'
ipaName = "xtrend.ipa"


#将此处打开的链接改为firim对应app的链接
openUrl = 'https://fir.im/XTrend'
type = "ios"
api_token = "ee248d434929148de68a21a9d382e785"
bundle_id = "com.bravely.xtrend"

name = "XTrend"
version = "2.0.0"
build = "2000"
changelog = "test auto ipa"+name+version+build

tokenUrl = 'http://api.fir.im/apps'

#上传firim
#1.获取上传所需数据->2.上传文件
#上传firim
def getUploadUrl(url):
    if(url==''):
        print "\n*************** firim获取token路径异常 *********************\n"
        return
    else:
        print "\n*************** 开始获取firim上传地址 *********************\n"
        data1= {
            'type':type,
            'bundle_id':bundle_id,
            'api_token':api_token
        }
        r=requests.post(url,data=data1)
        print('request url = %s'%r.url)
#        转换请求结果为字典
        resultData = json.loads(r.text)
        print "\n*************** firim上传地址获取成功 *********************\n"
        cert = resultData['cert']
#        print('cert =%s'%cert)

        binary = cert['binary']
#key 上传所需key
        upload_key=binary['key']
#token 上传所需token
        upload_token=binary['token']
#upload_url 上传路径
        upload_url=binary['upload_url']
#路径
        ipa_path = '%s/%s'%(IpaBagPath,ipaName)
        print "\n*************** ipa_path="+ipa_path+" *********************\n"

        x_data={
            'name':name,
            'version':version,
            'build':build,
            'changelog':changelog,
            'release_type':''
        }
        upload_data={
            'key':upload_key,
            'token':upload_token,
            'file':ipa_path,
            'x':x_data
        }
        print('upload_key = %s'%upload_key)
        print('upload_token = %s'%upload_token)
        print('upload_url = %s'%upload_url)
        uploadIPA(ipa_path,upload_data,upload_url)


#上传文件 ipa_path:ipa路径 upload_data 上传所带参数 upload_url 上传请求的url
def uploadIPA(ipa_path,upload_data,upload_url):
    if(ipa_path==''):
        print "\n*************** 没有找到对应上传的IPA包 *********************\n"
        return
    else:
        print "\n***************开始上传到firim *********************\n"
        files={'file':open(ipa_path,'rb')}
        r=requests.post(upload_url,data=upload_data,files=files)
        print "\n***************上传firim成功 *********************\n"

#打开下载网页
def openDownloadUrl():
    webbrowser.open(openUrl,new=1,autoraise=True)
    print "\n*************** 更新成功 *********************\n"


#创建文件夹方法 IpaPath 文件夹path
def mkdir(IpaPath):
    isExists = os.path.exists(IpaPath)
    if not isExists:
        os.makedirs(IpaPath)
        print IpaPath + '创建成功'
        return True
    else:
        print IpaPath + '目录已经存在'
        return False


#编译打包流程
def bulidIPA():
    #打包之前先删除IpaBagPath下的文件夹
    commands.getoutput('rm -rf %s'%IpaBagPath)
    #桌面创建文件夹
    mkdir(IpaPath)
    #将app拷贝到IpaPath路径下
    commands.getoutput('cp -r %s %s'%(appFileFullPath,IpaPath))
    #在桌面上创建IpaBagPath的文件夹
    commands.getoutput('mkdir -p %s'%IpaBagPath)
    #将IpaPath文件夹拷贝到IpaBagPath文件夹下
    commands.getoutput('cp -r %s %s'%(IpaPath,IpaBagPath))
    #删除桌面的IpaPath文件夹
    commands.getoutput('rm -rf %s'%(IpaPath))
    #切换到当前目录
    os.chdir(IpaBagPath)
    #压缩IpaBagPath文件夹下的IpaPath文件夹夹
    commands.getoutput('zip -r ./Payload.zip .')
    print "\n*************** 打包成功 *********************\n"
    #将zip文件改名为ipa
    commands.getoutput('mv Payload.zip %s'%ipaName)



if __name__ == '__main__':
#    des = input("请输入更新的日志描述:")
    #创建ipa
    bulidIPA()
    #获取权限执行上传操作
    getUploadUrl(tokenUrl)
    openDownloadUrl()


    



    

