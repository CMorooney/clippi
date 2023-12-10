function init() {
    const sourceDropdown = document.querySelector('#source-form-source');
    sourceDropdown.addEventListener('change', uploadSourceChanged);
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