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


function openNoteModal() {

    noteModal.classList.add("active");

    noteTitle.focus();

}


function closeNoteModalWindow() {

    noteModal.classList.remove("active");

    noteForm.reset();

}


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


notesSearch.addEventListener(
    "input",
    filterNotes
);


notesProjectFilter.addEventListener(
    "change",
    filterNotes
);


renderProjectOptions();

filterNotes();