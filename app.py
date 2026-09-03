import os
from functools import wraps
from itertools import combinations

from flask import Flask, render_template, jsonify, request, session
from supabase import create_client
from dotenv import load_dotenv
load_dotenv()


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
    ],

    "Women's Pool": [
        "Team Rushh",
        "Disciples",
        "Femme Force",
        "Velocity (A)"
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

        "winner": None,

        # NEW
        "walkover": False 
    }
# =========================================================
# CREATE COMPLETE TOURNAMENT FIXTURES
# =========================================================

def create_matches():

    tournament_matches = []

    match_id = 1


    # =====================================================
    # 29 AUGUST 2026 - EVENING SESSION
    # =====================================================

    scheduled_fixtures = [

        (
            "Pool 2",
            "Apex",
            "Zenith",
            "29 August 2026",
            "4:00 – 4:45 PM",
            "Evening Session"
        ),

        (
            "Pool 1",
            "Tribal Boys",
            "Ezzey Volleyball",
            "29 August 2026",
            "4:50 – 5:30 PM",
            "Evening Session"
        ),


        # =================================================
        # 30 AUGUST 2026 - MORNING SESSION
        # =================================================

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
        # 30 AUGUST 2026 - EVENING SESSION
        # =================================================

        (
            "Pool 1",
            "Mahua Boyz",
            "Tribal Boys",
            "30 August 2026",
            None,
            "Evening Session"
        ),

        (
            "Pool 1",
            "Dominators",
            "Mahua Boyz",
            "30 August 2026",
            None,
            "Evening Session"
        ),

        (
            "Pool 1",
            "Mahua Boyz",
            "Ezzey Volleyball",
            "30 August 2026",
            None,
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
        ),

# =================================================
# 31 AUGUST 2026 - MORNING SESSION
# =================================================

(
    "Women's Pool",
    "Team Rushh",
    "Disciples",
    "31 August 2026",
    "5:00 – 5:45 AM",
    "Morning Session"
),

(
    "Pool 3",
    "The Disciples",
    "PhD.",
    "31 August 2026",
    "5:50 – 6:30 AM",
    "Morning Session"
),

(
    "Pool 3",
    "The Disciples",
    "Null Scapes",
    "31 August 2026",
    "6:40 – 7:20 AM",
    "Morning Session"
),


# =================================================
# 31 AUGUST 2026 - EVENING SESSION
# =================================================

(
    "Pool 1",
    "Tribal Boys",
    "Predators",
    "31 August 2026",
    "4:30 – 5:30 PM",
    "Evening Session"
),
        # =================================================
        # 1 SEPTEMBER 2026 - MORNING SESSION
        # =================================================

        (
            "Women's Pool",
            "Disciples",
            "Femme Force",
            "1 September 2026",
            "5:00 – 5:45 AM",
            "Morning Session"
        ),

        (
            "Women's Pool",
            "Team Rushh",
            "Velocity (A)",
            "1 September 2026",
            "5:50 – 6:30 AM",
            "Morning Session"
        ),

        (
            "Pool 3",
            "The Disciples",
            "Spike Force",
            "1 September 2026",
            "6:40 – 7:20 AM",
            "Morning Session"
        ),

        # =================================================
        # 1 SEPTEMBER 2026 - EVENING SESSION
        # =================================================

        (
            "Pool 1",
            "Tribal Boys",
            "Dominators",
            "1 September 2026",
            "4:30 – 5:30 PM",
            "Evening Session"
        ),


        # =================================================
        # 2 SEPTEMBER 2026 - MORNING SESSION
        # =================================================

        (
            "Women's Pool",
            "Femme Force",
            "Velocity (A)",
            "2 September 2026",
            "5:00 – 5:45 AM",
            "Morning Session"
        ),

        (
            "Pool 3",
            "PhD.",
            "Spike Force",
            "2 September 2026",
            "5:50 – 6:30 AM",
            "Morning Session"
        ),

        (
            "Pool 1",
            "Predators",
            "Ezzey Volleyball",
            "2 September 2026",
            "6:40 – 7:20 AM",
            "Morning Session"
        ),


        # =================================================
        # 2 SEPTEMBER 2026 - EVENING SESSION
        # =================================================

        (
            "Pool 3",
            "PhD.",
            "Null Scapes",
            "2 September 2026",
            "4:30 – 5:30 PM",
            "Evening Session"
        ),


        # =================================================
        # 3 SEPTEMBER 2026 - MORNING SESSION
        # =================================================

        (
            "Pool 1",
            "Ezzey Volleyball",
            "Dominators",
            "3 September 2026",
            "5:00 – 5:45 AM",
            "Morning Session"
        ),

        (
            "Women's Pool",
            "Team Rushh",
            "Femme Force",
            "3 September 2026",
            "5:50 – 6:30 AM",
            "Morning Session"
        ),


        # =================================================
        # 4 SEPTEMBER 2026 - MORNING SESSION
        # =================================================

        (
            "Women's Pool",
            "Disciples",
            "Velocity (A)",
            "4 September 2026",
            "6:00 – 7:30 AM",
            "Morning Session"
        )

    ]


    # =====================================================
    # ADD ALL SCHEDULED FIXTURES
    # =====================================================

    scheduled_pairs = {
        "Pool 1": set(),
        "Pool 2": set(),
        "Pool 3": set(),
        "Women's Pool": set()
    }


    for (
        stage,
        team_a,
        team_b,
        match_date,
        match_time,
        session_name
    ) in scheduled_fixtures:

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

        scheduled_pairs[stage].add(
            tuple(sorted([team_a, team_b]))
        )

        match_id += 1
    # =====================================================
    # ADD REMAINING POOL MATCHES
    # =====================================================

    for pool_name, teams in pools.items():

        for team_a, team_b in combinations(
            teams,
            2
        ):

            pair = tuple(
                sorted([team_a, team_b])
            )

            if pair not in scheduled_pairs[pool_name]:

                tournament_matches.append(

                    create_match(
                        match_id,
                        pool_name,
                        team_a,
                        team_b,
                        match_time=None,
                        session_name="Later Fixtures"
                    )
                )

                match_id += 1

    # =====================================================
    # MEN'S SEMI FINAL 1
    # =====================================================

    tournament_matches.append(

        create_match(
            match_id,
            "Semi Final",
            "Pool 1 #2",
            "Pool 3 #1",
            status="locked",
            label="SF1",

            match_date="3 September 2026",

            match_time="6:40 – 7:20 AM",

            session_name="Morning Session"
        )
    )

    match_id += 1


    # =====================================================
    # MEN'S SEMI FINAL 2
    # =====================================================

    tournament_matches.append(

        create_match(
            match_id,
            "Semi Final",
            "Pool 2 #1",
            "Pool 1 #1",
            status="locked",
            label="SF2",

            match_date="3 September 2026",

            match_time="4:30 – 5:30 PM",

            session_name="Evening Session"
        )
    )

    match_id += 1


    # =====================================================
    # MEN'S FINAL
    # =====================================================

    tournament_matches.append(

        create_match(
            match_id,
            "Final",
            "Winner SF1",
            "Winner SF2",
            status="locked",
            label="FINAL",

            match_date="4 September 2026",

            match_time="5:30 – 6:45 AM",

            session_name="Morning Session"
        )
    )

    match_id += 1


    # =====================================================
    # WOMEN'S FINAL
    # =====================================================

    tournament_matches.append(

        create_match(
            match_id,
            "Women's Final",
            "Women's Pool #1",
            "Women's Pool #2",
            status="locked",
            label="WOMENS_FINAL",

            match_date="4 September 2026",

            match_time="4:30 – 5:15 PM",

            session_name="Evening Session"
        )
    )

    match_id += 1


    return tournament_matches
# =========================================================
# APPLY KNOCKOUT SCHEDULE
# =========================================================

def apply_knockout_schedule(match_list):

    schedule = {

        "SF1": {
            "date": "3 September 2026",
            "time": "6:40 – 7:20 AM",
            "session": "Morning Session"
        },

        "SF2": {
            "date": "3 September 2026",
            "time": "4:30 – 5:30 PM",
            "session": "Evening Session"
        },

        "FINAL": {
            "date": "4 September 2026",
            "time": "5:30 – 6:45 AM",
            "session": "Morning Session"
        },

        "WOMENS_FINAL": {
            "date": "4 September 2026",
            "time": "4:45 – 5:15 PM",
            "session": "Evening Session"
        }
    }


    for match in match_list:

        label = match.get("label")

        if label in schedule:

            match["date"] = schedule[label]["date"]

            match["time"] = schedule[label]["time"]

            match["session"] = schedule[label]["session"]
     
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




# =========================================================
# MATCH IDENTITY HELPER
# =========================================================

def get_match_key(match):

    return (
        match.get("stage"),
        tuple(
            sorted([
                match.get("teamA"),
                match.get("teamB")
            ])
        )
    )

# =========================================================
# APPLY MAHUA BOYZ WALKOVERS
# =========================================================

def apply_mahua_walkovers(match_list):

    walkover_results = [

        {
            "teamA": "Mahua Boyz",
            "teamB": "Tribal Boys",
            "winner": "Tribal Boys"
        },

        {
            "teamA": "Dominators",
            "teamB": "Mahua Boyz",
            "winner": "Dominators"
        },

        {
            "teamA": "Mahua Boyz",
            "teamB": "Ezzey Volleyball",
            "winner": "Ezzey Volleyball"
        }
    ]


    for walkover in walkover_results:

        for match in match_list:

            teams_match = (
                match.get("teamA") == walkover["teamA"]
                and
                match.get("teamB") == walkover["teamB"]
            )

            if teams_match:

                match["status"] = "finished"

                match["winner"] = walkover["winner"]

                match["walkover"] = True

                match["scoreA"] = 0
                match["scoreB"] = 0

                match["setHistory"] = []


                if walkover["winner"] == match["teamA"]:

                    match["setsA"] = 2
                    match["setsB"] = 0

                else:

                    match["setsA"] = 0
                    match["setsB"] = 2


                break


# =========================================================
# CHECK WHETHER OLD TOURNAMENT DATA NEEDS MIGRATION
# =========================================================

needs_migration = False


if not saved_state:

    needs_migration = True

else:

    saved_pools = saved_state.get(
        "pools",
        {}
    )

    # If Women's Pool is missing,
    # the old Supabase tournament structure is still active.

    if "Women's Pool" not in saved_pools:

        needs_migration = True


# =========================================================
# MIGRATE OLD TOURNAMENT DATA SAFELY
# =========================================================

if needs_migration:

    print(
        "Migrating tournament to latest fixture structure..."
    )


    # Keep the latest pools from app.py
    # including Women's Pool.

    new_matches = create_matches()


    old_matches = []

    if saved_state:

        old_matches = saved_state.get(
            "matches",
            []
        )


    # Store old matches using team/stage identity.

    old_match_map = {

        get_match_key(match): match

        for match in old_matches

    }


    merged_matches = []


    for new_match in new_matches:

        key = get_match_key(new_match)

        old_match = old_match_map.get(key)


        # Preserve matches that were already played
        # or are currently live.

        if (

            old_match

            and old_match.get("status")
            in [
                "completed",
                "finished",
                "live"
            ]

        ):

            # Preserve the old match result,
            # but update fixture information.

            old_match["stage"] = new_match["stage"]

            old_match["date"] = new_match.get(
                "date"
            )

            old_match["time"] = new_match.get(
                "time"
            )

            old_match["session"] = new_match.get(
                "session"
            )

            old_match["label"] = new_match.get(
                "label"
            )

            merged_matches.append(
                old_match
            )

        else:

            merged_matches.append(
                new_match
            )


    matches = merged_matches


    # Apply the three confirmed Mahua Boyz walkovers.

    apply_mahua_walkovers(
        matches
    )


    # Save the new tournament permanently.

    save_tournament_state()


    print(
        "Tournament migration completed successfully."
    )


# =========================================================
# NORMAL STARTUP
# =========================================================

else:

    pools = saved_state.get(
        "pools",
        pools
    )


    matches = saved_state.get(
        "matches",
        []
    )


    scoring_format = saved_state.get(
        "scoring_format",
        scoring_format
    )

    # =========================================================
    # ALWAYS APPLY CONFIRMED TOURNAMENT UPDATES
    # =========================================================
    apply_mahua_walkovers(matches)

    apply_knockout_schedule(matches)


    # =================================================
    # RESCHEDULED MATCHES - 31 AUGUST 2026
    # =================================================

    for match in matches:
# Tribal Boys vs Predators → Rescheduled to Evening

        if (
            match.get("teamA") == "Tribal Boys"
            and match.get("teamB") == "Predators"
            and match.get("date") == "31 August 2026"
        ):

            match["time"] = "4:30 – 5:30 PM"
            match["session"] = "Evening Session"

            # Show as rescheduled
            match["rescheduled"] = True

          

        # The Disciples vs Null Scapes → Morning
        elif (
            match.get("teamA") == "The Disciples"
            and match.get("teamB") == "Null Scapes"
            and match.get("date") == "31 August 2026"
        ):

            match["time"] = "6:40 – 7:20 AM"
            match["session"] = "Morning Session"
            match["rescheduled"] = True


   
    


    save_tournament_state()

    print(
        "Tournament updates applied successfully."
    )

    print(
        "Tournament loaded normally from Supabase."
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
# TOURNAMENT QUALIFICATION
# =========================================================

def get_pool_standings(pool_name):

    teams = pools.get(pool_name, [])

    standings = {
        team: {
            "team": team,
            "played": 0,
            "wins": 0,
            "losses": 0,
            "sets_won": 0,
            "sets_lost": 0
        }
        for team in teams
    }

    pool_matches = [
        match
        for match in matches
        if match.get("stage") == pool_name
    ]

    for match in pool_matches:

        if match.get("status") != "finished":
            continue

        team_a = match["teamA"]
        team_b = match["teamB"]

        if (
            team_a not in standings
            or team_b not in standings
        ):
            continue

        standings[team_a]["played"] += 1
        standings[team_b]["played"] += 1

        standings[team_a]["sets_won"] += match.get(
            "setsA",
            0
        )

        standings[team_a]["sets_lost"] += match.get(
            "setsB",
            0
        )

        standings[team_b]["sets_won"] += match.get(
            "setsB",
            0
        )

        standings[team_b]["sets_lost"] += match.get(
            "setsA",
            0
        )

        winner = match.get("winner")

        if winner == team_a:

            standings[team_a]["wins"] += 1
            standings[team_b]["losses"] += 1

        elif winner == team_b:

            standings[team_b]["wins"] += 1
            standings[team_a]["losses"] += 1


    ranking = list(
        standings.values()
    )

    ranking.sort(
        key=lambda team: (
            team["wins"],
            team["sets_won"] - team["sets_lost"],
            team["sets_won"]
        ),
        reverse=True
    )

    return ranking


def is_pool_complete(pool_name):

    pool_matches = [
        match
        for match in matches
        if match.get("stage") == pool_name
    ]

    if not pool_matches:
        return False

    return all(
        match.get("status") == "finished"
        for match in pool_matches
    )


def find_match_by_label(label):

    return next(
        (
            match
            for match in matches
            if match.get("label") == label
        ),
        None
    )

def update_pool_qualification():

    # =====================================================
    # GET KNOCKOUT MATCHES
    # =====================================================

    sf1 = find_match_by_label("SF1")
    sf2 = find_match_by_label("SF2")


    # =====================================================
    # POOL 1 QUALIFICATION
    #
    # Pool 1 #2 → SF1 Team A
    # Pool 1 #1 → SF2 Team B
    # =====================================================

    if is_pool_complete("Pool 1"):

        pool1 = get_pool_standings("Pool 1")

        if len(pool1) >= 2:

            if sf1:
                sf1["teamA"] = pool1[1]["team"]

            if sf2:
                sf2["teamB"] = pool1[0]["team"]


    # =====================================================
    # POOL 2 QUALIFICATION
    #
    # Pool 2 #1 → SF2 Team A
    # =====================================================

    if is_pool_complete("Pool 2"):

        pool2 = get_pool_standings("Pool 2")

        if len(pool2) >= 1 and sf2:

            sf2["teamA"] = pool2[0]["team"]


    # =====================================================
    # POOL 3 QUALIFICATION
    #
    # Pool 3 #1 → SF1 Team B
    # =====================================================

    if is_pool_complete("Pool 3"):

        pool3 = get_pool_standings("Pool 3")

        if len(pool3) >= 1 and sf1:

            sf1["teamB"] = pool3[0]["team"]


    # =====================================================
    # UNLOCK SF1 ONLY WHEN BOTH REQUIRED POOLS COMPLETE
    # =====================================================

    if (
        sf1
        and is_pool_complete("Pool 1")
        and is_pool_complete("Pool 3")
    ):

        sf1["status"] = "upcoming"


    # =====================================================
    # UNLOCK SF2 ONLY WHEN BOTH REQUIRED POOLS COMPLETE
    # =====================================================

    if (
        sf2
        and is_pool_complete("Pool 1")
        and is_pool_complete("Pool 2")
    ):

        sf2["status"] = "upcoming"


    # =====================================================
    # MEN'S FINAL QUALIFICATION
    # =====================================================

    sf1 = find_match_by_label("SF1")
    sf2 = find_match_by_label("SF2")
    final = find_match_by_label("FINAL")


    if (
        sf1
        and sf2
        and final
        and sf1.get("status") == "finished"
        and sf2.get("status") == "finished"
        and sf1.get("winner")
        and sf2.get("winner")
    ):

        # Winner of SF1 always appears first
        final["teamA"] = sf1["winner"]

        # Winner of SF2 always appears second
        final["teamB"] = sf2["winner"]

        final["status"] = "upcoming"    


    # =====================================================
    # WOMEN'S FINAL QUALIFICATION
    # =====================================================

    if is_pool_complete("Women's Pool"):

        womens_pool = get_pool_standings(
            "Women's Pool"
        )

        womens_final = find_match_by_label(
            "WOMENS_FINAL"
        )

        if (
            womens_final
            and len(womens_pool) >= 2
        ):

            womens_final["teamA"] = (
                womens_pool[0]["team"]
            )

            womens_final["teamB"] = (
                womens_pool[1]["team"]
            )

            womens_final["status"] = "upcoming"
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

                # Update semifinal / women's final
            # qualification after a pool match finishes.
            update_pool_qualification()    

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
# RESTART CURRENT SET
# =========================================================

@app.route(
    "/api/restart-set/<int:match_id>",
    methods=["POST"]
)
@admin_required
def restart_set(match_id):

    match = find_match(match_id)

    if not match:
        return jsonify({
            "error": "Match not found"
        }), 404

    if match["status"] != "live":
        return jsonify({
            "error": "Only a live match can restart its current set"
        }), 400

    # Reset only the current set.
    # Previous completed sets remain unchanged.
    match["scoreA"] = 0
    match["scoreB"] = 0

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

    # Create fresh tournament fixtures
    matches = create_matches()

    # Apply permanent walkover results
    apply_mahua_walkovers(matches)

    # Apply semifinal and final schedule
    apply_knockout_schedule(matches)

    # Save everything to Supabase
    result = save_tournament_state()


    update_pool_qualification()
    save_tournament_state()
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

    data = request.get_json() or{}

    new_format = data.get("scoring_format")

    if new_format not in [
        "25-25-15",
        "15-15-25"
    ]:
        return jsonify({
            "error": "Invalid scoring format."
        }), 400


    scoring_format = new_format

    save_tournament_state()

    return jsonify({
        "success": True,
        "scoring_format": scoring_format
    })
# =========================================================
# APPLY EXISTING TOURNAMENT QUALIFICATION
# =========================================================

update_pool_qualification()
save_tournament_state()


# =========================================================
# RUN APPLICATION
# =========================================================

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=5000,
        debug=False
    )