import os
from functools import wraps

from flask import Flask, render_template, jsonify, request, session

app = Flask(__name__)

# =========================================================
# SECURITY CONFIGURATION
# =========================================================

# Change these fallback values for your local testing.
# Environment variables will override these values if configured.

app.secret_key = os.environ.get(
    "SECRET_KEY",
    "change-this-to-a-long-random-secret-key"
)

ADMIN_USERNAME = os.environ.get(
    "ADMIN_USERNAME",
    "Dinesh"
)

ADMIN_PASSWORD = os.environ.get(
    "ADMIN_PASSWORD",
    "7893894890"
)


# =========================================================
# ADMIN AUTHENTICATION DECORATOR
# =========================================================

def admin_required(f):

    @wraps(f)
    def decorated_function(*args, **kwargs):

        if not session.get("is_admin"):

            return jsonify({
                "error": "Admin authentication required"
            }), 401

        return f(*args, **kwargs)

    return decorated_function


# =========================================================
# TOURNAMENT POOLS
# =========================================================

pools = {
    "Pool 1": [
        "Mahua Boyz",
        "Dominators",
        "Predators",
        "Tribal Boys",
        "Ezzey Volleyball"
    ],
    "Pool 2": [
        "Apex",
        "Avengers",
        "Net Warriors",
        "Zenith"
    ],
    "Pool 3": [
        "The Disciples",
        "Null Scapes",
        "Spike Force",
        "PhD."
    ]
}


# =========================================================
# CREATE MATCHES
# =========================================================

def create_matches():

    matches = []
    match_id = 1

    # League Matches
    for pool, teams in pools.items():

        for i in range(len(teams)):

            for j in range(i + 1, len(teams)):

                matches.append({

                    "id": match_id,
                    "stage": pool,

                    "teamA": teams[i],
                    "teamB": teams[j],

                    "status": "upcoming",

                    "scoreA": 0,
                    "scoreB": 0,

                    "setsA": 0,
                    "setsB": 0,

                    "setHistory": [],

                    "winner": None

                })

                match_id += 1


    # =====================================================
    # SEMI FINAL 1
    # Pool 1 #1 vs Pool 3 #1
    # =====================================================

    matches.append({

        "id": 23,

        "stage": "Semi Final",

        "label": "SF1",

        "teamA": "Pool 1 #1",
        "teamB": "Pool 3 #1",

        "status": "locked",

        "scoreA": 0,
        "scoreB": 0,

        "setsA": 0,
        "setsB": 0,

        "setHistory": [],

        "winner": None

    })


    # =====================================================
    # SEMI FINAL 2
    # Pool 2 #1 vs Pool 1 #2
    # =====================================================

    matches.append({

        "id": 24,

        "stage": "Semi Final",

        "label": "SF2",

        "teamA": "Pool 2 #1",
        "teamB": "Pool 1 #2",

        "status": "locked",

        "scoreA": 0,
        "scoreB": 0,

        "setsA": 0,
        "setsB": 0,

        "setHistory": [],

        "winner": None

    })


    # =====================================================
    # FINAL
    # =====================================================

    matches.append({

        "id": 25,

        "stage": "Final",

        "label": "FINAL",

        "teamA": "Winner SF1",
        "teamB": "Winner SF2",

        "status": "locked",

        "scoreA": 0,
        "scoreB": 0,

        "setsA": 0,
        "setsB": 0,

        "setHistory": [],

        "winner": None

    })


    return matches


matches = create_matches()


# =========================================================
# HOME PAGE
# =========================================================

@app.route("/")
def home():

    return render_template("index.html")


# =========================================================
# ADMIN LOGIN
# =========================================================

@app.route("/api/admin/login", methods=["POST"])
def admin_login():

    data = request.get_json()

    if not data:

        return jsonify({
            "error": "Invalid request"
        }), 400


    username = data.get("username", "")
    password = data.get("password", "")


    if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:

        session["is_admin"] = True

        return jsonify({
            "success": True,
            "message": "Admin login successful"
        })


    return jsonify({
        "error": "Invalid username or password"
    }), 401


# =========================================================
# ADMIN LOGOUT
# =========================================================

@app.route("/api/admin/logout", methods=["POST"])
def admin_logout():

    session.clear()

    return jsonify({
        "success": True,
        "message": "Logged out successfully"
    })


# =========================================================
# CHECK ADMIN SESSION
# =========================================================

@app.route("/api/admin/status")
def admin_status():

    return jsonify({
        "is_admin": session.get("is_admin", False)
    })


# =========================================================
# PUBLIC TOURNAMENT DATA
# =========================================================

@app.route("/api/data")
def get_data():

    return jsonify({

        "pools": pools,

        "matches": matches

    })


# =========================================================
# START MATCH
# ADMIN ONLY
# =========================================================

@app.route("/api/start/<int:match_id>", methods=["POST"])
@admin_required
def start_match(match_id):

    global matches


    # Only one match can be live at a time
    for match in matches:

        if match["status"] == "live":

            match["status"] = "upcoming"


    match = next(

        (m for m in matches if m["id"] == match_id),

        None

    )


    if not match:

        return jsonify({
            "error": "Match not found"
        }), 404


    if match["status"] == "locked":

        return jsonify({
            "error": "Match is locked"
        }), 400


    match["status"] = "live"


    return jsonify(match)


# =========================================================
# ADD POINT
# ADMIN ONLY
# =========================================================

@app.route("/api/point/<int:match_id>/<side>", methods=["POST"])
@admin_required
def add_point(match_id, side):

    match = next(

        (m for m in matches if m["id"] == match_id),

        None

    )


    if not match:

        return jsonify({
            "error": "Match not found"
        }), 404


    if match["status"] != "live":

        return jsonify({
            "error": "Match is not live"
        }), 400


    # Add point
    if side == "A":

        match["scoreA"] += 1


    elif side == "B":

        match["scoreB"] += 1


    else:

        return jsonify({
            "error": "Invalid side"
        }), 400


    # Deciding set is played to 15
    target = 15 if (
        match["setsA"] == 1
        and match["setsB"] == 1
    ) else 25


    a = match["scoreA"]
    b = match["scoreB"]


    # =====================================================
    # CHECK IF SET FINISHED
    # =====================================================

    if max(a, b) >= target and abs(a - b) >= 2:


        if a > b:

            match["setsA"] += 1


        else:

            match["setsB"] += 1


        match["setHistory"].append({

            "a": a,

            "b": b

        })


        # =================================================
        # CHECK IF MATCH FINISHED
        # =================================================

        if match["setsA"] == 2 or match["setsB"] == 2:


            match["status"] = "finished"


            if match["setsA"] > match["setsB"]:

                match["winner"] = match["teamA"]


            else:

                match["winner"] = match["teamB"]


        else:

            # Start next set

            match["scoreA"] = 0

            match["scoreB"] = 0


    return jsonify(match)


# =========================================================
# UNDO POINT
# ADMIN ONLY
# =========================================================

@app.route("/api/undo/<int:match_id>/<side>", methods=["POST"])
@admin_required
def undo_point(match_id, side):

    match = next(

        (m for m in matches if m["id"] == match_id),

        None

    )


    if not match:

        return jsonify({
            "error": "Match not found"
        }), 404


    if side == "A":

        match["scoreA"] = max(
            0,
            match["scoreA"] - 1
        )


    elif side == "B":

        match["scoreB"] = max(
            0,
            match["scoreB"] - 1
        )


    else:

        return jsonify({
            "error": "Invalid side"
        }), 400


    return jsonify(match)


# =========================================================
# RESET TOURNAMENT
# ADMIN ONLY
# =========================================================

@app.route("/api/reset", methods=["POST"])
@admin_required
def reset():

    global matches

    matches = create_matches()


    return jsonify({

        "message": "Tournament reset"

    })


# =========================================================
# RUN APP
# =========================================================

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)

