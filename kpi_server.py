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
    header("Content-type: json")
    return {
        "num": escape(num),
        "name": r_person.hget(escape(num), "name"),
        "level": r_person.hget(escape(num), "level"),
        "team": r_person.hget(escape(num), "team"),
        "index": {
            "study": r_person.hget(escape(num), "study_index"),
            "creativity": r_person.hget(escape(num), "creativity_index"),
            "responsibility": r_person.hget(escape(num), "responsibility_index")
        }
    }


@app.route('/updateperson/', methods=['POST'])
def updateperson():
    num = request.form["num"]
    r_person.hset(num, "num", num)
    r_person.hset(num, "name", request.form["name"])
    r_person.hset(num, "level", request.form["level"])
    r_person.hset(num, "team", request.form["team"])
    r_person.hset(num, "study_index", request.form["study_index"])
    r_person.hset(num, "creativity_index", request.form["creativity_index"])
    r_person.hset(num, "responsibility_index",
                  request.form["responsibility_index"])
    return "ok"


@app.route('/getteam/<num>', methods=['GET'])
def getteam(num):
    header("Content-type: json")
    return {
        "num": num,
        "name": r_team.hget(num, "name"),
        "scale": r_team.hget(num, "scale"),
        "detail": {
            "l0": r_team.hget(num, "l0"),
            "l1": r_team.hget(num, "l1"),
            "l2": r_team.hget(num, "l2"),
            "l3": r_team.hget(num, "l3")
        }
    }


@app.route('/updateteam/', methods=['POST'])
def updateteam():
    num = request.form["num"]
    r_team.hset(num, "num", num)
    r_team.hset(num, "name", request.form["name"])
    r_team.hset(num, "scale", request.form["scale"])
    r_team.hset(num, "l0", request.form["l0"])
    r_team.hset(num, "l1", request.form["l1"])
    r_team.hset(num, "l2", request.form["l2"])
    r_team.hset(num, "l3", request.form["l3"])
    return "ok"
