const SEARCH_OPTIONS_BTN = document.getElementById('search-options-btn');
const SEARCH_OPTIONS_ICON = document.getElementById('search-options-icon');
const SEARCH_OPTIONS_CONTAINER = document.getElementsByClassName('search-options')[0];
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
