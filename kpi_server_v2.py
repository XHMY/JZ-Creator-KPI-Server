from flask import Flask, request, escape
import redis

r_person = redis.Redis(host='localhost', port=6379, db=0)
r_team = redis.Redis(host='localhost', port=6379, db=1)

app = Flask(__name__)


@app.route('/')
def test():
    return str(r_person.ping())


@app.route('/getperson/<num>', methods=['GET'])
def getperson(num):
    # print(escape(num))
    ls = str(r_person.hget(escape(num), "level_symbol"), encoding='utf-8')
    tn = str(r_person.hget(escape(num), "team_num"), encoding='utf-8')
    return {
        "num": escape(num),
        "name": str(r_person.hget(escape(num), "name"), encoding='utf-8'),
        "level_symbol": ls,
        "level": str(str(r_team.hget(tn, "level_name"), encoding='utf-8').split()[int(ls[-1])]),
        "team_num": tn,
        "team_name": str(r_team.hget(tn, "name"), encoding='utf-8'),
        "index": {
            "study": str(r_person.hget(escape(num), "study_index"), encoding='utf-8'),
            "creativity": str(r_person.hget(escape(num), "creativity_index"), encoding='utf-8'),
            "responsibility": str(r_person.hget(escape(num), "responsibility_index"), encoding='utf-8')
        }
    }


@ app.route('/updateperson/', methods=['POST'])
def updateperson():

    num = request.form["num"]

    if not r_team.exists(request.form["team_num"]):
        return str(f"Error: Can not find Team {request.form['team_num']}.")

    if request.form["level_symbol"] not in {"l0", "l1", "l2", "l3"}:
        return str(f"Error: {request.form['level']} is not a standard level symbol.")

    if not r_person.exists(num):
        r_team.hset(request.form["team_num"], "scale", int(
            r_team.hget(request.form["team_num"], "scale"))+1)

        r_team.hset(request.form["team_num"], request.form["level_symbol"], int(
            r_team.hget(request.form["team_num"], request.form["level_symbol"]))+1)

    r_person.hset(num, "num", num)
    r_person.hset(num, "name", request.form["name"])
    r_person.hset(num, "level_symbol", request.form["level_symbol"])
    r_person.hset(num, "team_num", request.form["team_num"])
    r_person.hset(num, "study_index", request.form["study_index"])
    r_person.hset(num, "creativity_index", request.form["creativity_index"])
    r_person.hset(num, "responsibility_index",
                  request.form["responsibility_index"])
    return "ok"


@ app.route('/getteaminfo/<num>', methods=['GET'])
def getteaminfo(num):
    return {
        "num": num,
        "name": str(r_team.hget(num, "name"), encoding='utf-8'),
        "scale": str(r_team.hget(num, "scale"), encoding='utf-8'),
        "detail": {
            "l0": str(r_team.hget(num, "l0"), encoding='utf-8'),
            "l1": str(r_team.hget(num, "l1"), encoding='utf-8'),
            "l2": str(r_team.hget(num, "l2"), encoding='utf-8'),
            "l3": str(r_team.hget(num, "l3"), encoding='utf-8')
        }
    }


@ app.route('/getteamname/<num>', methods=['GET'])
def getteamname(num):
    return str(r_team.hget(num, "name"), encoding='utf-8')


@ app.route('/updateteam/', methods=['POST'])
def updateteam():
    num = request.form["num"]
    r_team.hset(num, "num", num)
    r_team.hset(num, "name", request.form["name"])
    r_team.hset(num, "level_name", request.form["level_name"])
    r_team.hset(num, "scale", request.form["scale"])
    r_team.hset(num, "l0", request.form["l0"])
    r_team.hset(num, "l1", request.form["l1"])
    r_team.hset(num, "l2", request.form["l2"])
    r_team.hset(num, "l3", request.form["l3"])
    return "ok"


@ app.route('/initteam/', methods=['POST'])
def initteam():
    num = request.form["num"]
    r_team.hset(num, "num", num)
    r_team.hset(num, "name", request.form["name"])
    r_team.hset(num, "level_name", request.form["level_name"])
    r_team.hset(num, "scale", 0)
    r_team.hset(num, "l0", 0)
    r_team.hset(num, "l1", 0)
    r_team.hset(num, "l2", 0)
    r_team.hset(num, "l3", 0)
    return "ok"
