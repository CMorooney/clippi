function init() {
    const sourceDropdown = document.querySelector('#source-form-source');
    sourceDropdown.addEventListener('change', uploadSourceChanged);

    const inputForm = document.getElementById("renameForm");
    form.addEventListener("submit", function(event) {
        // First, prevent the default form submission behavior
        event.preventDefault();
    });
}

function uploadSourceChanged(e) {
    const ytForm = document.querySelector('#youtube-form');
    const uploadForm = document.querySelector('#upload-form');

    if (e.target.value == "youtube") {
        ytForm.style.display = "flex";
        uploadForm.style.display = "none";
    } else if (e.target.value == "local") {
        ytForm.style.display = "none";
        uploadForm.style.display = "flex";
    }
}

function showLoader() {
    const modal = document.getElementById("loadingModal");
    modal.style.display = "flex";
}

function showRenameInput(currentName, clipIndexString, bankIndexString) {
    const modal = document.getElementById("renameModal");
    modal.style.display = "flex";

    const input = document.getElementById("new-file-name");
    input.value = currentName.split('__')[1];

    const clipIndexInput = document.getElementById("rename-file-clip-index");
    clipIndexInput.value = parseInt(clipIndexString);

    const bankIndexInput = document.getElementById("rename-file-bank-index");
    bankIndexInput.value = parseInt(bankIndexString);
}
