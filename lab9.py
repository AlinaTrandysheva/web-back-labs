from flask import Blueprint, render_template, request, jsonify, session
import random

lab9 = Blueprint("lab9", __name__, url_prefix="/lab9")

BOX_IMAGES = [
    "lab9/boxes/box1.jpg",
    "lab9/boxes/box2.avif",
    "lab9/boxes/box3.webp",
    "lab9/boxes/box4.avif",
    "lab9/boxes/box5.webp",
    "lab9/boxes/box6.png",
    "lab9/boxes/box7.avif",
    "lab9/boxes/box8.png",
    "lab9/boxes/box9.webp",
    "lab9/boxes/box10.png",
]

GIFTS = [
    "lab9/gifts/gift1.png",
    "lab9/gifts/gift2.png",
    "lab9/gifts/gift3.png",
    "lab9/gifts/gift4.png",
    "lab9/gifts/gift5.png",
    "lab9/gifts/gift6.png",
    "lab9/gifts/gift7.png",
    "lab9/gifts/gift8.png",
    "lab9/gifts/gift9.webp",
    "lab9/gifts/gift10.webp",
]

CONGRATS = [
    "С Новым годом! Пусть мечты превращаются в планы, а планы — в реальность!",
    "С праздником! Пусть в новом году будет больше радости и спокойствия!",
    "С Новым годом! Желаю удачи, вдохновения и приятных сюрпризов!",
    "С праздником! Пусть рядом будут люди, которые поддерживают и радуют!",
    "С Новым годом! Пусть учёба и дела даются легко и приносят результат!",
    "С праздником! Пусть в доме будет тепло, а в душе — уверенность!",
    "С Новым годом! Желаю здоровья, энергии и отличного настроения!",
    "С праздником! Пусть каждый месяц будет по-своему счастливым!",
    "С Новым годом! Пусть всё лишнее останется в прошлом, а лучшее — впереди!",
    "С праздником! Пусть новый год принесёт много поводов улыбаться!",
]

_BOX_POSITIONS = None
_OPENED_BOXES = set()


def _ensure_positions():
    global _BOX_POSITIONS
    if _BOX_POSITIONS is not None:
        return

    positions = []
    for i, img in enumerate(BOX_IMAGES):
        positions.append({
            "id": i,
            "top": random.randint(5, 75),
            "left": random.randint(3, 85),
            "size": random.randint(80, 140),
            "img": img
        })
    _BOX_POSITIONS = positions


def _init_session_limits():
    if "opened_count" not in session:
        session["opened_count"] = 0


@lab9.route("/", methods=["GET"])
def index():
    _ensure_positions()
    _init_session_limits()

    if len(_OPENED_BOXES) == 0 and session.get("opened_count", 0) > 0:
        session["opened_count"] = 0

    unopened_total = len(BOX_IMAGES) - len(_OPENED_BOXES)

    return render_template(
        "lab9/index.html",
        boxes=_BOX_POSITIONS,
        opened_boxes=list(_OPENED_BOXES),
        unopened_total=unopened_total
    )



@lab9.route("/open", methods=["POST"])
def open_box():
    _ensure_positions()
    _init_session_limits()

    data = request.get_json(silent=True) or {}
    box_id = data.get("box_id", None)

    if box_id is None:
        return jsonify({"ok": False, "message": "Не удалось определить коробку."}), 400

    try:
        box_id = int(box_id)
    except ValueError:
        return jsonify({"ok": False, "message": "Некорректный ID коробки."}), 400

    if box_id < 0 or box_id >= len(BOX_IMAGES):
        return jsonify({"ok": False, "message": "Такой коробки не существует."}), 404

    if box_id in _OPENED_BOXES:
        unopened_total = len(BOX_IMAGES) - len(_OPENED_BOXES)
        return jsonify({
            "ok": False,
            "already_opened": True,
            "message": "Эта коробка уже пустая — подарок забрали 🎁",
            "unopened_total": unopened_total,
            "opened_count": session["opened_count"],
        })

    if session["opened_count"] >= 3:
        unopened_total = len(BOX_IMAGES) - len(_OPENED_BOXES)
        return jsonify({
            "ok": False,
            "limit": True,
            "message": "Можно открыть только 3 подарка. Лимит исчерпан!",
            "unopened_total": unopened_total,
            "opened_count": session["opened_count"],
        })

    _OPENED_BOXES.add(box_id)
    session["opened_count"] = session["opened_count"] + 1

    unopened_total = len(BOX_IMAGES) - len(_OPENED_BOXES)

    return jsonify({
        "ok": True,
        "congrats": CONGRATS[box_id],
        "gift_img": GIFTS[box_id],
        "unopened_total": unopened_total,
        "opened_count": session["opened_count"],
        "box_id": box_id,
    })
