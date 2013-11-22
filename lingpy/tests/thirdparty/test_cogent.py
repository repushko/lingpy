# author   : Johann-Mattis List
# email    : mattis.list@uni-marburg.de
# created  : 2013-11-20 20:02
# modified : 2013-11-20 20:02
"""
Test thirdparty modules.
"""

__author__="Johann-Mattis List"
__date__="2013-11-20"

import os
from lingpy.thirdparty.cogent import LoadTree
from lingpy.settings import rcParams

def test_LoadTree():
    
    # test to load a given tree-file
    tree = LoadTree(os.path.join(rcParams['_path'], 'tests', 'test_data',
        'phylogeny.tre'))
    
    taxa = sorted(["Beijing", "Changsha", "Chengdu", "Fuzhou",
            "Guangzhou", "Guiyang", "Haerbin", "Haikou", "Hangzhou", "Hefei",
            "Huhehaote", "Jian\u2019ou", "Jinan", "Kunming", "Lanzhou",
            "Meixian", "Nanchang", "Nanjing", "Nanning", "Pingyao", "Qingdao",
            "Shanghai", "Shantou", "Shexian", "Suzhou", "Taibei", "Taiyuan",
            "Taoyuan", "Tianjin", "Tunxi", "Wenzhou", "Wuhan", "Wulumuqi",
            "Xi\u2019an", "Xiamen", "Xianggang", "Xiangtan", "Xining",
            "Yinchuan", "Zhengzhou"])
    
    for a,b in zip(sorted(tree.taxa), taxa):
        assert a == b
    
    tree = LoadTree("((((((((Taiyuan,Pingyao,Huhehaote),((((Xi’an,Xining,Zhengzhou),(Lanzhou,Yinchuan,Wulumuqi)),(((Tianjin,Jinan),Qingdao),Beijing,Haerbin)),(((Guiyang,Kunming),Chengdu,Wuhan),(Nanjing,Hefei)))),(Xiangtan,Changsha)),Nanchang),(Shexian,Tunxi)),((Shanghai,Suzhou,Hangzhou),Wenzhou)),(((Xianggang,Guangzhou),Nanning),(Meixian,Taoyuan))),((((Xiamen,Taibei),Shantou,Haikou),Fuzhou),Jian’ou));")

    for a,b in zip(sorted(tree.taxa), taxa):
        assert a == b