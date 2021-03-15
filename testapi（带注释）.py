import requests

payload = {
    "num": 20190105,  # 学号
    "name": "Yokey",  # 姓名
    "level": "Chief Engineer",  # 职称
    "team": 1,  # 所属团队编号
    "study_index": 99,  # 学习力指数
    "creativity_index": 99,  # 创造力指数
    "responsibility_index": 99  # 责任力指数
}

# 更新某个人的信息，以学号作为键
r = requests.post('http://127.0.0.1:5000/updateperson', data=payload)

payload = {
    "num": 1,  # 团队编号
    "name": "EM",  # 团队名
    "scale": 30,  # 团队规模
    "l0": 99,  # 团队 0 级人数
    "l1": 99,  # 团队 1 级人数
    "l2": 99,  # 团队 2 级人数
    "l3": 99  # 团队 3 级人数
}

# 更新某团队的信息，以团队编号作为键
r = requests.post('http://127.0.0.1:5000/updateteam', data=payload)


# 用学号获取指定成员的信息
r = requests.get("http://127.0.0.1:5000/getperson/20190105")
print(r.url)
print(r.text)

# 用团队编号获取指定团队的信息
r = requests.get("http://127.0.0.1:5000/getteam/1")
print(r.url)
print(r.text)
