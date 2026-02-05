// =======================
// GLOBAL STATE
// =======================
let appState = {
    homeType: '',
    familySize: 2,
    selectedAppliances: [],
    applianceDetails: {},
    currentApplianceIndex: 0
};

const applianceIcons = {
    'AC': '❄️',
    'Fan': '🌀',
    'TV': '📺',
    'Fridge': '🧊',
    'Washing Machine': '🧺',
    'Geyser': '🚿',
    'Lights': '💡',
    'Air Cooler': '🌬️'
};

// =======================
// NAVIGATION
// =======================
function showScreen(id) {
    document.querySelectorAll('.screen').forEach(s => s.classList.remove('active'));
    document.getElementById(id).classList.add('active');
}

// =======================
// SCREEN 1 – BASIC INPUT
// =======================
const familySizeSlider = document.getElementById('familySize');
const familySizeValue = document.getElementById('familySizeValue');

familySizeSlider.oninput = () => {
    familySizeValue.textContent = familySizeSlider.value;
    appState.familySize = parseInt(familySizeSlider.value);
    validateStep1();
};

document.querySelectorAll('.radio-card').forEach(card => {
    card.onclick = () => {
        document.querySelectorAll('.radio-card').forEach(c => c.classList.remove('selected'));
        card.classList.add('selected');
        card.querySelector('input').checked = true;
        appState.homeType = card.dataset.value;
        validateStep1();
    };
});

function validateStep1() {
    document.getElementById('continueStep1').disabled = !appState.homeType;
}

document.getElementById('continueStep1').onclick = () => showScreen('screen2');

// =======================
// SCREEN 2 – APPLIANCES
// =======================
document.querySelectorAll('.appliance-card').forEach(card => {
    card.onclick = () => {
        card.classList.toggle('selected');
        card.querySelector('input').checked = card.classList.contains('selected');
        updateApplianceSelection();
    };
});

function updateApplianceSelection() {
    const checked = document.querySelectorAll('input[name="appliances"]:checked');
    appState.selectedAppliances = Array.from(checked).map(c => c.value);
    document.getElementById('selectionCounter').textContent =
        `✅ ${appState.selectedAppliances.length} appliances selected`;
    document.getElementById('continueStep2').disabled =
        appState.selectedAppliances.length === 0;
}

document.getElementById('continueStep2').onclick = () => {
    appState.currentApplianceIndex = 0;
    loadApplianceDetails();
    showScreen('screen3');
};

// =======================
// SCREEN 3 – DETAILS
// =======================
const usageHoursSlider = document.getElementById('usageHours');
const usageHoursValue = document.getElementById('usageHoursValue');

usageHoursSlider.oninput = () =>
    usageHoursValue.textContent = usageHoursSlider.value;

document.querySelectorAll('.quantity-option').forEach(o =>
    o.onclick = () => {
        document.querySelectorAll('.quantity-option').forEach(x => x.classList.remove('selected'));
        o.classList.add('selected');
    }
);

document.querySelectorAll('.condition-option').forEach(o =>
    o.onclick = () => {
        document.querySelectorAll('.condition-option').forEach(x => x.classList.remove('selected'));
        o.classList.add('selected');
    }
);

function loadApplianceDetails() {
    const name = appState.selectedAppliances[appState.currentApplianceIndex];
    document.getElementById('currentApplianceName').innerHTML =
        `${applianceIcons[name] || '⚡'} ${name}`;
}

function saveCurrentApplianceDetails() {
    const appliance = appState.selectedAppliances[appState.currentApplianceIndex];
    appState.applianceDetails[appliance] = {
        hours: parseFloat(usageHoursSlider.value),
        quantity: parseInt(document.querySelector('.quantity-option.selected')?.dataset.value || 1),
        condition: document.querySelector('.condition-option.selected')?.dataset.value || 'moderate'
    };
}

document.getElementById('nextAppliance').onclick = () => {
    saveCurrentApplianceDetails();
    if (++appState.currentApplianceIndex < appState.selectedAppliances.length) {
        loadApplianceDetails();
    } else {
        sendToBackend();
    }
};

// =======================
// SEND TO BACKEND
// =======================
function sendToBackend() {
    const payload = {
        family_size: appState.familySize,
        num_appliances: appState.selectedAppliances.length,
        total_hours: Object.values(appState.applianceDetails)
            .reduce((s, a) => s + a.hours, 0),
        avg_condition: 1.2,
        appliance_breakdown: appState.applianceDetails
    };

    fetch("/predict", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload)
    })
    .then(res => res.json())
    .then(result => {
        document.getElementById("estimatedUsage").innerText =
            result.predicted_units;

        renderSuggestions(result.suggestions);
        createPieChart(result.appliance_breakdown);

        showScreen("screen5");
    })
    .catch(err => console.error("Backend error:", err));
}
function createPieChart(breakdown) {
    const labels = Object.keys(breakdown);
    const values = Object.values(breakdown).map(a => a.hours);

    const ctx = document.getElementById("pieChart").getContext("2d");

    if (window.usageChart) {
        window.usageChart.destroy();
    }

    window.usageChart = new Chart(ctx, {
        type: "pie",
        data: {
            labels: labels,
            datasets: [{
                data: values
            }]
        }
    });
}

// =======================
// SUGGESTIONS
// =======================
function renderSuggestions(suggestions) {
    document.getElementById('suggestionsContainer').innerHTML =
        suggestions.map(s => `<div class="suggestion-card">${s}</div>`).join('');
}

// =======================
// INIT
// =======================
document.addEventListener('DOMContentLoaded', () => {
    validateStep1();
    updateApplianceSelection();
});
