const searchName = document.querySelector('[name="search"]');
const searchSubmit = document.querySelector('#search-submit');
const warning = document.querySelector('#warning');
const selectSubmit = document.getElementById('episode');
const stageForm = document.querySelector('[name="stageForm"]');


// Submit search form. If search has less than two characters, show warning.
searchSubmit.onclick = (event) => {
    event.preventDefault();
    warning.classList.add("hidden");
    if (searchName.value.length > 1) {
        document.stageForm.submit();
    } else {
        warning.classList.remove("hidden");
    }
};

// Submit select form on change.
selectSubmit.onchange = (event) => {
    document.stageForm.submit();
};

// Submit form to filter the index.
stageForm.onsubmit = (event) => {
    event.preventDefault();
    warning.classList.add("hidden");
    if (searchName.value.length > 0 && searchName.value.length < 2) {
        warning.classList.remove("hidden");
    } else {
        document.stageForm.submit();
    }
};

warning.onclick = (event) => {
    warning.classList.add("hidden");
};
