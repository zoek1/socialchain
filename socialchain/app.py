import uuid
from datetime import datetime
from math import ceil

import pytz
from flask import Flask, request, render_template, jsonify
from neomodel import config, db
from web3 import Web3
from hexbytes import HexBytes
from eth_account.messages import encode_defunct
from flask_jwt_extended import create_access_token
from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

from .model import Address, Post, Action, Comment
from .utils import get_address_or_create, get_user_activity

config.DATABASE_URL = 'bolt://neo4j:socialchain@localhost:7687'  # default

app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = "super-secret"  # Change this!
jwt = JWTManager(app)


@app.route("/login", methods=["POST"])
def login():
    address = request.json.get("address").lower()
    signature = request.json.get("signature")

    address = Address.nodes.get_or_none(address=address)

    text = "I love socialchain!"
    ref = get_address_from_signature(signature, text).lower()
    print(address)
    print(ref)
    if address and address.address.encode('utf-8') == ref.encode('utf-8'):
        access_token = create_access_token(identity=address.address)
        return jsonify(access_token=access_token)

    return jsonify({"msg": "Bad username or password"}), 401


@app.route("/")
def index():
    return render_template('index.html')


def get_address_from_signature(signature, text):
    w3 = Web3(Web3.HTTPProvider(""))
    message = encode_defunct(text=text)
    address = w3.eth.account.recover_message(message, signature=HexBytes(signature))

    return address

@app.route("/api/v1/activity")
@jwt_required()
def activity():
    address = request.args.get("address", get_jwt_identity()).lower()
    page = int(request.args.get("page", 1))
    count = int(request.args.get("count", 150))
    if page <= 0:
        page = 1

    if count <= 0:
        count = 150

    from_ = Address.nodes.get_or_none(address=address)
    if not from_:
        from_ = get_address_or_create(Address, address)
        get_user_activity(address)
    user_activity = from_.activity(page=page, count=count)

    return {
        "status": 200,
        "pages": ceil(from_.total_activity() / count),
        "page": page,
        "count": count,
        "data": user_activity,

    }


@app.route("/api/v1/timeline")
@jwt_required()
def timeline():
    address = get_jwt_identity().lower()
    from_ = Address.nodes.get_or_none(address=address)
    page = int(request.args.get("page", 1))
    count = int(request.args.get("count", 150))
    if page <= 0:
        page = 1

    if count <= 0:
        count = 150

    if not from_:
        from_ = get_address_or_create(Address, address)
        get_user_activity(address)

    user_timeline = from_.timeline(page=page, count=count)

    return {
        "status": 200,
        "pages": ceil(from_.total_timeline() / count),
        "page": page,
        "count": count,
        "data": user_timeline
    }


@app.route("/api/v1/follow", methods=["POST"])
@jwt_required()
def follow():
    address = get_jwt_identity().lower()
    follow_address = request.json.get("to").lower()

    from_address = Address.nodes.get_or_none(address=address)
    if not from_address:
        from_address = get_address_or_create(Address, address)
        get_user_activity(address)

    to_address = Address.nodes.get_or_none(address=follow_address)
    if not to_address:
        to_address = get_address_or_create(Address, address)
        get_user_activity(to_address)

    if not from_address.follow.is_connected(to_address):
        from_address.follow.connect(to_address)

    return {
        "status": 200,
        "data": {
            "following": from_address.follow.is_connected(to_address)
        }
    }

@app.route("/api/v1/unfollow", methods=["POST"])
@jwt_required()
def unfollow():
    address = get_jwt_identity().lower()
    follow_address = request.json.get("to").lower()

    from_address = Address.nodes.get_or_none(address=address)
    if not from_address:
        from_address = get_address_or_create(Address, address)
        get_user_activity(address)

    to_address = Address.nodes.get_or_none(address=follow_address)
    if not to_address:
        to_address = get_address_or_create(Address, address)
        get_user_activity(to_address)

    from_address.follow.disconnect(to_address)

    return {
        "status": 200,
        "data": {
            "following": from_address.follow.is_connected(to_address)
        }
    }


@app.route("/api/v1/like", methods=["POST"])
@jwt_required()
def like():
    address = get_jwt_identity().lower()
    action_hash = request.json.get("action").lower()

    action = Action.nodes.get_or_none(tx_hash=action_hash)
    from_address = Address.nodes.get_or_none(address=address)

    if not action.like.is_connected(from_address):
        action.like.connect(from_address)

    return {
        "status": 200,
        "data": {
            "like": action.like.is_connected(from_address)
        }
    }


@app.route("/api/v1/unlike", methods=["POST"])
@jwt_required()
def unlike():
    address = get_jwt_identity().lower()
    action_hash = request.json.get("action").lower()

    action = Action.nodes.get_or_none(tx_hash=action_hash)
    from_address = Address.nodes.get_or_none(address=address)

    if action.like.is_connected(from_address):
        action.like.disconnect(from_address)

    return {
        "status": 200,
        "data": {
            "like": action.like.is_connected(from_address)
        }
    }


@app.route("/api/v1/share", methods=["POST"])
@jwt_required()
def share():
    address = get_jwt_identity().lower()
    action_hash = request.json.get("action").lower()

    action = Action.nodes.get_or_none(tx_hash=action_hash)
    from_address = Address.nodes.get_or_none(address=address)

    if not action.share.is_connected(from_address):
        action.share.connect(from_address)

    return {
        "status": 200,
        "data": {
            "share": action.share.is_connected(from_address)
        }
    }


@app.route("/api/v1/share", methods=["POST"])
@jwt_required()
def unshare():
    address = get_jwt_identity().lower()
    action_hash = request.json.get("action").lower()

    action = Action.nodes.get_or_none(tx_hash=action_hash)
    from_address = Address.nodes.get_or_none(address=address)

    if action.share.is_connected(from_address):
        action.share.disconnect(from_address)

    return {
        "status": 200,
        "data": {
            "share": action.share.is_connected(from_address)
        }
    }


@app.route("/api/v1/following")
@jwt_required()
def following():
    address = get_jwt_identity().lower()
    follow_address = request.json.get("to").lower()
    from_address = Address.nodes.get_or_none(address=address)

    return {
        "status": 200,
        "data": {
            "following": True if from_address.follow.get_or_none(address=follow_address) else False
        }
    }

@app.route("/api/v1/post", methods=["POST"])
@jwt_required()
def post():
    address = get_jwt_identity().lower()
    from_address = Address.nodes.get_or_none(address=address)

    text = request.args.get("text")
    post = Post(text=text,
                timestamp = datetime.now(pytz.utc),
                tx_hash=str(uuid.uuid4()),
                type="post",
                tag="post"
                ).save()

    post.address_from.connect(from_address)

    return {
        "status": 200,
        "data": post.to_json()
    }


@app.route("/api/v1/comment", methods=["POST"])
@jwt_required()
def comment():
    address = get_jwt_identity().lower()
    action_hash = request.json.get("action").lower()

    from_address = Address.nodes.get_or_none(address=address)
    action = Action.nodes.get_or_none(tx_hash=action_hash)

    text = request.args.get("text")
    comment = Comment(text=text,
                      timestamp=datetime.now(pytz.utc),
                      ).save()
    comment.commenter.connect(from_address)
    comment.action.connect(action)

    return {
        "status": 200,
        "data": comment.to_json()
    }


@app.route("/api/v1/comments")
@jwt_required()
def comments():
    address = get_jwt_identity().lower()
    from_address = Address.nodes.get_or_none(address=address)
    comments = from_address.posts.all()

    return {
        "status": 200,
        "data": [comment.to_json() for comment in comments]
    }


@app.route("/api/v1/refresh", methods=["POST"])
@jwt_required()
def refresh():
    address = request.json.get("address").lower()

    from_address = Address.nodes.get_or_none(address=address)
    if not from_address:
        from_address = get_address_or_create(Address, address)
    get_user_activity(address)

    return {
        "status": 200,
        "data": ""
    }
