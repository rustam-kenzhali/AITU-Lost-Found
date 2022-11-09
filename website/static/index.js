function deleteNote(noteId){
    fetch('/notes/delete-note', {
        method: 'POST',
        body: JSON.stringify({ noteId: noteId }),
    }).then((_res) => {
        window.location.href = "/notes";
        }
    );
}

function changeNote(noteId){
    fetch('/notes/change-note', {
        method: 'POST',
        body: JSON.stringify({ noteId: noteId }),
    }).then((_res) => {
        window.location.href = "/notes";
        }
    );
}