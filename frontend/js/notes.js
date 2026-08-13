const notesGrid =
    document.querySelector("#notes-grid");

const notesSearch =
    document.querySelector("#notes-search");

const notesProjectFilter =
    document.querySelector("#notes-project-filter");

const newNoteButton =
    document.querySelector("#new-note-btn");

const noteModal =
    document.querySelector("#note-modal");

const closeNoteModal =
    document.querySelector("#close-note-modal");

const cancelNote =
    document.querySelector("#cancel-note");

const noteForm =
    document.querySelector("#note-form");

const noteTitle =
    document.querySelector("#note-title");

const noteContent =
    document.querySelector("#note-content");

const noteProject =
    document.querySelector("#note-project");



/*
|--------------------------------------------------------------------------
| Project Options
|--------------------------------------------------------------------------
*/

function renderProjectOptions() {

    notesProjectFilter.innerHTML = `
        <option value="all">
            All Projects
        </option>
    `;

    noteProject.innerHTML = `
        <option value="">
            Select project
        </option>
    `;


    projects.forEach((project) => {

        notesProjectFilter.innerHTML += `
            <option value="${project.name}">
                ${project.name}
            </option>
        `;

        noteProject.innerHTML += `
            <option value="${project.name}">
                ${project.name}
            </option>
        `;

    });

}



/*
|--------------------------------------------------------------------------
| Render Notes
|--------------------------------------------------------------------------
*/

function renderNotes(noteList) {

    notesGrid.innerHTML = "";


    if (noteList.length === 0) {

        notesGrid.innerHTML = `
            <div class="empty-state">

                <h3>
                    No notes found
                </h3>

                <p>
                    Create a note or change your search.
                </p>

            </div>
        `;

        return;
    }


    noteList.forEach((note) => {

        const card =
            document.createElement("article");

        card.className =
            "note-card";


        card.innerHTML = `

            <div class="note-card-header">

                <h2>
                    ${note.title}
                </h2>

                <button
                    class="note-menu"
                    type="button"
                    data-note-id="${note.id}"
                >
                    ⋮
                </button>

            </div>


            <p>
                ${note.content}
            </p>


            <span class="note-project">
                ${note.project}
            </span>


            <div class="note-footer">

                <span>
                    ${note.updated}
                </span>

                <span>
                    Note
                </span>

            </div>

        `;


        notesGrid.appendChild(card);

    });

}



/*
|--------------------------------------------------------------------------
| Filter Notes
|--------------------------------------------------------------------------
*/

function filterNotes() {

    const searchTerm =
        notesSearch.value
            .trim()
            .toLowerCase();


    const selectedProject =
        notesProjectFilter.value;


    const filteredNotes =
        notes.filter((note) => {

            const matchesSearch =
                note.title
                    .toLowerCase()
                    .includes(searchTerm)

                ||

                note.content
                    .toLowerCase()
                    .includes(searchTerm);


            const matchesProject =
                selectedProject === "all"

                ||

                note.project === selectedProject;


            return (
                matchesSearch &&
                matchesProject
            );

        });


    renderNotes(filteredNotes);

}



/*
|--------------------------------------------------------------------------
| Open Modal
|--------------------------------------------------------------------------
*/

function openNoteModal() {

    noteModal.classList.add("active");

    noteTitle.focus();

}



/*
|--------------------------------------------------------------------------
| Close Modal
|--------------------------------------------------------------------------
*/

function closeNoteModalWindow() {

    noteModal.classList.remove("active");

    noteForm.reset();

}



/*
|--------------------------------------------------------------------------
| Create Note
|--------------------------------------------------------------------------
*/

newNoteButton.addEventListener(
    "click",
    openNoteModal
);


closeNoteModal.addEventListener(
    "click",
    closeNoteModalWindow
);


cancelNote.addEventListener(
    "click",
    closeNoteModalWindow
);


noteModal.addEventListener(
    "click",
    (event) => {

        if (event.target === noteModal) {

            closeNoteModalWindow();

        }

    }
);



noteForm.addEventListener(
    "submit",
    (event) => {

        event.preventDefault();


        const title =
            noteTitle.value.trim();


        const content =
            noteContent.value.trim();


        const project =
            noteProject.value;


        if (
            !title ||
            !content ||
            !project
        ) {

            return;

        }


        const newNote = {

            id: Date.now(),

            title,

            content,

            project,

            createdAt: Date.now(),

            updated: "Just now",

        };


        notes.unshift(newNote);


        saveNotes();


        closeNoteModalWindow();


        filterNotes();

    }
);



/*
|--------------------------------------------------------------------------
| Edit Note
|--------------------------------------------------------------------------
*/

function editNote(noteId) {

    const note =
        notes.find(
            (item) =>
                item.id === noteId
        );


    if (!note) {

        return;

    }


    const newTitle =
        prompt(
            "Note title:",
            note.title
        );


    if (newTitle === null) {

        return;

    }


    const trimmedTitle =
        newTitle.trim();


    if (!trimmedTitle) {

        return;

    }


    const newContent =
        prompt(
            "Note content:",
            note.content
        );


    if (newContent === null) {

        return;

    }


    const trimmedContent =
        newContent.trim();


    if (!trimmedContent) {

        return;

    }


    note.title =
        trimmedTitle;


    note.content =
        trimmedContent;


    note.updated =
        "Just now";


    saveNotes();


    filterNotes();

}



/*
|--------------------------------------------------------------------------
| Delete Note
|--------------------------------------------------------------------------
*/

function deleteNote(noteId) {

    const noteIndex =
        notes.findIndex(
            (item) =>
                item.id === noteId
        );


    if (noteIndex === -1) {

        return;

    }


    const note =
        notes[noteIndex];


    const confirmed =
        confirm(
            `Delete "${note.title}"?`
        );


    if (!confirmed) {

        return;

    }


    notes.splice(
        noteIndex,
        1
    );


    saveNotes();


    filterNotes();

}



/*
|--------------------------------------------------------------------------
| Three-Dot Menu
|--------------------------------------------------------------------------
*/

notesGrid.addEventListener(
    "click",
    (event) => {

        const menuButton =
            event.target.closest(
                ".note-menu"
            );


        if (!menuButton) {

            return;

        }


        const noteId =
            Number(
                menuButton.dataset.noteId
            );


        const action =
            prompt(
                "Type 'edit' to edit or 'delete' to delete:"
            );


        if (!action) {

            return;

        }


        const normalizedAction =
            action
                .trim()
                .toLowerCase();


        if (
            normalizedAction === "edit"
        ) {

            editNote(noteId);

        }


        if (
            normalizedAction === "delete"
        ) {

            deleteNote(noteId);

        }

    }
);



/*
|--------------------------------------------------------------------------
| Search / Filter Events
|--------------------------------------------------------------------------
*/

notesSearch.addEventListener(
    "input",
    filterNotes
);


notesProjectFilter.addEventListener(
    "change",
    filterNotes
);



/*
|--------------------------------------------------------------------------
| Initial Render
|--------------------------------------------------------------------------
*/

renderProjectOptions();

filterNotes();