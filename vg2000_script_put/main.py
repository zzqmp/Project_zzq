# coding=utf-8
import time
import xlrd
import os
import json
from jinja2 import Template
import numpy as np

area_code_id: str
tel_excl_and_small = "./bignum_cornet_pass.xlsx"  #有大号，小号
tel_num_excl_big_only= "./bignum_pass.xlsx"  #只有大号
tel_num_excl = ""
area_ims_file = "./area_code.json"
jsObj = json.load(open(area_ims_file,encoding="utf-8"))
Config_Template = "./hl_ims_Template.j2"
ip_add = ""
netmask = ""
ip_gw = ""
table_row_num: int
table_col_num: int
def menu():
    print("\n \n===========================欢迎使用迈普语音配置生成器===========================")
    print("#请提前准备设备配置相关资料（大号  小号  注册密码）,并将其填入该程序目录下zzq.xlsx表格中")
    time.sleep(0.5)
    print("下面进入我们脚本的生成流程吧！")
    global area_code_id,ip_add,netmask,ip_gw,tel_num_excl
    while True:
        area_code_id = input(
            "请输入您的所在地区[0(哈尔滨) 1(大庆) 2(绥化) "
            "3(齐齐哈尔) 4(牡丹江) 5(伊春) 6(黑河) 7(大兴安岭) 8(双鸭山) "
            "9 (鸡西) 10(七台河) : "
        )
        if area_code_id != "":
            break
    while True:
        ip_add = input("输入接口IP地址:")
        if ip_add != "":
            break
    while True:
        netmask = input("输入掩码:")
        if netmask != "":
            break
    while True:
        ip_gw = input("输入网关:")
        if ip_gw != "":
            break
    while True:
        te_type= input("是否存在小号?(y/n):")
        if te_type != "y" or te_type != "n":
            if te_type == "y":
                tel_num_excl = tel_excl_and_small
            else:
                tel_num_excl = tel_num_excl_big_only
            break
# 参数：配置模板，电话号码信息[大号，小号，密码]，IMS其他信息[接口ip,接口掩码,网关地址，IMS地址，区域号]
def Build_configuration(template_ims,tel_num_list,ims_inform):
    global table_row_num,table_col_num
    with (open(template_ims)) as f:
        ims_template = Template(f.read())
    ims_config = ims_template.render(
        ims_ip = ims_inform["ims_ip"],
        ip_address = ims_inform["ip_address"],
        netmask = ims_inform["netmask"],
        area_code = ims_inform["area_code"],
        ip_gw = ims_inform["ip_gw"],
        row_num = table_row_num-1,
        tel_bg_num = tel_num_list,
        area_id = ims_inform["area_code"].lstrip("0"),
        tel_col_num = len(np.array(tel_num_list).shape)
    )
    with open("config.txt","w+") as f:
        f.write(ims_config)
    time.sleep(2)
    print("配置生成完毕！")
def get_tel_num():
    global table_row_num,table_col_num, tel_num_pass
    tel_num_data = xlrd.open_workbook(tel_num_excl)
    table = tel_num_data.sheets()[0]
    table_row_num = table.nrows  # 行数
    table_col_num = table.ncols  # 列数
    if table_col_num == 3:
        test_col_0 = table.col_values(0, start_rowx=1, end_rowx=None)
        test_col_1 = table.col_values(1, start_rowx=1, end_rowx=None)
        test_col_2 = table.col_values(2, start_rowx=1, end_rowx=None)
        tel_b_num = []
        tel_s_num = []
        tel_pass = test_col_2
        for f_0,f_1 in zip(test_col_0,test_col_1):
            tel_b_num.append(int(f_0))
            tel_s_num.append(int(f_1))
        # test = table.row_values(0, start_colx=0, end_colx=None)
        tel_num_pass =[tel_b_num,tel_s_num,tel_pass]
    elif table_col_num == 2:
        test_col_0 = table.col_values(0, start_rowx=1, end_rowx=None)
        test_col_1 = table.col_values(1, start_rowx=1, end_rowx=None)
        tel_b_num = []
        tel_pass = test_col_1
        for f_0 in test_col_0:
            tel_b_num.append(int(f_0))
        # test = table.row_values(0, start_colx=0, end_colx=None)
        tel_num_pass = [tel_b_num, tel_pass]
    return tel_num_pass
def get_dict(area_ims):
    #整合信息，将接口IP地址、掩码、网关、ims_ip、区号整理成字典返回！
    global  area_code_id,table_col_num,table_row_num
    area_ims_list = area_ims[area_code_id]  #根据area_id输出IMS服务器IP和区号
    ims_inform_dict={
        "ip_address": ip_add,
        "netmask": netmask,
        "ip_gw": ip_gw,
        "ims_ip":area_ims_list["ims"],
        "area_code": area_ims_list["area_id"]
    }
    return ims_inform_dict
if __name__ == "__main__":
    menu()
    tel_num_list = get_tel_num() #获取到的表格中的大号，小号和密码
    ims_inform_dict = get_dict(jsObj)
    # 参数：配置模板，电话号码信息[大号，小号，密码]，IMS其他信息[接口ip,接口掩码,网关地址，IMS地址，区域号]
    Build_configuration(Config_Template,tel_num_list,ims_inform_dict)
