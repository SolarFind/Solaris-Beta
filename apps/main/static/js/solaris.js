function notifyMe() {
  // Проверка поддержки браузером уведомлений
  if (!("Notification" in window)) {
    console.log("This browser does not support desktop notification");
  }

  // Проверка разрешения на отправку уведомлений
  else if (Notification.permission === "granted") {
    // Если разрешено, то создаем уведомление
    var notification = new Notification("Hi there!");
  }

  // В противном случае, запрашиваем разрешение
  else if (Notification.permission !== 'denied') {
    Notification.requestPermission(function (permission) {
      // Если пользователь разрешил, то создаем уведомление 
      if (permission === "granted") {
        var notification = new Notification("Thanks for subscribe!");
      }
    });
  }

}

function SaySomething (smth) {
        var voices = speechSynthesis.getVoices();
        var utterance = new SpeechSynthesisUtterance(smth);
        utterance.voice = voices[1];
        speechSynthesis.speak(utterance);
    }

    console.log("Старту-у-ем! (Игорь Негода, 2018)");
    var recognizer = new webkitSpeechRecognition();
function RecognizeRU(){
    console.log("Кнопку нажимаем! Voice Recognition started.");
    // Создаем распознаватель
    // Ставим опцию, чтобы распознавание началось ещё до того, как пользователь закончит говорить
    recognizer.interimResults = true;

// Какой язык будем распознавать?
    recognizer.lang = 'ru-Ru';

// Используем колбек для обработки результатов
    recognizer.onresult = function (event) {
        var result = event.results[event.resultIndex];
        if (result.isFinal) {
            a = result[0].transcript;
            $("#search-input")[0].value=a;
            $("#search-button")[0].click();
        } else {
            console.log('Промежуточный результат: ', result[0].transcript);
        }
    };

// Начинаем слушать микрофон и распознавать голос
setTimeout(function(){
console.log("Поехали!")    
recognizer.start();}, 3000);

}


navigator.geolocation.getCurrentPosition(function(position) {
              lat = position.coords.latitude;
              long = position.coords.longitude;
              console.log("Latitude: "+lat);
              console.log("Longitude: "+long)
              document.cookie = "lat="+lat;
              document.cookie = "long="+long;

});



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
        try{
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
        };}catch (e) {
            
        }

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
    $("body").after('<link href="/static/css/glodark.css" rel="stylesheet">')
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

function pageres_preloader() {
var containerElement = document.getElementById("cnt");

var containerMonitor = scrollMonitor.createContainer(containerElement);
// this containerMonitor is an instance of the scroll monitor
// that listens to scroll events on your container.

var childElement = document.getElementById("results");
var elementWatcher = containerMonitor.create(childElement);

elementWatcher.enterViewport(function() {
    console.log( 'I have entered the viewport' );
});
elementWatcher.exitViewport(function() {
    console.log( 'I have left the viewport' );
});
}