let tournamentData = null;
let selectedMatchId = null;
let isAdmin = false;


function getTargetScore(match) {

    const completedSets =
        match.setHistory.length;

    const format =
        tournamentData.scoring_format
        || "25-25-15";

    if (format === "15-15-25") {

        return completedSets === 2
            ? 25
            : 15;

    }

    return completedSets === 2
        ? 15
        : 25;

}

function getMatchStatusText(match) {

    if (match.walkover === true) {
        return "🚫 WALKOVER";
    }

    if (match.status === "finished" ||
        match.status === "completed") {

        return "FINISHED";
    }

    if (match.status === "live") {
        return "🔴 LIVE";
    }

    if (match.status === "locked") {
        return "🔒 LOCKED";
    }

    return "UPCOMING";
}


/* =========================================================
   LOAD DATA
========================================================= */

async function loadData() {

    try {

        const response = await fetch("/api/data");

        tournamentData = await response.json();

        updateEverything();

    } catch (error) {

        console.error("Could not load tournament data:", error);

    }

}


/* =========================================================
   UPDATE EVERYTHING
========================================================= */

function updateEverything() {

    if (!tournamentData) return;

    updateMatchSelect();
    updateLiveScore();
    updatePools();
    updateFixtures();
    updateStandings();
    updateKnockout();
    updateAdminPanel();
    updateScoringFormatButtons();

}


/* =========================================================
   PAGE NAVIGATION
========================================================= */

function showPage(page, button) {

    document
        .querySelectorAll(".page")
        .forEach(pageElement => {

            pageElement.classList.add("hidden");

        });


    document
        .getElementById(page + "Page")
        .classList.remove("hidden");


    document
        .querySelectorAll(".nav-btn")
        .forEach(navButton => {

            navButton.classList.remove("active");

        });


    button.classList.add("active");

}


/* =========================================================
   ADMIN LOGIN MODAL
========================================================= */

function openAdminLogin() {

    if (isAdmin) {

        document
            .getElementById("adminPanel")
            .classList.toggle("hidden");

        return;

    }


    document
        .getElementById("loginModal")
        .classList.remove("hidden");

}


function closeAdminLogin() {

    document
        .getElementById("loginModal")
        .classList.add("hidden");


    document
        .getElementById("loginError")
        .textContent = "";

}


/* =========================================================
   LOGIN
========================================================= */

async function loginAdmin() {

    const username =
        document.getElementById("adminUsername").value.trim();

    const password =
        document.getElementById("adminPassword").value;


    const response = await fetch(
        "/api/admin/login",
        {
            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                username,
                password
            })
        }
    );


    const result = await response.json();


    if (!response.ok) {

        document
            .getElementById("loginError")
            .textContent =
            result.error || "Login failed";

        return;

    }


    isAdmin = true;

    closeAdminLogin();


    document
        .getElementById("adminPanel")
        .classList.remove("hidden");


    document
        .getElementById("adminButton")
        .textContent = "⚙ ADMIN PANEL";


    document
        .getElementById("adminPassword")
        .value = "";


    await loadData();

}


/* =========================================================
   CHECK ADMIN SESSION
========================================================= */

async function checkAdminStatus() {

    try {

        const response =
            await fetch("/api/admin/status");

        const data =
            await response.json();


        isAdmin = data.is_admin;


        if (isAdmin) {

            document
                .getElementById("adminButton")
                .textContent =
                "⚙ ADMIN PANEL";

        }

    } catch (error) {

        console.error(
            "Could not check admin status:",
            error
        );

    }

}


/* =========================================================
   LOGOUT
========================================================= */

async function logoutAdmin() {

    await fetch(
        "/api/admin/logout",
        {
            method: "POST"
        }
    );


    isAdmin = false;


    document
        .getElementById("adminPanel")
        .classList.add("hidden");


    document
        .getElementById("adminButton")
        .textContent =
        "🔐 ADMIN LOGIN";


    alert("Logged out successfully.");

}


/* =========================================================
   MATCH SELECT
========================================================= */

function updateMatchSelect() {

    const select =
        document.getElementById("matchSelect");


    const availableMatches =
        tournamentData.matches.filter(
            match =>
                match.status !== "locked"
                && match.status !== "finished"
        );


    select.innerHTML = "";


    availableMatches.forEach(match => {

        const option =
            document.createElement("option");


        option.value = match.id;


        option.textContent =
            `Match ${match.id} • ${match.teamA} vs ${match.teamB}`;


        select.appendChild(option);

    });


    if (availableMatches.length === 0) {

        selectedMatchId = null;

        return;

    }


    const selectedStillExists =
        availableMatches.some(
            match =>
                match.id === selectedMatchId
        );


    if (
        selectedMatchId === null
        || !selectedStillExists
    ) {

        const liveMatch =
            availableMatches.find(
                match =>
                    match.status === "live"
            );


        selectedMatchId =
            liveMatch
                ? liveMatch.id
                : availableMatches[0].id;

    }


    select.value = selectedMatchId;


    select.onchange = () => {

        selectedMatchId =
            Number(select.value);

        updateAdminPanel();

    };

}


/* =========================================================
   GET SELECTED MATCH
========================================================= */

function getSelectedMatch() {

    if (!selectedMatchId) return null;


    return tournamentData.matches.find(
        match =>
            match.id === selectedMatchId
    );

}


/* =========================================================
   ADMIN PANEL
========================================================= */

function updateAdminPanel() {

    const match =
        getSelectedMatch();


    if (!match) return;


    document
        .getElementById("adminTeamA")
        .textContent =
        match.teamA;


    document
        .getElementById("adminTeamB")
        .textContent =
        match.teamB;


    document
        .getElementById("adminScoreA")
        .textContent =
        match.scoreA;


    document
        .getElementById("adminScoreB")
        .textContent =
        match.scoreB;


    document
        .getElementById("adminSets")
        .textContent =
        `${match.setsA} - ${match.setsB}`;


    const target =
        getTargetScore(match);


        document
            .getElementById("targetText")
            .textContent =
            `Target: ${target}`;

    }


/* =========================================================
   START MATCH
========================================================= */

async function startSelectedMatch() {

    if (!selectedMatchId) {

        alert("No match available.");

        return;

    }


    const response = await fetch(
        `/api/start/${selectedMatchId}`,
        {
            method: "POST"
        }
    );


    const result =
        await response.json();


    if (!response.ok) {

        alert(
            result.error
            || "Could not start match."
        );

        return;

    }


    await loadData();

}


/* =========================================================
   ADD POINT
========================================================= */
async function addPoint(side) {

    if (!selectedMatchId) {

        alert("Please select a match first.");

        return;

    }

    const response = await fetch(

        `/api/point/${selectedMatchId}/${side}`,

        {
            method: "POST"
        }

    );

    const result = await response.json();


    if (!response.ok) {

        alert(

            result.error
            || "Could not add point."

        );

        return;

    }


    // Reload latest tournament data
    tournamentData = await (

        await fetch("/api/data")

    ).json();


    // Keep the same selected match
    const select = document.getElementById(

        "matchSelect"

    );

    select.value = selectedMatchId;


    // Update admin score immediately
    updateAdminPanel();


    // Update public pages
    updateLiveScore();
    updateFixtures();
    updateStandings();
    updateKnockout();

}

/* =========================================================
   UNDO POINT
========================================================= */
async function undoPoint(side) {

    if (!selectedMatchId) {

        alert("Please select a match first.");

        return;

    }

    const response = await fetch(

        `/api/undo/${selectedMatchId}/${side}`,

        {
            method: "POST"
        }

    );

    const result = await response.json();


    if (!response.ok) {

        alert(

            result.error
            || "Could not undo point."

        );

        return;

    }


    // Reload latest tournament data
    tournamentData = await (

        await fetch("/api/data")

    ).json();


    // Keep same selected match
    const select = document.getElementById(

        "matchSelect"

    );

    select.value = selectedMatchId;


    // Update admin display
    updateAdminPanel();


    // Update other displays
    updateLiveScore();
    updateFixtures();
    updateStandings();
    updateKnockout();

}

/* =========================================================
   LIVE SCORE
========================================================= */

function updateLiveScore() {

    const liveMatch =
        tournamentData.matches.find(
            match =>
                match.status === "live"
        );


    const status =
        document.getElementById("liveStatus");


    const container =
        document.getElementById("liveScoreContainer");


    if (!liveMatch) {

        status.textContent =
            "⏳ NO MATCH LIVE";


        status.classList.remove("active");


        container.innerHTML = `
            <div class="no-live">
                No match is currently live.
            </div>
        `;

        return;

    }


    status.textContent =
        "🔴 LIVE NOW";


    status.classList.add("active");


const currentSet =
    liveMatch.setHistory.length + 1;

const target =
    getTargetScore(liveMatch);

let history = "";


    if (liveMatch.setHistory.length > 0) {

        history =
            liveMatch.setHistory
                .map(
                    (set, index) => `
                        <span>
                            Set ${index + 1}:
                            ${set.a} - ${set.b}
                        </span>
                    `
                )
                .join("");

    }


    container.innerHTML = `

        <div class="live-score-card">

            <div class="live-team">
                ${liveMatch.teamA}
            </div>


            <div class="live-score">
                ${liveMatch.scoreA}
            </div>


            <div class="live-middle">

                SET ${currentSet}

                <strong>
                    ${liveMatch.setsA}
                    -
                    ${liveMatch.setsB}
                </strong>

                <small>
                    Target: ${target}
                </small>

            </div>


            <div class="live-score">
                ${liveMatch.scoreB}
            </div>


            <div class="live-team">
                ${liveMatch.teamB}
            </div>


            <div class="set-history">
                ${history}
            </div>

        </div>

    `;

}


/* =========================================================
   POOLS
========================================================= */

function updatePools() {

    const poolContainers = {
    "Pool 1": "pool1Teams",
    "Pool 2": "pool2Teams",
    "Pool 3": "pool3Teams",
    "Women's Pool": "womensPoolTeams"
};


    Object.entries(poolContainers)
        .forEach(([poolName, elementId]) => {

            const container =
                document.getElementById(elementId);


            container.innerHTML = "";


            tournamentData.pools[poolName]
                .forEach((team, index) => {

                    container.innerHTML += `
                        <div class="pool-team">
                            <span>${index + 1}</span>
                            ${team}
                        </div>
                    `;

                });

        });

}


/* =========================================================
   FIXTURES
========================================================= */
/* FIXTURES */

function updateFixtures() {

    const container =
        document.getElementById("fixturesContainer");

    container.innerHTML = "";


    const poolMatches =
    tournamentData.matches.filter(
        match =>
            match.stage.startsWith("Pool")
            ||
            match.stage === "Women's Pool"
    );


    // =====================================================
    // GROUP MATCHES BY DATE AND SESSION
    // =====================================================

    const groupedFixtures = {};


    poolMatches.forEach(match => {

        const date =
            match.date || "Later Fixtures";

        const session =
            match.session || "Schedule To Be Announced";


        if (!groupedFixtures[date]) {

            groupedFixtures[date] = {};

        }


        if (!groupedFixtures[date][session]) {

            groupedFixtures[date][session] = [];

        }


        groupedFixtures[date][session].push(match);

    });


    // =====================================================
    // DISPLAY FIXTURES
    // =====================================================

    Object.keys(groupedFixtures).forEach(date => {

        container.innerHTML += `

            <div class="fixture-date">

                <h2>📅 ${date}</h2>

            </div>

        `;


        Object.keys(groupedFixtures[date]).forEach(session => {

            container.innerHTML += `

                <div class="fixture-session">

                    <h3>

                        ${session === "Morning Session"
                            ? "🌅 Morning Session"
                            : session === "Evening Session"
                            ? "🌆 Evening Session"
                            : "📌 " + session
                        }

                    </h3>

                </div>

            `;


            groupedFixtures[date][session]

                .forEach(match => {


                    let score = "VS";


                    if (match.status === "finished") {

                        score =
                            `${match.setsA} - ${match.setsB}`;

                    }


                    const matchTime = match.walkover
                        ? "🚫 WALKOVER"
                        : (match.time || "TBA");


                    container.innerHTML += `

                        <div class="match-row">

                            <div class="match-stage">

                                ${match.stage}
                                • Match ${match.id}

                            </div>


                            <div class="match-time">

                                 ${matchTime}

                            </div>


                            <div class="match-teams">

                                ${match.teamA}

                                <b>
                                    ${score}
                                </b>

                                ${match.teamB}

                            </div>


                            <div class="match-status ${match.status}">

                                ${getMatchStatusText(match)}

                            </div>

                            ${match.walkover ? `

                            <div class="walkover-result">

                                🏆 WINNER:
                                <strong>${match.winner}</strong>

                            </div>

                        ` : ""}

                        </div>

                    `;

                });

        });

    });

}
/* =========================================================
   STANDINGS
========================================================= */

function calculateStandings(poolName) {

    const teams =
        tournamentData.pools[poolName];


    const table =
        teams.map(team => ({

            team,

            played: 0,
            won: 0,
            lost: 0,

            // Total individual sets won
            setsWon: 0,
            setsLost: 0,

            // Tournament points
            points: 0

        }));


    const completedMatches =
        tournamentData.matches.filter(
            match =>
                match.stage === poolName
                &&
                match.status === "finished"
        );


    completedMatches.forEach(match => {

        const teamA =
            table.find(
                team =>
                    team.team === match.teamA
            );


        const teamB =
            table.find(
                team =>
                    team.team === match.teamB
            );


        if (!teamA || !teamB) {
            return;
        }


        // Matches played
        teamA.played++;
        teamB.played++;


        // Total sets won and lost
        teamA.setsWon += match.setsA;
        teamA.setsLost += match.setsB;

        teamB.setsWon += match.setsB;
        teamB.setsLost += match.setsA;


        // Match winner
        if (match.winner === match.teamA) {

            teamA.won++;
            teamB.lost++;


            // 2-0 win = 3 points
            // 2-1 win = 2 points
            if (
                match.setsA === 2
                &&
                match.setsB === 0
            ) {

                teamA.points += 3;

            } else if (
                match.setsA === 2
                &&
                match.setsB === 1
            ) {

                teamA.points += 2;

            }


        } else if (match.winner === match.teamB) {

            teamB.won++;
            teamA.lost++;


            // 2-0 win = 3 points
            // 2-1 win = 2 points
            if (
                match.setsB === 2
                &&
                match.setsA === 0
            ) {

                teamB.points += 3;

            } else if (
                match.setsB === 2
                &&
                match.setsA === 1
            ) {

                teamB.points += 2;

            }

        }

    });


    // =====================================================
    // SORT STANDINGS
    // =====================================================

    table.sort((a, b) => {

        // 1. Tournament points
        if (b.points !== a.points) {

            return (
                b.points - a.points
            );

        }


        // 2. Matches won
        if (b.won !== a.won) {

            return (
                b.won - a.won
            );

        }


        // 3. Total sets won
        if (b.setsWon !== a.setsWon) {

            return (
                b.setsWon - a.setsWon
            );

        }


        // 4. Alphabetical order
        return a.team.localeCompare(
            b.team
        );

    });


    return table;

}


/* =========================================================
   DISPLAY STANDINGS
========================================================= */

function updateStandings() {

    const container =
        document.getElementById(
            "standingsContainer"
        );


    container.innerHTML = "";


    [
        "Pool 1",
        "Pool 2",
        "Pool 3",
        "Women's Pool"
    ]
        .forEach(poolName => {


            const table =
                calculateStandings(poolName);

            let qualificationText;

            if (poolName === "Pool 1") {

                qualificationText =
                    "🏆 Top 2 Qualify for Men's Knockout";

            } else if (poolName === "Women's Pool") {

                qualificationText =
                    "🏆 Top 2 Qualify for Women's Final";

            } else {

                qualificationText =
                    "🏆 Top 1 Qualifies for Men's Knockout";

            }


            let rows = "";


            table.forEach(
                (team, index) => {


                    rows += `

                        <tr>

                            <td>
                                ${index + 1}
                            </td>

                            <td>
                                ${team.team}
                            </td>

                            <td>
                                ${team.played}
                            </td>

                            <td>
                                ${team.won}
                            </td>

                            <td>
                                ${team.lost}
                            </td>

                            <td>
                                ${team.setsWon} - ${team.setsLost}
                            </td>

                            <td>
                                <strong>
                                    ${team.points}
                                </strong>
                            </td>

                        </tr>

                    `;

                }
            );


            container.innerHTML += `

                <div class="standing-card">

                    <h2>
                        ${poolName}
                    </h2>


                    <div class="qualification-note">

                        ${qualificationText}

                    </div>


                    <div class="table-wrapper">

                        <table>

                            <thead>

                                <tr>

                                    <th>#</th>

                                    <th>Team</th>

                                    <th>P</th>

                                    <th>W</th>

                                    <th>L</th>

                                    <th>
                                        SETS
                                        <br>
                                        <small>(W-L)</small>
                                    </th>
                                    <th>PTS</th>

                                </tr>

                            </thead>


                            <tbody>

                                ${rows}

                            </tbody>

                        </table>

                    </div>

                </div>

            `;

        });

}
/* =========================================================
   KNOCKOUT
========================================================= */
function updateKnockout() {

    const container =
        document.getElementById("knockoutContainer");

    if (!container || !tournamentData) {
        return;
    }

    container.innerHTML = "";


    // =====================================================
    // MEN'S KNOCKOUT
    // =====================================================

    const mensMatches =
        tournamentData.matches.filter(
            match =>
                match.stage === "Semi Final"
                ||
                match.stage === "Final"
        );


    container.innerHTML += `

        <h2 class="knockout-heading">
            🏆 MEN'S KNOCKOUT
        </h2>

    `;


    mensMatches.forEach(match => {

        let score = "VS";

        if (
            match.status === "finished"
            ||
            match.status === "live"
        ) {

            score =
                `${match.setsA} - ${match.setsB}`;

        }


        container.innerHTML += `

            <div class="match-row">

                <div class="match-stage">
                    ${match.label || match.stage}
                </div>


                <div class="match-teams">

                    ${match.teamA}

                    <b>${score}</b>

                    ${match.teamB}

                </div>


                <div class="knockout-schedule">

                    📅 ${match.date || "TBA"}

                    <br>

                    ⏰ ${match.time || "TBA"}

                </div>


                <div class="
                    match-status
                    ${match.status}
                ">

                    ${getMatchStatusText(match)}

                </div>

            </div>

        `;

    });


    // =====================================================
    // WOMEN'S FINAL
    // =====================================================

    const womensFinal =
        tournamentData.matches.filter(
            match =>
                match.stage === "Women's Final"
        );


    if (womensFinal.length > 0) {

        container.innerHTML += `

            <h2 class="knockout-heading womens-heading">
                👑 WOMEN'S FINAL
            </h2>

        `;

    }


    womensFinal.forEach(match => {

        let score = "VS";


        if (
            match.status === "finished"
            ||
            match.status === "live"
        ) {

            score =
                `${match.setsA} - ${match.setsB}`;

        }


        container.innerHTML += `

            <div class="match-row womens-final-row">

                <div class="match-stage">
                    WOMEN'S FINAL
                </div>


                <div class="match-teams">

                    ${match.teamA}

                    <b>${score}</b>

                    ${match.teamB}

                </div>


                <div class="knockout-schedule">

                    📅 ${match.date || "TBA"}

                    <br>

                    ⏰ ${match.time || "TBA"}

                </div>


                <div class="
                    match-status
                    ${match.status}
                ">

                    ${getMatchStatusText(match)}

                </div>

            </div>

        `;

    });

}


function updateScoringFormatButtons() {

    if (!tournamentData) {
        return;
    }

    const format =
        tournamentData.scoring_format ||
        "25-25-15";

    const button252515 =
        document.getElementById("format252515");

    const button151525 =
        document.getElementById("format151525");

    const note =
        document.getElementById("scoringFormatNote");


    if (button252515 && button151525) {

        button252515.classList.toggle(
            "active",
            format === "25-25-15"
        );

        button151525.classList.toggle(
            "active",
            format === "15-15-25"
        );

    }


    if (note) {

        if (format === "15-15-25") {

            note.textContent =
                "Best of 3 Sets • Sets 1 & 2: Minimum 15 Points • Deciding Set: Minimum 25 Points • 2 Point Lead Required";

        } else {

            note.textContent =
                "Best of 3 Sets • Sets 1 & 2: Minimum 25 Points • Deciding Set: Minimum 15 Points • 2 Point Lead Required";

        }

    }

}
/* =========================================================
   RESET TOURNAMENT
========================================================= */
async function setScoringFormat(format) {

    try {

        const response = await fetch("/api/scoring-format", {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                scoring_format: format
            })

        });


        const result = await response.json();


        if (!response.ok) {

            alert(
                result.error ||
                "Could not update scoring format."
            );

            return;

        }


        tournamentData.scoring_format =
            result.scoring_format;


        updateEverything();


    } catch (error) {

        console.error(
            "Scoring format error:",
            error
        );

        alert(
            "Network error while changing scoring format."
        );

    }


// Update local tournament data immediately
tournamentData.scoring_format =
    result.scoring_format;


// Refresh all UI elements
updateEverything();
}

document.addEventListener("DOMContentLoaded", async () => {

    await checkAdminStatus();

    await loadData();

});