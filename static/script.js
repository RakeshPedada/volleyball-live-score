let tournamentData = null;

let selectedMatchId = null;


/* LOAD DATA */

async function loadData() {

    const response = await fetch("/api/data");

    tournamentData = await response.json();

    updateEverything();

}


/* UPDATE EVERYTHING */

function updateEverything() {

    updateMatchSelect();

    updateLiveScore();

    updatePools();

    updateFixtures();

    updateStandings();

    updateKnockout();

    updateAdminPanel();

}


/* PAGE NAVIGATION */

function showPage(page, button) {

    document.querySelectorAll(".page").forEach(p => {

        p.classList.add("hidden");

    });

    document.getElementById(page + "Page").classList.remove("hidden");


    document.querySelectorAll(".nav-btn").forEach(btn => {

        btn.classList.remove("active");

    });

    button.classList.add("active");

}


/* ADMIN TOGGLE */

/* ===================================
   ADMIN AUTHENTICATION
=================================== */

let isAdmin = false;


/* OPEN LOGIN */

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


/* CLOSE LOGIN */

function closeAdminLogin() {

    document
        .getElementById("loginModal")
        .classList.add("hidden");

    document
        .getElementById("loginError")
        .textContent = "";

}


/* LOGIN */

async function loginAdmin() {

    const username =
        document.getElementById("adminUsername").value;

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

                username: username,

                password: password

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
        .textContent =
        "⚙ ADMIN PANEL";

}


/* CHECK EXISTING SESSION */

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

    }

    catch (error) {

        console.error(
            "Could not check admin status",
            error
        );

    }

}



/* MATCH SELECT */

function updateMatchSelect() {

    const select = document.getElementById("matchSelect");

    select.innerHTML = "";

    tournamentData.matches.forEach(match => {

        if (match.status === "locked") return;

        const option = document.createElement("option");

        option.value = match.id;

        option.textContent =
            `Match ${match.id} • ${match.teamA} vs ${match.teamB}`;

        select.appendChild(option);

    });


    if (selectedMatchId === null) {

        selectedMatchId = Number(select.value);

    }

    select.value = selectedMatchId;


    select.onchange = () => {

        selectedMatchId = Number(select.value);

        updateAdminPanel();

    };

}


/* GET SELECTED MATCH */

function getSelectedMatch() {

    return tournamentData.matches.find(
        m => m.id === selectedMatchId
    );

}


/* ADMIN DISPLAY */

function updateAdminPanel() {

    const match = getSelectedMatch();

    if (!match) return;

    document.getElementById("adminTeamA").textContent =
        match.teamA;

    document.getElementById("adminTeamB").textContent =
        match.teamB;

    document.getElementById("adminScoreA").textContent =
        match.scoreA;

    document.getElementById("adminScoreB").textContent =
        match.scoreB;

    document.getElementById("adminSets").textContent =
        `${match.setsA} - ${match.setsB}`;


    let target = 25;

    if (match.setsA === 1 && match.setsB === 1) {

        target = 15;

    }

    document.getElementById("targetText").textContent =
        `Target: ${target}`;

}


/* START MATCH */

async function startSelectedMatch() {

    const response = await fetch(
        `/api/start/${selectedMatchId}`,
        {
            method: "POST"
        }
    );

    const result = await response.json();

    if (result.error) {

        alert(result.error);

    }

    await loadData();

}


/* ADD POINT */

async function addPoint(side) {

    const response = await fetch(

        `/api/point/${selectedMatchId}/${side}`,

        {
            method: "POST"
        }

    );

    const result = await response.json();

    if (result.error) {

        alert(result.error);

    }

    await loadData();

}


/* UNDO POINT */

async function undoPoint(side) {

    await fetch(

        `/api/undo/${selectedMatchId}/${side}`,

        {
            method: "POST"
        }

    );

    await loadData();

}


/* LIVE SCORE */

function updateLiveScore() {

    const liveMatch = tournamentData.matches.find(
        m => m.status === "live"
    );


    const status = document.getElementById("liveStatus");

    const container =
        document.getElementById("liveScoreContainer");


    if (!liveMatch) {

        status.textContent = "⏳ NO MATCH LIVE";

        status.classList.remove("active");

        container.innerHTML = `

            <div class="no-live">

                Select a match from the Admin Panel
                and press <b>START MATCH</b>.

            </div>

        `;

        return;

    }


    status.textContent = "🔴 LIVE NOW";

    status.classList.add("active");


    let history = "";

    if (liveMatch.setHistory.length > 0) {

        history =
            liveMatch.setHistory
                .map((set, index) =>
                    `<span>Set ${index + 1}: ${set.a}-${set.b}</span>`
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

                SETS

                <strong>

                    ${liveMatch.setsA}
                    -
                    ${liveMatch.setsB}

                </strong>

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


/* POOL TEAMS */

function updatePools() {

    tournamentData.pools["Pool 1"]
        .forEach((team, index) => {

            document.getElementById("pool1Teams")
                .innerHTML += `
                    <div class="pool-team">
                        <span>${index + 1}</span>
                        ${team}
                    </div>
                `;

        });


    tournamentData.pools["Pool 2"]
        .forEach((team, index) => {

            document.getElementById("pool2Teams")
                .innerHTML += `
                    <div class="pool-team">
                        <span>${index + 1}</span>
                        ${team}
                    </div>
                `;

        });


    tournamentData.pools["Pool 3"]
        .forEach((team, index) => {

            document.getElementById("pool3Teams")
                .innerHTML += `
                    <div class="pool-team">
                        <span>${index + 1}</span>
                        ${team}
                    </div>
                `;

        });

}


/* FIXTURES */

function updateFixtures() {

    const container =
        document.getElementById("fixturesContainer");

    container.innerHTML = "";


    tournamentData.matches
        .filter(match =>
            match.stage.startsWith("Pool")
        )
        .forEach(match => {

            let score = "VS";

            if (match.status === "finished") {

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

                        <b>
                            ${score}
                        </b>

                        ${match.teamB}

                    </div>


                    <div class="match-status ${match.status}">

                        ${match.status.toUpperCase()}

                    </div>

                </div>

            `;

        });

}


/* STANDINGS */

function calculateStandings(poolName) {

    const teams =
        tournamentData.pools[poolName];


    let table = teams.map(team => ({

        team,

        played: 0,

        won: 0,

        lost: 0,

        setsFor: 0,

        setsAgainst: 0,

        pointsFor: 0,

        pointsAgainst: 0

    }));


    const matches =
        tournamentData.matches.filter(
            match =>
                match.stage === poolName &&
                match.status === "finished"
        );


    matches.forEach(match => {

        const teamA =
            table.find(t =>
                t.team === match.teamA
            );

        const teamB =
            table.find(t =>
                t.team === match.teamB
            );


        teamA.played++;

        teamB.played++;


        teamA.setsFor += match.setsA;

        teamA.setsAgainst += match.setsB;


        teamB.setsFor += match.setsB;

        teamB.setsAgainst += match.setsA;


        if (match.winner === match.teamA) {

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

        if (b.won !== a.won)
            return b.won - a.won;


        const setDiffA =
            a.setsFor - a.setsAgainst;

        const setDiffB =
            b.setsFor - b.setsAgainst;

        if (setDiffB !== setDiffA)
            return setDiffB - setDiffA;


        const pointDiffA =
            a.pointsFor - a.pointsAgainst;

        const pointDiffB =
            b.pointsFor - b.pointsAgainst;

        if (pointDiffB !== pointDiffA)
            return pointDiffB - pointDiffA;


        return a.team.localeCompare(b.team);

    });


    return table;

}


function updateStandings() {

    const container =
        document.getElementById("standingsContainer");

    container.innerHTML = "";


    ["Pool 1", "Pool 2", "Pool 3"]
        .forEach(pool => {

            const table =
                calculateStandings(pool);


            const qualify =
                pool === "Pool 1"
                    ? "🏆 Top 2 Qualify"
                    : "🏆 Top 1 Qualifies";


            let rows = "";


            table.forEach((team, index) => {

                rows += `

                    <tr>

                        <td>${index + 1}</td>

                        <td>${team.team}</td>

                        <td>${team.played}</td>

                        <td>${team.won}</td>

                        <td>${team.lost}</td>

                        <td>
                            ${team.setsFor - team.setsAgainst}
                        </td>

                        <td>
                            ${team.pointsFor - team.pointsAgainst}
                        </td>

                    </tr>

                `;

            });


            container.innerHTML += `

                <div class="standing-card">

                    <h2>${pool}</h2>

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

                        ${qualify}

                    </p>

                </div>

            `;

        });

}


/* KNOCKOUT */

function updateKnockout() {

    const container =
        document.getElementById("knockoutContainer");

    container.innerHTML = "";


    tournamentData.matches
        .filter(match =>
            match.stage === "Semi Final" ||
            match.stage === "Final"
        )
        .forEach(match => {

            let score = "VS";

            if (match.status === "finished") {

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

                        <b>
                            ${score}
                        </b>

                        ${match.teamB}

                    </div>


                    <div class="match-status">

                        ${match.status.toUpperCase()}

                    </div>

                </div>

            `;

        });

}


/* RESET */

async function resetTournament() {

    const confirmReset =
        confirm(
            "Are you sure you want to reset the entire tournament?"
        );


    if (!confirmReset) return;


    await fetch(
        "/api/reset",
        {
            method: "POST"
        }
    );


    selectedMatchId = 1;


    await loadData();

}
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


    alert("Logged out successfully");

}


/* AUTO REFRESH */

/* CHECK LOGIN SESSION */

checkAdminStatus();


/* AUTO REFRESH DATA */

setInterval(loadData, 3000);


/* INITIAL LOAD */

loadData();