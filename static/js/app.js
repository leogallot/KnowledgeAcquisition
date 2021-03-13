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
const TAB_ENTITIES = document.getElementsByClassName('tab-entities')[0];
const BTN_TAB_ENTITIES = document.getElementById('tab-entities-btn');

const TEXT_CONTAINER = document.getElementById('text');

let user = {
    search_options_visible: true,
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

// Manage button tab:entities
BTN_TAB_ENTITIES.addEventListener('click', ev => {
    ev.preventDefault();
    if (user.current_tab !== TAB_ENTITIES) {
        switchBtnTab(BTN_TAB_ENTITIES, TAB_ENTITIES);
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
    TAB.style.display = 'block';
    user.current_tab.style.display = 'block';

    processText(data['text']);
    processEntities(data['yago']);
    google.charts.setOnLoadCallback(drawChart(data['pure']));
}

// Draw relation graph
function drawChart(data) {
    let table = new google.visualization.DataTable();

    table.addColumn('string', 'name')
    table.addColumn('string', 'manager')

    let tableData  = [
        ['toptype', ''],
        ['person', 'toptype'],
        ['organization', 'toptype'],
        ['event', 'toptype'],
        ['artifact', 'toptype'],
        ['yagogeoentity', 'toptype']
    ];

    tableData = addDataChart(tableData, data);
    table.addRows(tableData);
    let chart = new google.visualization.OrgChart(document.getElementById('chart'));
    chart.draw(table, {"allowHtml": false});
}

// Add data to graph
function addDataChart(array, data) {
    data.forEach(item => {
        let top = item.top;
        let wordnet = Object.keys(item.content);

        // loop for each wordnet
        for (let index = 0; index < wordnet.length; index++) {
            let current = wordnet[index];

            array.push([current, top]);

            // loop for each word:score
            for (let i = 0; i < item.content[current].length; i++) {
                let id_word = item.content[current][i]['word']+'_'+current+'_';
                let id_score = id_word+'_'+item.content[current][i]['score']+'_'+i;

                array.push([{'v': id_score, 'f': item.content[current][i]['score'].toString()}, current]);
                array.push([{v: id_word, f: item.content[current][i]['word']},  id_score]);
            }
        }
    });
    return array;
}

// Process text
function processText(text) {
    cleanText();
    text.forEach(item => {
        if (item.mark) {
            let temp_link = document.createElement('a');
            temp_link.href = item.link;
            temp_link.innerHTML = item.word;
            temp_link.target = '_blank';
            TEXT_CONTAINER.appendChild(temp_link);
            TEXT_CONTAINER.innerHTML = TEXT_CONTAINER.innerHTML + ' '; // add space
        } else {
            TEXT_CONTAINER.innerHTML = TEXT_CONTAINER.innerHTML + item.word + ' ';
        }
    });
}

// Process entities
function processEntities(data) {
    console.log(data);
    const CONTAINER = document.getElementsByClassName('entities')[0];
    for (let index = 0; index < data.length; index++) {
        const DIV = document.createElement('div');
        DIV.classList.add('entities-container')
        const TITLE = document.createElement('h3');
        const CONTENT = document.createElement('p');

        TITLE.innerText = data[index]['word'];
        for (let yago_index = 0; yago_index < data[index]['yago'].length; yago_index++) {
            let li = document.createElement('i');
            li.innerText = data[index]['yago'][yago_index];
            CONTENT.appendChild(li);
        }
        DIV.appendChild(TITLE);
        DIV.appendChild(CONTENT);
        CONTAINER.appendChild(DIV);
    }
}

// Clean text area
function cleanText() {
    TEXT_CONTAINER.innerHTML = '';
}
