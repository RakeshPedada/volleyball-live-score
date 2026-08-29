import os
from functools import wraps
from itertools import combinations

from flask import Flask, render_template, jsonify, request, session
from supabase import create_client


# =========================================================
# SUPABASE CONFIGURATION
# =========================================================

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_SECRET_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError(
        "SUPABASE_URL or SUPABASE_SECRET_KEY environment variable is missing."
    )

supabase = create_client(
    SUPABASE_URL,
    SUPABASE_KEY
)


# =========================================================
# FLASK APPLICATION
# =========================================================

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
    label=None,
    match_time=None,
    session_name=None
):

    return {
        "id": match_id,
        "stage": stage,
        "label": label,

        "teamA": team_a,
        "teamB": team_b,

        "status": status,

        "time": match_time,
        "session": session_name,

        "scoreA": 0,
        "scoreB": 0,

        "setsA": 0,
        "setsB": 0,

        "setHistory": [],

        "winner": None
    }


# =========================================================
# CREATE COMPLETE TOURNAMENT FIXTURES
# =========================================================

def create_matches():

    tournament_matches = []

    match_id = 1


    # =====================================================
    # DAY 1 - MORNING SESSION
    # =====================================================

    day_one_fixtures = [

        (
            "Pool 2",
            "Zenith",
            "Net Warriors",
            "5:00 – 5:45 AM",
            "Morning Session"
        ),

        (
            "Pool 3",
            "Spike Force",
            "Null Scapes",
            "5:50 – 6:30 AM",
            "Morning Session"
        ),

        (
            "Pool 2",
            "Zenith",
            "Avengers",
            "6:40 – 7:15 AM",
            "Morning Session"
        ),

        (
            "Pool 1",
            "Mahua Boyz",
            "Predators",
            "7:20 – 8:00 AM",
            "Morning Session"
        ),

        (
            "Pool 2",
            "Avengers",
            "Apex",
            "8:05 – 8:45 AM",
            "Morning Session"
        ),

        (
            "Pool 1",
            "Dominators",
            "Predators",
            "8:50 – 9:30 AM",
            "Morning Session"
        ),


        # =================================================
        # DAY 1 - EVENING SESSION
        # =================================================

        (
            "Pool 1",
            "Dominators",
            "Mahua Boyz",
            "3:00 – 3:45 PM",
            "Evening Session"
        ),

        (
            "Pool 2",
            "Apex",
            "Net Warriors",
            "3:50 – 4:30 PM",
            "Evening Session"
        ),

        (
            "Pool 2",
            "Avengers",
            "Net Warriors",
            "4:40 – 5:40 PM",
            "Evening Session"
        )
    ]


    # Add Day 1 fixtures first

    scheduled_pairs = set()

    for (
        stage,
        team_a,
        team_b,
        match_time,
        session_name
    ) in day_one_fixtures:

        tournament_matches.append(

            create_match(
                match_id,
                stage,
                team_a,
                team_b,
                match_time=match_time,
                session_name=session_name
            )
        )

        scheduled_pairs.add(
            tuple(sorted([team_a, team_b]))
        )

        match_id += 1


    # =====================================================
    # ADD REMAINING POOL 1 MATCHES
    # =====================================================

    for team_a, team_b in combinations(
        pools["Pool 1"],
        2
    ):

        pair = tuple(
            sorted([team_a, team_b])
        )

        if pair not in scheduled_pairs:

            tournament_matches.append(

                create_match(
                    match_id,
                    "Pool 1",
                    team_a,
                    team_b,
                    match_time=None,
                    session_name="Later Fixtures"
                )
            )

            match_id += 1


    # =====================================================
    # ADD REMAINING POOL 2 MATCHES
    # =====================================================

    for team_a, team_b in combinations(
        pools["Pool 2"],
        2
    ):

        pair = tuple(
            sorted([team_a, team_b])
        )

        if pair not in scheduled_pairs:

            tournament_matches.append(

                create_match(
                    match_id,
                    "Pool 2",
                    team_a,
                    team_b,
                    match_time=None,
                    session_name="Later Fixtures"
                )
            )

            match_id += 1


    # =====================================================
    # ADD REMAINING POOL 3 MATCHES
    # =====================================================

    for team_a, team_b in combinations(
        pools["Pool 3"],
        2
    ):

        pair = tuple(
            sorted([team_a, team_b])
        )

        if pair not in scheduled_pairs:

            tournament_matches.append(

                create_match(
                    match_id,
                    "Pool 3",
                    team_a,
                    team_b,
                    match_time=None,
                    session_name="Later Fixtures"
                )
            )

            match_id += 1


    # =====================================================
    # SEMI FINALS
    # =====================================================

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


    # =====================================================
    # FINAL
    # =====================================================

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


# =========================================================
# SUPABASE SAVE
# =========================================================

def save_tournament_state():

    tournament_state = {
        "pools": pools,
        "matches": matches
    }

    # upsert guarantees that row id=1 is created or replaced
    # with the latest tournament state.
    result = supabase.table(
        "tournament_state"
    ).upsert({
        "id": 1,
        "data": tournament_state
    }, on_conflict="id").execute()

    return result


# =========================================================
# SUPABASE LOAD
# =========================================================

def load_tournament_state():

    result = supabase.table(
        "tournament_state"
    ).select(
        "data"
    ).eq(
        "id",
        1
    ).execute()

    if not result.data:
        return None

    data = result.data[0].get("data")

    if not data:
        return None

    if "matches" not in data:
        return None

    return data


# =========================================================
# LOAD TOURNAMENT ON SERVER START
# =========================================================

saved_state = load_tournament_state()

if saved_state:

    pools = saved_state.get(
        "pools",
        pools
    )

    matches = saved_state.get(
        "matches",
        create_matches()
    )

    print("Tournament loaded from Supabase.")

else:

    matches = create_matches()

    save_tournament_state()

    print("New tournament created and saved to Supabase.")


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

    return len(match["setHistory"]) + 1


def get_target_score(match):

    current_set = get_current_set_number(match)

    # Third / deciding set
    if current_set == 3:
        return 15

    # Set 1 and Set 2
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

    # Award set

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

@app.route(
    "/api/admin/login",
    methods=["POST"]
)
def admin_login():

    data = request.get_json()

    if not data:

        return jsonify({
            "error": "Invalid request"
        }), 400

    username = data.get(
        "username",
        ""
    )

    password = data.get(
        "password",
        ""
    )

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

@app.route(
    "/api/admin/logout",
    methods=["POST"]
)
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
        "is_admin": session.get(
            "is_admin",
            False
        )
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

@app.route(
    "/api/start/<int:match_id>",
    methods=["POST"]
)
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


    # Only one match can be live

    for other_match in matches:

        if (
            other_match["status"] == "live"
            and other_match["id"] != match_id
        ):

            other_match["status"] = "upcoming"


    match["status"] = "live"

    save_tournament_state()

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


    # Add point

    if side == "A":

        match["scoreA"] += 1

    elif side == "B":

        match["scoreB"] += 1

    else:

        return jsonify({
            "error": "Invalid side"
        }), 400


    # Check whether set has finished

    if check_set_finished(match):

        finish_current_set(match)


        # First team to win 2 sets wins match

        if (
            match["setsA"] == 2
            or match["setsB"] == 2
        ):

            finish_match(match)

        else:

            # Automatically start next set

            start_next_set(match)


    save_tournament_state()

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


    save_tournament_state()

    return jsonify(match)


# =========================================================
# RESET TOURNAMENT
# =========================================================

@app.route(
    "/api/reset",
    methods=["POST"]
)
@admin_required
def reset_tournament():

    global matches

    # Recreate the COMPLETE tournament:
    # 22 pool matches + 2 semi-finals + 1 final

    matches = create_matches()

    result = save_tournament_state()

    print("====================================")
    print("TOURNAMENT RESET COMPLETED")
    print("Total matches:", len(matches))
    print("Supabase result:", result.data)
    print("====================================")

    return jsonify({
        "success": True,
        "message": "Tournament reset successfully",
        "matches_count": len(matches)
    })


# =========================================================
# RUN APPLICATION
# =========================================================
@app.route(
    "/api/force-reset-fixtures",
    methods=["GET", "POST"]
)
def force_reset_fixtures():
    """Replace the persisted Supabase fixtures with the current code fixtures."""
    global matches

    matches = create_matches()
    result = save_tournament_state()

    print("FIXTURES REPLACED IN SUPABASE")
    print("Total matches:", len(matches))

    return jsonify({
        "success": True,
        "message": "Supabase fixtures replaced successfully",
        "total_matches": len(matches),
        "matches": matches,
        "supabase_saved": bool(result.data is not None)
    })

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )
