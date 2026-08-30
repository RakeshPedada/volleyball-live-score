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
    session_name=None,
    match_date=None
):

    return {
        "id": match_id,
        "stage": stage,
        "label": label,

        "teamA": team_a,
        "teamB": team_b,

        "status": status,

        "date": match_date,
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

        # stage, team A, team B, date, time, session
        (
            "Pool 2",
            "Zenith",
            "Net Warriors",
            "30 August 2026",
            "5:00 – 5:45 AM",
            "Morning Session"
        ),

        (
            "Pool 3",
            "Spike Force",
            "Null Scapes",
            "30 August 2026",
            "5:50 – 6:30 AM",
            "Morning Session"
        ),

        (
            "Pool 2",
            "Zenith",
            "Avengers",
            "30 August 2026",
            "6:40 – 7:15 AM",
            "Morning Session"
        ),

        (
            "Pool 1",
            "Mahua Boyz",
            "Predators",
            "30 August 2026",
            "7:20 – 8:00 AM",
            "Morning Session"
        ),

        (
            "Pool 2",
            "Avengers",
            "Apex",
            "30 August 2026",
            "8:05 – 8:45 AM",
            "Morning Session"
        ),

        (
            "Pool 1",
            "Dominators",
            "Predators",
            "30 August 2026",
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
            "30 August 2026",
            "3:00 – 3:45 PM",
            "Evening Session"
        ),

        (
            "Pool 2",
            "Apex",
            "Net Warriors",
            "30 August 2026",
            "3:50 – 4:30 PM",
            "Evening Session"
        ),

        (
            "Pool 2",
            "Avengers",
            "Net Warriors",
            "30 August 2026",
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
        match_date,
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
                session_name=session_name,
                match_date=match_date
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
        "matches": matches,
        "scoring_format": scoring_format
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
# SCORING FORMAT
# =========================================================

scoring_format = "25-25-15"


# =========================================================
# LOAD TOURNAMENT ON SERVER START
# =========================================================



saved_state = load_tournament_state()

if saved_state:

    pools = saved_state.get(
        "pools",
        pools
    )

    scoring_format = saved_state.get(
         "scoring_format",
        scoring_format
    )

    print(
        "Tournament data found in Supabase."
    )

else:

    print(
        "No existing tournament found in Supabase."
    )


# =========================================================
# CREATE AND SAVE CURRENT FIXTURE SCHEDULE
# =========================================================

# The current tournament has not started yet.
# Therefore, create_matches() is the source of truth and
# replaces the old fixture schedule stored in Supabase.

matches = create_matches()

save_tournament_state()


print(
    "Current fixture schedule saved to Supabase."
)





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

    if scoring_format == "15-15-25":

        # Set 1 and Set 2
        if current_set in [1, 2]:
            return 15

        # Deciding Set
        return 25

    # Default: 25-25-15
    if current_set in [1, 2]:
        return 25

    return 15


def check_set_finished(match):

    target = get_target_score(match)

    score_a = match["scoreA"]
    score_b = match["scoreB"]

    highest_score = max(score_a, score_b)

    score_difference = abs(score_a - score_b)


    # =====================================================
    # DIRECT WIN / MERCY RULE
    # =====================================================

    # For a 15-point set:
    # A team wins immediately at 7-0
    if target == 15:

        if (
            highest_score >= 7
            and min(score_a, score_b) == 0
        ):
            return True


    # For a 25-point set:
    # A team wins immediately at 12-0
    if target == 25:

        if (
            highest_score >= 12
            and min(score_a, score_b) == 0
        ):
            return True


    # =====================================================
    # NORMAL VOLLEYBALL SET RULE
    # =====================================================

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
        "matches": matches,
        "scoring_format": scoring_format
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
# SCHEDULE / ADD FUTURE FIXTURES WITHOUT RESETTING SCORES
# =========================================================

@app.route(
    "/api/schedule-fixtures",
    methods=["POST"]
)
@admin_required
def schedule_fixtures():
    """
    Schedule existing upcoming fixtures, or add a new fixture if it does not
    already exist. Finished/live matches are never modified, so past scores
    and set history remain safe.
    """

    global matches

    data = request.get_json(silent=True) or {}
    fixtures = data.get("fixtures")

    if not isinstance(fixtures, list) or not fixtures:
        return jsonify({
            "error": "Provide a non-empty fixtures list"
        }), 400

    updated = []
    added = []

    next_id = max(
        (match["id"] for match in matches),
        default=0
    ) + 1

    for fixture in fixtures:

        if not isinstance(fixture, dict):
            return jsonify({
                "error": "Each fixture must be an object"
            }), 400

        stage = fixture.get("stage")
        team_a = fixture.get("teamA")
        team_b = fixture.get("teamB")
        match_date = fixture.get("date")
        match_time = fixture.get("time")
        session_name = fixture.get("session")

        if not all([
            stage,
            team_a,
            team_b,
            match_date,
            match_time,
            session_name
        ]):
            return jsonify({
                "error": "Each fixture requires stage, teamA, teamB, date, time and session"
            }), 400

        existing = next(
            (
                match for match in matches
                if match["stage"] == stage
                and {match["teamA"], match["teamB"]} == {team_a, team_b}
            ),
            None
        )

        # If the pool fixture already exists, schedule it instead of creating
        # a duplicate. Never overwrite a match that has already started.
        if existing:

            if existing["status"] != "upcoming":
                return jsonify({
                    "error": (
                        f'{team_a} vs {team_b} cannot be rescheduled because '
                        f'its status is {existing["status"]}'
                    )
                }), 400

            existing["date"] = match_date
            existing["time"] = match_time
            existing["session"] = session_name

            updated.append(existing["id"])

        else:

            new_match = create_match(
                next_id,
                stage,
                team_a,
                team_b,
                match_time=match_time,
                session_name=session_name,
                match_date=match_date
            )

            matches.append(new_match)
            added.append(next_id)
            next_id += 1

    save_tournament_state()

    return jsonify({
        "success": True,
        "message": "Fixtures scheduled without resetting tournament scores",
        "updated_match_ids": updated,
        "added_match_ids": added,
        "total_matches": len(matches)
    })


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
# UPDATE SCORING FORMAT
# =========================================================

@app.route(
    "/api/scoring-format",
    methods=["POST"]
)
def update_scoring_format():

    global scoring_format

    data = request.get_json()

    new_format = data.get("format")

    if new_format not in [
        "25-25-15",
        "15-15-25"
    ]:
        return jsonify({
            "error": "Invalid scoring format."
        }), 400

    # Prevent changing format while a match is live
    live_match = next(
        (
            match
            for match in matches
            if match["status"] == "live"
        ),
        None
    )

    if live_match:
        return jsonify({
            "error": "Finish the live match before changing the scoring format."
        }), 400

    scoring_format = new_format

    save_tournament_state()

    return jsonify({
        "success": True,
        "scoring_format": scoring_format
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
