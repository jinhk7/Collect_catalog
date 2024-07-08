# -*- encoding=utf8 -*-
__author__ = "jinhk"

from airtest.core.api import *
from airtest.cli.parser import cli_setup
from openpyxl import *
import pandas as pd
import datetime


if not cli_setup():
    auto_setup(__file__, logdir=True, devices=["android://127.0.0.1:5037/RFCN305QB4P?touch_method=ADBTOUCH&",], project_root="C:/Users/jinhk/Desktop/01_xiaomi/pyxiaomi")



from poco.drivers.android.uiautomation import AndroidUiautomationPoco
poco = AndroidUiautomationPoco(use_airtest_input=True, screenshot_each_action=False)


# script content
print("start...")

#print(len(main_page.children()))

def checkSubCatalog(main_page,KEEP_GO,**data):
    if KEEP_GO == "false":
        data = {}
        sheetList = []
        if len(main_page.children()) >= 2:
            viewGroup = main_page.children()[0]
            viewGroupName = viewGroup.children()[0].children().get_text()
            data["ExcelName"] = viewGroupName
            print(viewGroupName)  # ExcelName
            for subdevices in viewGroup.children()[1].children():
                subCatalogName = subdevices.children()[1].get_text()
                print(subCatalogName) # sheetName
                sheetList.append(subCatalogName)
                data["SheetName"] = sheetList
    return data

def check_page(main_page):
    print(len(main_page.children()))
    if len(main_page.children()) >= 2:
        KEEP_GO = "false"
        return KEEP_GO
    else:
        KEEP_GO = "true"
        return KEEP_GO

def ExcelOpt(data):
    now = datetime.datetime.now()
    formatted_now = now.strftime("%Y%m%d_%H%M%S")
    ExcelName = data["ExcelName"] + formatted_now +'.xlsx'
    SheetNames = data["SheetName"]
    # 创建excel
    workbook = Workbook()
    workbook.save(ExcelName)
    # for SheetName in SheetNames:
    #     print("Creat sheet:" + SheetName + "........")
    #     workbook.create_sheet(SheetName)
    # 追加
    with pd.ExcelWriter(ExcelName, engine='openpyxl', mode='a') as writer:
        for SheetName in SheetNames:
            #print("Creat sheet:" + SheetName + "........")
            d1 = {
                "Name":[1,2,3],
                "OtherText":[1,2,3]
                }
            df1 = pd.DataFrame(d1)
            df1.to_excel(writer, sheet_name=SheetName, index=False)





# KEEP_GO = check_page()

# ExcelData = checkSubCatalog(main_page,KEEP_GO)

# ExcelOpt(ExcelData)

def collect_main_catalog():
    data=[]
    stop_flag = True
    main_page = poco("android.widget.FrameLayout").child("android.widget.LinearLayout").offspring("com.xiaomi.smarthome:id/cdt").offspring("com.xiaomi.smarthome:id/c89").offspring("com.xiaomi.smarthome:id/ctu")
    #KEEP_GO = check_page(main_page)
    # check block name
    while stop_flag:
        for viewGroup in main_page.children():
            viewGroupName = viewGroup.children()[0].children().get_text()
            if viewGroupName == "Others":
                stop_flag = False
            data.append(viewGroupName)
        try:
            poco("com.xiaomi.smarthome:id/ctu").swipe([0, -0.4])
        except poco.exceptions.PocoNoSuchNodeException:
            poco("com.xiaomi.smarthome:id/ctu").swipe([0, -0.4])
        else:
            continue

    #print(data)
    #print('---------------')
    data1 = list(filter(None ,data))
    #print(data1)
    #print('---------------')
    res = []
    res.append(data1[0])
    for i in data1:
        #print(i)
        if i != res[-1]:
            res.append(i)
    # print(res)
    init_page()
    return res

# 回到最上方
def init_page():
    init_page_flag = False
    while not init_page_flag:
        init_page_flag = poco("android.widget.FrameLayout").child("android.widget.LinearLayout").offspring("com.xiaomi.smarthome:id/cdt").child("android.widget.LinearLayout").offspring("com.xiaomi.smarthome:id/gb").exists()
        print(init_page_flag)
        poco("com.xiaomi.smarthome:id/ctu").swipe([0, 1])


# main catalog list
# main_catalog_list = collect_main_catalog()
# print(main_catalog_list)

def get_all_texts():
    texts = []
    ScanExist = poco("android.widget.FrameLayout").child("android.widget.LinearLayout").offspring("com.xiaomi.smarthome:id/c46").exists()

    if ScanExist:
        viewText = poco("android.widget.FrameLayout").child("android.widget.LinearLayout").offspring("com.xiaomi.smarthome:id/c46").get_text()
        if viewText == "Scan" or viewText == "扫描":
            texts = poco("android.widget.FrameLayout").child("android.widget.LinearLayout").offspring("com.xiaomi.smarthome:id/d0f").get_text()
        else:
            texts.append(poco("android.widget.FrameLayout").child("android.widget.LinearLayout").offspring("android.widget.LinearLayout").child("android.widget.TextView").get_text())
            gateWay_View = poco("android.widget.FrameLayout").child("android.widget.LinearLayout").offspring("com.xiaomi.smarthome:id/di5").children().children()
            for text_view in gateWay_View.child("android.widget.TextView"):
                texts.append(text_view.get_text())
    else:
        infoView = poco("android.widget.FrameLayout").child("android.widget.LinearLayout").offspring("android.widget.RelativeLayout").child("android.webkit.WebView").offspring("app")
        for text_view in infoView.child("android.widget.TextView"):
                texts.append(text_view.get_text())
    #print(ScanExist)
    return texts


def swipe_in_subpage():
    device_data = {}
    devieceNameList = []
    all_textsList = []
    poco("com.xiaomi.smarthome:id/dgf").swipe([0, -0.134375],duration=1.3)
    sleep(5)
    #subpage_views = poco("android.widget.FrameLayout").child("android.widget.LinearLayout").offspring("android:id/content").offspring("com.xiaomi.smarthome:id/dgh")
    NeedSwipe = True
    while NeedSwipe:
        subpage_views = poco("android.widget.FrameLayout").child("android.widget.LinearLayout").offspring("android:id/content").offspring("com.xiaomi.smarthome:id/dgh")
        for view in subpage_views.children():
            if view.get_size()[1] == 0.16375:
                devieceName = view.children().children()[1].get_text()
                if not devieceName in devieceNameList:
                    view.click()
                    sleep(3)
                    all_texts = get_all_texts()
                    devieceNameList.append(devieceName)
                    all_textsList.append(all_texts)
                    poco("com.xiaomi.smarthome:id/c40").click()
        NeedSwipe=check_subpage_end(subpage_views)
    device_data["deviceName"] = devieceNameList
    device_data["info"] = all_textsList
    return device_data

def check_subpage_end(subpage_views):
    NeedSwipe = True
    if len(subpage_views.children()) < 15:
        print(len(subpage_views.children()))
        print(NeedSwipe + "22222222222222222222")
        NeedSwipe = False
        return NeedSwipe
    elif len(subpage_views.children()) >= 15:
        if subpage_views[-1].get_size()[1] == 0.16375:
            devieceName_last1=subpage_views.children()[-1].children().children()[1].get_text()
            devieceName_last2=subpage_views.children()[-2].children().children()[1].get_text()
            devieceName_last3=subpage_views.children()[-3].children().children()[1].get_text()
            devieceName_last4=subpage_views.children()[-4].children().children()[1].get_text()
            if devieceName_last1 != devieceName_last2 and devieceName_last2 != devieceName_last3 and devieceName_last1 != devieceName_last4:
                NeedSwipe = False
                print(NeedSwipe + "111111111111111111111111111")
                return NeedSwipe
    else:
       poco("com.xiaomi.smarthome:id/dgf").swipe([0, -0.16375*5],duration=5)
       return NeedSwipe

#MainCatalog = collect_main_catalog()
data = swipe_in_subpage()

print(data["deviceName"])
print(data["info"])


#poco("com.xiaomi.smarthome:id/dgf").swipe([0, -0.16375*5],duration=5)