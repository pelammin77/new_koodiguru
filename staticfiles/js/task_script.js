let editor;
let taskId;
let taskLanguage;

document.addEventListener('DOMContentLoaded', (event) => {
    var taskData = document.getElementById('task-data');
    taskId = taskData.dataset.taskId;
    taskLanguage = taskData.dataset.taskLanguage;
    console.log("Task Language: ", taskLanguage);

    var themeToUse = localStorage.getItem('selectedTheme') || 'default';
        editor = CodeMirror.fromTextArea(document.getElementById("code-editor"), {
        mode: taskLanguage,
        extraKeys: {
                "Ctrl-Space": "autocomplete"
            },
        lineNumbers: true,
        styleActiveLine: true,
        gutters: ["breakpoints", "CodeMirror-linenumbers"],
        autoCloseBrackets: true
        });
    editor.setSize("100%", "550px");
    editor.setOption('theme', themeToUse);
    document.getElementById('theme-selector').value = themeToUse;
});


document.getElementById('theme-selector').addEventListener('change', function() {
    var selectedTheme = this.value;
    editor.setOption("theme", selectedTheme);
    // Tallenna valittu teema localStorage-muistiin
    localStorage.setItem('selectedTheme', selectedTheme);
    
    // Lähetä AJAX-pyyntö Djangolle tallentaaksesi teeman
    $.ajax({
        url: '/save_editor_theme/',  // vaihda tarvittaessa oikeaan URL-osoitteeseen
        type: 'post',
        headers: {'X-CSRFToken': getCookie('csrftoken')},
        data: {
            'theme': selectedTheme
        },
        success: function(response){
            if(response.status === 'success') {
                console.log('Teema tallennettu onnistuneesti.');
            } else {
                console.error('Virhe tallennettaessa teemaa:', response.message);
            }
        }
    });
});

  function saveSuccesCode(code) {
$.ajax({
  url: '/save-code/',  // change this to your save code endpoint
  type: 'post',
  headers: {'X-CSRFToken': getCookie('csrftoken')},
  data: {
      'code': code,
      'task_id': taskId
  },
}).done(function() {
  Swal.fire(
      'Onneksi olkoon!',
      'Koodisi tuotti oikean tuloksen ja se tallenettiin.',
      'success'
  ).then((result) => {
      if (result.isConfirmed) {
         
          window.location.href = '/tasks/' + taskId + '/review/';

      }
  });
}).fail(function() {
  // Voit lisätä käsittelyn epäonnistuneille pyynnöille tässä
});
}





  
// Muut koodit pysyvät samana kuin aikaisemmin.

document.getElementById('run-code-button').addEventListener('click', function() {
   alert("Aja");
    var code = editor.getValue();
    editor.clearGutter('breakpoints');

    fetch('/run-code/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: 'code=' + encodeURIComponent(code) + '&language=' + encodeURIComponent(taskLanguage)
    })
    .then(response => response.json())
    .then(data => {
        var consoleElement = document.getElementById('consoleElement');

        if (data.error) {
            let errorMessage = data.error;
            console.log(errorMessage)
            consoleElement.innerHTML = errorMessage.replace(/\n/g, '<br>');
            console.log("consoleElement.innerHTML:", consoleElement.innerHTML);


            if (errorMessage.includes("TestFailed:")) {  // Oletetaan että testien epäonnistumisessa palautetaan viesti, joka sisältää "TestFailed:"
                Swal.fire(
                    'Hups!',
                    'Yksi tai useampi testi epäonnistui. Tarkista koodisi.',
                    'error'
                );
            } else {
                let lineNumber = parseInt(errorMessage.split("line ")[1]);
                if (isNaN(lineNumber)) {
                    lineNumber = 0; // Oletusarvo, jos riviä ei määritelty
                }
                consoleElement.style.color = 'red';
                editor.setGutterMarker(lineNumber - 1, 'breakpoints', makeMarker(errorMessage));

                Swal.fire(
                    'Hups!',
                    'Koodissasi on virhe. Yritä uudelleen.',
                    'error'
                );
            }
        } else {
            // Koska tulosteen tarkistus on poistettu, oletamme että jos ei ole virhettä, koodi on oikein.
            updateTaskStatus('solved');
            saveSuccesCode(code);
        }
    });
});

function updateTaskStatus(status) {

      var url = status === 'started' ? '/update-task-status-started/' : '/update-task-status-solved/';
      $.ajax({
          url: url,
          method: 'POST',
          headers: {
              'X-CSRFToken': getCookie('csrftoken')
          },
          data: {
              task_id: taskId
          },
          success: function(data) {
              console.log(data.message);
            
          },
          error: function(data) {
             alert("'Error updating task status'")
              console.log('Error updating task status');
          }
      });
  }
  function getCookie(name) {
      var cookieValue = null;
      if (document.cookie && document.cookie !== '') {
          var cookies = document.cookie.split(';');
          for (var i = 0; i < cookies.length; i++) {
              var cookie = cookies[i].trim();
              if (cookie.substring(0, name.length + 1) === (name + '=')) {
                  cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                  break;
              }
          }
      }
      return cookieValue;
  }


document.getElementById('save-code-button').addEventListener('click', function() {
var code = editor.getValue();
$.ajax({
  url: '/save-code/',  // change this to your save code endpoint
  type: 'post',
  headers: {'X-CSRFToken': getCookie('csrftoken')},
  data: {
      'code': code,
      'task_id': taskId
  },
  success: function(response){
      Swal.fire(
          'Koodisi tallenettu', 
          '',  
          'success'
      )
  }
});
});

// Lisää tämä kohta olemassa olevan "run-code-button" kuuntelijan alapuolelle.
document.getElementById('console-run-code-button').addEventListener('click', function() {
    var code = editor.getValue();
    editor.clearGutter('breakpoints');

    fetch('/run-code/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: 'code=' + encodeURIComponent(code) + '&language=' + encodeURIComponent(taskLanguage)
    })
    .then(response => response.json())
    .then(data => {
        var consoleElement = document.getElementById('consoleElement');

        if (data.error) {
            let errorMessage = data.error;
            consoleElement.innerHTML = errorMessage;

            if (errorMessage.includes("TestFailed:")) {
                Swal.fire(
                    'Hups!',
                    'Yksi tai useampi testi epäonnistui. Tarkista koodisi.',
                    'error'
                );
            } else {
                let lineNumber = parseInt(errorMessage.split("line ")[1]);
                if (isNaN(lineNumber)) {
                    lineNumber = 0;
                }
                consoleElement.style.color = 'red';
                editor.setGutterMarker(lineNumber - 1, 'breakpoints', makeMarker(errorMessage));

                Swal.fire(
                    'Hups!',
                    'Koodissasi on virhe. Yritä uudelleen.',
                    'error'
                );
            }
        } else {
            updateTaskStatus('solved');
            saveSuccesCode(code);
        }
    });
});

// Lisää tämä kohta olemassa olevan "save-code-button" kuuntelijan alapuolelle.
document.getElementById('console-save-code-button').addEventListener('click', function() {
    var code = editor.getValue();
    $.ajax({
      url: '/save-code/',  // change this to your save code endpoint
      type: 'post',
      headers: {'X-CSRFToken': getCookie('csrftoken')},
      data: {
          'code': code,
          'task_id': taskId 
      },
      success: function(response){
          Swal.fire(
              'Koodisi tallenettu', 
              '',  
              'success'
          )
      }
    });
});



function makeMarker(errorMessage) {
var marker = document.createElement("div");
marker.style.color = "#822";
marker.innerHTML = "●";
marker.title = errorMessage;
marker.style.fontSize = '30px'; 

return marker;
}
