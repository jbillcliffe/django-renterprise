function setActiveSideNav(id) {
    let sideBarButtons = document.getElementsByClassName('side-bar nav-link');

    for (let i = 0; i < sideBarButtons.length; i++) {
        if (sideBarButtons[i].href == id) {
            sideBarButtons[i].className = "side-bar nav-link active";
        } else {
            sideBarButtons[i].className = "side-bar nav-link";
        }
    }
}

$(document).ready(function() {
    setActiveSideNav(window.location.href);
});


