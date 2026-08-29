import os
from functools import wraps

from flask import Flask, jsonify, render_template, request, session


app = Flask(__name__)

# =========================================================
# SECURITY CONFIGURATION
# =========================================================

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
# ADMIN AUTHENTICATION
# =========================================================

def admin_required(function):

    @wraps(function)
    def decorated_function(*args, **kwargs):

        if not session.get("is_admin"):
            return jsonify({
                "error": "Admin authentication required"
            }), 401

        return function(*args, **kwargs)

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
# MATCH CREATION
# =========================================================

def create_match(
    match_id,
    stage,
    team_a,
    team_b,
    status="upcoming",
    label=None
):

    return {
        "id": match_id,
        "stage": stage,
        "label": label,

        "teamA": team_a,
        "teamB": team_b,

        "status": status,

        "scoreA": 0,
        "scoreB": 0,

        "setsA": 0,
        "setsB": 0,

        "setHistory": [],

        "winner": None
    }


def create_matches():

    tournament_matches = []

    match_id = 1

    # -----------------------------------------------------
    # POOL MATCHES
    # -----------------------------------------------------

    for pool_name, teams in pools.items():

        for i in range(len(teams)):

            for j in range(i + 1, len(teams)):

                tournament_matches.append(
                    create_match(
                        match_id,
                        pool_name,
                        teams[i],
                        teams[j]
                    )
                )

                match_id += 1


    # -----------------------------------------------------
    # SEMI FINAL 1
    # -----------------------------------------------------

    tournament_matches.append(
        create_match(
            23,
            "Semi Final",
            "Pool 1 #1",
            "Pool 3 #1",
            status="locked",
            label="SF1"
        )
    )


    # -----------------------------------------------------
    # SEMI FINAL 2
    # -----------------------------------------------------

    tournament_matches.append(
        create_match(
            24,
            "Semi Final",
            "Pool 2 #1",
            "Pool 1 #2",
            status="locked",
            label="SF2"
        )
    )


    # -----------------------------------------------------
    # FINAL
    # -----------------------------------------------------

    tournament_matches.append(
        create_match(
            25,
            "Final",
            "Winner SF1",
            "Winner SF2",
            status="locked",
            label="FINAL"
        )
    )

    return tournament_matches


matches = create_matches()


# =========================================================
# HELPER FUNCTIONS
# =========================================================

def find_match(match_id):

    return next(
        (
            match
            for match in matches
            if match["id"] == match_id
        ),
        None
    )


def get_current_set_number(match):

    # Number of completed sets + current set
    return len(match["setHistory"]) + 1


def get_target_score(match):

    current_set = get_current_set_number(match)

    # Set 1 and Set 2 -> 25
    # Set 3 -> 15
    if current_set == 3:
        return 15

    return 25


def check_set_finished(match):

    target = get_target_score(match)

    score_a = match["scoreA"]
    score_b = match["scoreB"]

    highest_score = max(score_a, score_b)

    score_difference = abs(score_a - score_b)

    return (
        highest_score >= target
        and score_difference >= 2
    )


def finish_current_set(match):

    score_a = match["scoreA"]
    score_b = match["scoreB"]

    # Save completed set
    match["setHistory"].append({
        "a": score_a,
        "b": score_b
    })

    # Award the set
    if score_a > score_b:
        match["setsA"] += 1
    else:
        match["setsB"] += 1


def finish_match(match):

    match["status"] = "finished"

    if match["setsA"] > match["setsB"]:
        match["winner"] = match["teamA"]
    else:
        match["winner"] = match["teamB"]


def start_next_set(match):

    match["scoreA"] = 0
    match["scoreB"] = 0


# =========================================================
# HOME
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


    if (
        username == ADMIN_USERNAME
        and password == ADMIN_PASSWORD
    ):

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
# ADMIN STATUS
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
# =========================================================

@app.route("/api/start/<int:match_id>", methods=["POST"])
@admin_required
def start_match(match_id):

    match = find_match(match_id)

    if not match:
        return jsonify({
            "error": "Match not found"
        }), 404


    if match["status"] == "locked":

        return jsonify({
            "error": "Match is locked"
        }), 400


    if match["status"] == "finished":

        return jsonify({
            "error": "This match has already finished"
        }), 400


    # Only one match can be live at a time
    for other_match in matches:

        if (
            other_match["status"] == "live"
            and other_match["id"] != match_id
        ):
            other_match["status"] = "upcoming"


    match["status"] = "live"

    return jsonify(match)


# =========================================================
# ADD POINT
# =========================================================

@app.route(
    "/api/point/<int:match_id>/<side>",
    methods=["POST"]
)
@admin_required
def add_point(match_id, side):

    match = find_match(match_id)

    if not match:

        return jsonify({
            "error": "Match not found"
        }), 404


    if match["status"] != "live":

        return jsonify({
            "error": "Match is not live"
        }), 400


    # -----------------------------------------------------
    # ADD POINT
    # -----------------------------------------------------

    if side == "A":

        match["scoreA"] += 1

    elif side == "B":

        match["scoreB"] += 1

    else:

        return jsonify({
            "error": "Invalid side"
        }), 400


    # -----------------------------------------------------
    # CHECK WHETHER CURRENT SET HAS FINISHED
    # -----------------------------------------------------

    if check_set_finished(match):

        finish_current_set(match)


        # -------------------------------------------------
        # MATCH FINISHED
        # First team to win 2 sets wins.
        # Maximum possible sets = 3.
        # -------------------------------------------------

        if (
            match["setsA"] == 2
            or match["setsB"] == 2
        ):

            finish_match(match)


        else:

            # ---------------------------------------------
            # AUTOMATICALLY START NEXT SET
            # ---------------------------------------------

            start_next_set(match)


    return jsonify(match)


# =========================================================
# UNDO POINT
# =========================================================

@app.route(
    "/api/undo/<int:match_id>/<side>",
    methods=["POST"]
)
@admin_required
def undo_point(match_id, side):

    match = find_match(match_id)

    if not match:

        return jsonify({
            "error": "Match not found"
        }), 404


    if match["status"] != "live":

        return jsonify({
            "error": "Match is not live"
        }), 400


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
# =========================================================

@app.route("/api/reset", methods=["POST"])
@admin_required
def reset_tournament():

    global matches

    matches = create_matches()

    return jsonify({
        "success": True,
        "message": "Tournament reset successfully"
    })


# =========================================================
# RUN APPLICATION
# =========================================================

if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )