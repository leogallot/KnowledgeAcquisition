const SEARCH_OPTIONS_BTN = document.getElementById('search-options-btn');
const SEARCH_OPTIONS_ICON = document.getElementById('search-options-icon');
const SEARCH_OPTIONS_CONTAINER = document.getElementsByClassName('search-options')[0];
const LOADER = document.getElementsByClassName('loader')[0];
const FORM = document.getElementById('form');
const SUBMIT_BTN = document.getElementById('submit_btn');
let search_options_visible = true;

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
