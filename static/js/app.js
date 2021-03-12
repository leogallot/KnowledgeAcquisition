google.charts.load('current', {packages:["orgchart"]});

const SEARCH_OPTIONS_BTN = document.getElementById('search-options-btn');
const SEARCH_OPTIONS_ICON = document.getElementById('search-options-icon');
const SEARCH_OPTIONS_CONTAINER = document.getElementsByClassName('search-options')[0];

const LOADER = document.getElementsByClassName('loader')[0];
const FORM = document.getElementById('form');
const SUBMIT_BTN = document.getElementById('submit_btn');

const DIALOG = document.getElementsByClassName('dialog-bg')[0];
const DIALOG_TITLE = document.getElementById('dialog-title');
const DIALOG_CONTENT = document.getElementById('dialog-content');
const EXIT_DIALOG_BTN = document.getElementById('exit-dialog');

const TAB = document.getElementsByClassName('nav-container')[0];
const TAB_RELATIONS = document.getElementsByClassName('tab-relations')[0];
const BTN_TAB_RELATIONS = document.getElementById('tab-relations-btn');
const TAB_TEXT = document.getElementsByClassName('tab-text')[0];
const BTN_TAB_TEXT = document.getElementById('tab-text-btn');

const TEXT_CONTAINER = document.getElementById('text');

let user = {
    search_options_visible: true,
    tab_visible: false,
    current_tab: TAB_TEXT,
    current_tab_btn: BTN_TAB_TEXT
}

// Manage search options display
SEARCH_OPTIONS_BTN.addEventListener('click', ev => {
    if (user.search_options_visible) {
        SEARCH_OPTIONS_CONTAINER.style.display = 'none';
        SEARCH_OPTIONS_ICON.classList.remove('icon-up');
        SEARCH_OPTIONS_ICON.classList.add('icon-down');
        user.search_options_visible = false;
    }
    else {
        SEARCH_OPTIONS_CONTAINER.style.display = 'flex';
        SEARCH_OPTIONS_ICON.classList.remove('icon-down');
        SEARCH_OPTIONS_ICON.classList.add('icon-up');
        user.search_options_visible = true;
    }
});

// Exit dialog window
EXIT_DIALOG_BTN.addEventListener('click', ev => {
    DIALOG.style.display = 'none';
});

// Process form
FORM.addEventListener('submit', ev => {
    ev.preventDefault();
    SUBMIT_BTN.disabled = true;
    LOADER.style.display = 'block';

    const FORM_DATA = new FormData(FORM);
    const DATA = {
        'url': FORM_DATA.get('url'),
        'username': FORM_DATA.get('username'),
        'password': FORM_DATA.get('password'),
        'location': FORM_DATA.get('location')
    };

    fetch('/endpoint/', {
        method: 'POST',
        body: JSON.stringify(DATA),
        headers: {
            'content-type': 'application/json'
        }
    })
        .then(response => response.json())
        .then(response => {
            LOADER.style.display = 'none';
            SUBMIT_BTN.disabled = false;
            processData(response);
        });

});

// Manage button tab:text
BTN_TAB_TEXT.addEventListener('click', ev => {
    ev.preventDefault();
    if (user.current_tab !== TAB_TEXT) {
        switchBtnTab(BTN_TAB_TEXT, TAB_TEXT);
    }
});

// Manage button tab:relations
BTN_TAB_RELATIONS.addEventListener('click', ev => {
    ev.preventDefault();
    if (user.current_tab !== TAB_RELATIONS) {
        switchBtnTab(BTN_TAB_RELATIONS, TAB_RELATIONS);
    }
});

// Switch tabs
function switchBtnTab(new_btn, new_tab) {
    user.current_tab_btn.classList.remove('active');
    user.current_tab.style.display = 'none';
    new_btn.classList.add('active');
    new_tab.style.display = 'block';

    user.current_tab_btn = new_btn;
    user.current_tab = new_tab;
    // TODO : update tab view
}

// Show dialog window
function showDialogWindow(title, content) {
    DIALOG.style.display = 'block';
    DIALOG_TITLE.innerText = title;
    DIALOG_CONTENT.innerText = content;
}

// Process data from /endpoint/
function processData(data) {
    if (data.send === false) {
        if (data.error === 'scrap')
            showDialogWindow('Ouups ...', 'Our scrapper can\'t scrap this website. Try with another website to use this tool.');
    }
    else {
        if (data.success === false) {
            showDialogWindow('Ouups ...', 'The engine can\'t run. Check if AIDA location and login are corrects.');
        }
        else {
            // display results
            processOutput(data);
        }
    }
}

// Process result
function processOutput(data) {
    TEXT_CONTAINER.innerText = data['text']; // display text
    TAB.style.display = 'block';
    TAB_TEXT.style.display = 'block';

    google.charts.setOnLoadCallback(drawChart(data['pure']));
}

// Draw relation graph
function drawChart(data) {
    TAB_RELATIONS.style.display = 'block';
    let table = new google.visualization.DataTable();

    table.addColumn('string', 'name')
    table.addColumn('string', 'manager')
    table.addColumn('string', 'score')

    let tableData  = [
        ['entity', '', ''],
        ['person', 'entity', ''],
        ['organization', 'entity', ''],
        ['event', 'entity', ''],
        ['artifact', 'entity', ''],
        ['yagogeoentity', 'entity', '']
    ];

    tableData = addDataChart(tableData, data);
    table.addRows(tableData);
    let chart = new google.visualization.OrgChart(document.getElementById('chart'));
    chart.draw(table, {"allowHtml": false});
}

// Add data to graph
function addDataChart(array, data) {
    data.forEach(item => {
        for(let i = 0; i < item.content.length; i++) {
            array.push([item.content[i].wordnet, item.top, item.content[i].score.toString()]);
        }
    });
    return array;
}