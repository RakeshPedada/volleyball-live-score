let tournamentData = null;
let selectedMatchId = null;
let isAdmin = false;


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


    const completedSets =
        match.setHistory.length;


    const target =
        completedSets === 2
            ? 15
            : 25;


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

    if (!selectedMatchId) return;


    const response = await fetch(
        `/api/point/${selectedMatchId}/${side}`,
        {
            method: "POST"
        }
    );


    const result =
        await response.json();


    if (!response.ok) {

        alert(
            result.error
            || "Could not add point."
        );

        return;

    }


    await loadData();

}


/* =========================================================
   UNDO POINT
========================================================= */

async function undoPoint(side) {

    if (!selectedMatchId) return;


    const response = await fetch(
        `/api/undo/${selectedMatchId}/${side}`,
        {
            method: "POST"
        }
    );


    const result =
        await response.json();


    if (!response.ok) {

        alert(
            result.error
            || "Could not undo point."
        );

        return;

    }


    await loadData();

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
        currentSet === 3
            ? 15
            : 25;


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
        "Pool 3": "pool3Teams"
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

function updateFixtures() {

    const container =
        document.getElementById(
            "fixturesContainer"
        );


    container.innerHTML = "";


    tournamentData.matches
        .filter(
            match =>
                match.stage.startsWith("Pool")
        )
        .forEach(match => {

            let score = "VS";


            if (
                match.status === "finished"
                || match.status === "live"
            ) {

                score =
                    `${match.setsA} - ${match.setsB}`;

            }


            container.innerHTML += `

                <div class="match-row">

                    <div class="match-stage">
                        ${match.stage}
                        • Match ${match.id}
                    </div>


                    <div class="match-teams">

                        ${match.teamA}

                        <b>${score}</b>

                        ${match.teamB}

                    </div>


                    <div class="
                        match-status
                        ${match.status}
                    ">

                        ${match.status.toUpperCase()}

                    </div>

                </div>

            `;

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

            setsFor: 0,
            setsAgainst: 0,

            pointsFor: 0,
            pointsAgainst: 0

        }));


    const completedMatches =
        tournamentData.matches.filter(
            match =>
                match.stage === poolName
                && match.status === "finished"
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


        if (!teamA || !teamB) return;


        teamA.played++;
        teamB.played++;


        teamA.setsFor +=
            match.setsA;

        teamA.setsAgainst +=
            match.setsB;


        teamB.setsFor +=
            match.setsB;

        teamB.setsAgainst +=
            match.setsA;


        if (
            match.winner === match.teamA
        ) {

            teamA.won++;
            teamB.lost++;

        } else {

            teamB.won++;
            teamA.lost++;

        }


        match.setHistory.forEach(set => {

            teamA.pointsFor += set.a;
            teamA.pointsAgainst += set.b;

            teamB.pointsFor += set.b;
            teamB.pointsAgainst += set.a;

        });

    });


    table.sort((a, b) => {

        if (b.won !== a.won) {

            return b.won - a.won;

        }


        const setDifferenceA =
            a.setsFor - a.setsAgainst;

        const setDifferenceB =
            b.setsFor - b.setsAgainst;


        if (
            setDifferenceB
            !==
            setDifferenceA
        ) {

            return (
                setDifferenceB
                -
                setDifferenceA
            );

        }


        const pointDifferenceA =
            a.pointsFor - a.pointsAgainst;

        const pointDifferenceB =
            b.pointsFor - b.pointsAgainst;


        if (
            pointDifferenceB
            !==
            pointDifferenceA
        ) {

            return (
                pointDifferenceB
                -
                pointDifferenceA
            );

        }


        return a.team.localeCompare(
            b.team
        );

    });


    return table;

}


function updateStandings() {

    const container =
        document.getElementById(
            "standingsContainer"
        );


    container.innerHTML = "";


    [
        "Pool 1",
        "Pool 2",
        "Pool 3"
    ]
        .forEach(poolName => {

            const table =
                calculateStandings(poolName);


            const qualificationText =
                poolName === "Pool 1"
                    ? "🏆 Top 2 Qualify"
                    : "🏆 Top 1 Qualifies";


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
                                ${
                                    team.setsFor
                                    -
                                    team.setsAgainst
                                }
                            </td>

                            <td>
                                ${
                                    team.pointsFor
                                    -
                                    team.pointsAgainst
                                }
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


                    <table>

                        <thead>

                            <tr>

                                <th>#</th>
                                <th>Team</th>
                                <th>P</th>
                                <th>W</th>
                                <th>L</th>
                                <th>Set +/-</th>
                                <th>Point +/-</th>

                            </tr>

                        </thead>


                        <tbody>

                            ${rows}

                        </tbody>

                    </table>


                    <p class="qualify-text">

                        ${qualificationText}

                    </p>

                </div>

            `;

        });

}


/* =========================================================
   KNOCKOUT
========================================================= */

function updateKnockout() {

    const container =
        document.getElementById(
            "knockoutContainer"
        );


    container.innerHTML = "";


    tournamentData.matches
        .filter(
            match =>
                match.stage === "Semi Final"
                ||
                match.stage === "Final"
        )
        .forEach(match => {

            let score = "VS";


            if (
                match.status === "finished"
                || match.status === "live"
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


                    <div class="
                        match-status
                        ${match.status}
                    ">

                        ${match.status.toUpperCase()}

                    </div>

                </div>

            `;

        });

}


/* =========================================================
   RESET TOURNAMENT
========================================================= */

async function resetTournament() {

    const confirmed =
        confirm(
            "Are you sure you want to reset the entire tournament?"
        );


    if (!confirmed) return;


    const response = await fetch(
        "/api/reset",
        {
            method: "POST"
        }
    );


    const result =
        await response.json();


    if (!response.ok) {

        alert(
            result.error
            || "Could not reset tournament."
        );

        return;

    }


    selectedMatchId = null;


    await loadData();

}


/* =========================================================
   INITIALIZATION
========================================================= */

async function initializeApp() {

    await checkAdminStatus();

    await loadData();

}


initializeApp();


/* Refresh live data every 3 seconds */

setInterval(
    loadData,
    3000
);