from flask import Flask, request, jsonify
from flask_cors import CORS
import json, os, random
from datetime import datetime

app = Flask(__name__)
CORS(app)

FILE="reviews.json"

if not os.path.exists(FILE):
    json.dump([], open(FILE,"w"))

def load(): return json.load(open(FILE))
def save(d): json.dump(d, open(FILE,"w"), indent=4)

# random anonymous avatar
avatars=[
"https://api.dicebear.com/7.x/adventurer/svg?seed=",
"https://api.dicebear.com/7.x/bottts/svg?seed=",
"https://api.dicebear.com/7.x/fun-emoji/svg?seed="
]

def ai_rating(anime):
    data=load()
    r=[x for x in data if x["anime"]==anime]
    if not r: return 0
    score=sum((x["upvotes"]-x["downvotes"]) for x in r)
    return round(min(max(5 + score/5,1),10),1)

@app.route("/reviews/<anime>")
def reviews(anime):
    data=load()
    return jsonify([x for x in data if x["anime"]==anime])

@app.route("/add-review",methods=["POST"])
def add_review():
    data=load()
    body=request.json
    avatar=random.choice(avatars)+str(random.randint(1,9999))

    new={
        "id":len(data)+1,
        "anime":body["anime"],
        "review":body["review"],
        "comments":[],
        "avatar":avatar,
        "upvotes":0,
        "downvotes":0,
        "date":str(datetime.now().date())
    }

    data.append(new); save(data)
    return jsonify({"msg":"added"})

@app.route("/comment/<int:id>",methods=["POST"])
def comment(id):
    data=load()
    for r in data:
        if r["id"]==id:
            r["comments"].append(request.json["text"])
    save(data)
    return jsonify({"msg":"comment added"})

@app.route("/vote/<int:id>/<v>")
def vote(id,v):
    data=load()
    for r in data:
        if r["id"]==id:
            r["upvotes"]+=1 if v=="up" else 0
            r["downvotes"]+=1 if v=="down" else 0
    save(data); return jsonify({"msg":"ok"})

@app.route("/rating/<anime>")
def rating(anime):
    return jsonify({"rating":ai_rating(anime)})

app.run(debug=True)