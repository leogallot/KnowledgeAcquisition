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

let search_options_visible = true;

// Manage search options display
SEARCH_OPTIONS_BTN.addEventListener('click', ev => {
    if (search_options_visible) {
        SEARCH_OPTIONS_CONTAINER.style.display = 'none';
        SEARCH_OPTIONS_ICON.classList.remove('icon-up');
        SEARCH_OPTIONS_ICON.classList.add('icon-down');
        search_options_visible = false;
    }
    else {
        SEARCH_OPTIONS_CONTAINER.style.display = 'flex';
        SEARCH_OPTIONS_ICON.classList.remove('icon-down');
        SEARCH_OPTIONS_ICON.classList.add('icon-up');
        search_options_visible = true;
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
            console.log(response);
            LOADER.style.display = 'none';
            SUBMIT_BTN.disabled = false;
        });

});

// Show dialog window
function showDialogWindow(title, content) {
    DIALOG.style.display = 'block';
    DIALOG_TITLE.innerText = title;
    DIALOG_CONTENT.innerText = content;
}