# -*- coding: utf-8 -*-
#common_used_numerals={u'零':0,u'一':1,u'二':2,u'三':3,u'四':4,u'五':5,u'六':6,u'七':7,u'八':8,u'九':9,u'十':10,u'百':100,u'千':1000,u'万':10000,u'亿':100000000}

import string

def cn2digits_master(uchars_cn):
    uchars_cn = uchars_cn.replace(u",", u"")
    uchars_cn = uchars_cn.replace(u"，", u"")
    if is_numeric(uchars_cn):
        return uchars_cn
    if uchars_cn == u"空":
        return u"空"
    if (uchars_cn[-1] not in "0123456789") and is_numeric(uchars_cn[:-1]):
        # 9.6万， 10万
        if uchars_cn[-1] == u"万" or uchars_cn[-1] == u"萬":
            factor = 10000
        elif uchars_cn[-1] == u"千" or uchars_cn[-1] == u"仟":
            factor = 1000
        else:
            factor = None
        if factor:
            num_part = uchars_cn[:-1]
            float_num = float(num_part)
            num = float_num*factor
            return str(num)
        else:
            return uchars_cn
    else:
        num = cn2digits(uchars_cn)
        return num

def cn2digits(uchars_cn):
    cn_tra = [u'壹', u'贰', u'叁', u'肆', u'伍', u'陆', u'柒', u'捌', u'玖', u'拾', u'佰', u'仟']
    cn_sim = [u'一', u'二', u'三', u'四', u'五', u'六', u'七', u'八', u'九', u'十', u'百', u'千']
    for my_num in range(len(cn_tra)):
        uchars_cn = uchars_cn.replace(cn_tra[my_num], cn_sim[my_num])
    common_used_numerals={u'零':0,u'一':1,u'二':2,u'三':3,u'四':4,u'五':5,u'六':6,u'七':7,u'八':8,u'九':9,u'十':10,u'百':100,u'千':1000,u'万':10000,u'亿':100000000}
    s=uchars_cn
    if not s :
        return 0
    for i in [u'亿',u'万',u'千',u'百',u'十']:
        if i in s:
            ps=s.split(i)
            lp=cn2digits(ps[0])
            if lp==0:
                lp=1
            rp=cn2digits(ps[1])
            #print i,s,lp,rp
            return lp*common_used_numerals.get(i, 0)+rp
    return common_used_numerals.get(s[-1], 0)

def is_numeric(my_str):
    flag = True
    num_str = "0123456789." 
    for character in my_str:
        if character not in num_str:
            flag = False
            break
    return flag

def cn2date(my_str):
    if my_str == u"空":
        return u"空"
    my_str = my_str.replace(u"年", u"-")
    my_str = my_str.replace(u"月", u"-")
    my_str = my_str.replace(u"日", u"")
    return my_str

def handle_punctuations(obj_str):
    del_str = u"\n\r\t  ~`!@#$%^&*()_+-=	{}|[]\\:\";\'<>?,./~·！@#￥%……&*（）——+-=【】、{}|；‘：“，。、《》？	"
    for char in del_str:
        obj_str = obj_str.replace(char, u" ")
    return obj_str

if __name__ == "__main__":
    print(cn2digits_master(u'28.56万'))
    print(cn2digits_master(u'20万'))
    print(cn2digits_master(u'200000'))
    # print(is_numeric('111哇'))