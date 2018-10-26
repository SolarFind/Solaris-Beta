

function styped() {
    let typed = new Typed('#typed', {
        typeSpeed: 50,
        backSpeed: 40,
        strings: [
            "Find a new star!",
            "Find a new galaxy!",
            "Find a new life!",
            "Find a new hobbies!",
            "Find a new job!",
            "Find a new wife!",
            "Find a new adventure!",
            "Find a new car!",
            "Find a something cool!",],
        stringsElement: null,
        fadeOut: true,
        fadeOutClass: 'typed-fade-out',
        fadeOutDelay: 500,
        backDelay: 700,
    });
}
//Searcher script
function searchbox() {

    document.addEventListener('DOMContentLoaded', function () {
        var elems = document.querySelectorAll('.autocomplete');
        var instances = M.Autocomplete.init(elems, {
            data: {
                "Apple": null,
                "Microsoft": null,
                "Google": 'https://placehold.it/250x250'
            },
        });
        var instance = M.Autocomplete.getInstance(elems[0]);
        var y = $("#autocomplete-input")[0];
        console.log("y", y);
        y.oninput = function () {
            instance.open();
        };

    });
}

//ATTENTION TO BETA!
function betalarm() {
    if (localStorage["attention"]==null){
        var z = "false";} else {var z = localStorage["attention"]}

    if (z !== "true") {
        let timerInterval;
        swal({
            title: 'This site still in beta! Be careful!',
            html: 'Avoid the <bold>bugs</bold>',
            timer: 5000,
            onOpen: () => {
                swal.showLoading()
            },
            onClose: () => {
                clearInterval(timerInterval);
                 deferredPrompt.prompt();
  // Wait for the user to respond to the prompt
  deferredPrompt.userChoice
    .then((choiceResult) => {
      if (choiceResult.outcome === 'accepted') {
        console.log('User accepted the A2HS prompt');
      } else {
        console.log('User dismissed the A2HS prompt');
      }
      deferredPrompt = null;
    });
            }
        }).then((result) => {
            localStorage.setItem('attention', "true");
        })
    }
}
//THEME ENGINE!

function turn_moon() {
    localStorage.setItem('theme', 'dark');
    $("body").after('<link href="https://dangsun.github.io/SolarisUI/css/glodark.css" rel="stylesheet">')
}

function turn_day(){
    localStorage.setItem("theme", "light");
    location.reload();
}

if (localStorage["theme"]==="dark"){
    turn_moon();
}

let deferredPrompt;

window.addEventListener('beforeinstallprompt', (e) => {
  // Prevent Chrome 67 and earlier from automatically showing the prompt
  e.preventDefault();
  // Stash the event so it can be triggered later.
  deferredPrompt = e;
});
