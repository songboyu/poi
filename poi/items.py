# -*- coding: utf-8 -*-

from scrapy import Item, Field


class PoiItem(Item):

    # The following attributes are str by default. They share the same name in
    # the `poi` table of mysql. Total 36 attributes.

    # ID attributes.
    # 主站ID int
    # tianya=>1 wangyi=>2 baidu=>3
    site_id = Field()
    # 用户标志
    user_id = Field()

    # Personal attributes.
    # 昵称
    name = Field()
    # 头像url
    avatar = Field()
    # 个人描述
    description = Field() 
    # 婚姻状况 char
    # S=>单身 M=>已婚 D=>离异 L=>长期恋爱中 A=>单身 想找朋友 U=>单身 不想找朋友
    # P=>分居 W=>丧偶
    marital_status = Field()
    # 教育等级 char
    # 1=>中学 2=>中专/技校 3=>大专 4=>本科 5=>双学士/硕士 6=>博士或博士以上 7=>其他
    education_level = Field()
    # 职业
    occupation = Field()
    # 年薪
    salary = Field()
    # 专长技能
    speciality = Field()
    # 性格特点
    personality = Field()
    # 各种最爱，例如运动、电影、季节、颜色
    favorites = Field()
    # 个人经历，教育、工作履历
    experience = Field()

    # Body attributes.
    # 性别 char
    # M=>男 F=>女
    gender = Field()
    # 体重
    weight = Field()
    # 身高
    height = Field()
    # 体型
    body_size = Field()
    # 相貌
    looks = Field()
    # 血型 char
    # 1=>O 2=>A 3=>B 4=>AB 5=>other
    blood_type = Field()

    # Contact attributes.
    # email
    email = Field()
    # qq
    qq = Field()
    # 移动电话
    cellphone = Field()
    # 固定电话
    telephone = Field()

    # Time attributes.
    # 最近登录时间 datetime
    last_login_time = Field()
    # 最近更新时间 datetime
    last_update_time = Field()
    # 注册时间 datetime
    reg_time = Field()
    # 生日 datetime
    birthday = Field()

    # Location attributes.
    # 现居住地
    location = Field()
    # 家乡
    hometown = Field()

    # Relation attributes.
    # 粉丝数 int
    followers = Field()
    # 关注数 int
    following = Field()
    
    # Level attributes.
    # 积分 int
    score = Field()
    # 等级
    level = Field()
    
    # Operation count attributes.
    # 登录次数 int
    login_num = Field()
    # 发帖次数 int
    post_num = Field()
    # 回帖次数 int
    reply_num = Field()
