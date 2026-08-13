const bookmarksGrid =
    document.querySelector("#bookmarks-grid");

const bookmarksSearch =
    document.querySelector("#bookmarks-search");

const bookmarksProjectFilter =
    document.querySelector("#bookmarks-project-filter");

const newBookmarkButton =
    document.querySelector("#new-bookmark-btn");

const bookmarkModal =
    document.querySelector("#bookmark-modal");

const closeBookmarkModal =
    document.querySelector("#close-bookmark-modal");

const cancelBookmark =
    document.querySelector("#cancel-bookmark");

const bookmarkForm =
    document.querySelector("#bookmark-form");

const bookmarkTitle =
    document.querySelector("#bookmark-title");

const bookmarkUrl =
    document.querySelector("#bookmark-url");

const bookmarkDescription =
    document.querySelector("#bookmark-description");

const bookmarkProject =
    document.querySelector("#bookmark-project");


function renderProjectOptions() {

    bookmarksProjectFilter.innerHTML = `
        <option value="all">
            All Projects
        </option>
    `;


    bookmarkProject.innerHTML = `
        <option value="">
            Select project
        </option>
    `;


    projects.forEach((project) => {

        bookmarksProjectFilter.innerHTML += `
            <option value="${project.name}">
                ${project.name}
            </option>
        `;


        bookmarkProject.innerHTML += `
            <option value="${project.name}">
                ${project.name}
            </option>
        `;

    });

}


function renderBookmarks(bookmarkList) {

    bookmarksGrid.innerHTML = "";


    if (bookmarkList.length === 0) {

        bookmarksGrid.innerHTML = `
            <div class="empty-state">

                <h3>
                    No bookmarks found
                </h3>

                <p>
                    Add a bookmark or change your search.
                </p>

            </div>
        `;

        return;
    }


    bookmarkList.forEach((bookmark) => {

        const card =
            document.createElement("article");

        card.className =
            "bookmark-card";


        card.innerHTML = `

            <div class="bookmark-card-header">

                <h2>
                    ${bookmark.title}
                </h2>

                <button
                    class="bookmark-menu"
                    type="button"
                    data-bookmark-id="${bookmark.id}"
                >
                    ⋮
                </button>

            </div>


            <p>
                ${bookmark.description}
            </p>


            <a
                class="bookmark-url"
                href="${bookmark.url}"
                target="_blank"
                rel="noopener noreferrer"
            >
                ${bookmark.url}
            </a>


            <span class="bookmark-project">
                ${bookmark.project}
            </span>


            <div class="bookmark-footer">

                <span>
                    Saved bookmark
                </span>

                <a
                    href="${bookmark.url}"
                    target="_blank"
                    rel="noopener noreferrer"
                >
                    Open →
                </a>

            </div>

        `;


        bookmarksGrid.appendChild(card);

    });

}


function filterBookmarks() {

    const searchTerm =
        bookmarksSearch.value
            .trim()
            .toLowerCase();


    const selectedProject =
        bookmarksProjectFilter.value;


    const filteredBookmarks =
        bookmarks.filter((bookmark) => {

            const matchesSearch =
                bookmark.title
                    .toLowerCase()
                    .includes(searchTerm)

                ||

                bookmark.description
                    .toLowerCase()
                    .includes(searchTerm)

                ||

                bookmark.url
                    .toLowerCase()
                    .includes(searchTerm);


            const matchesProject =
                selectedProject === "all"

                ||

                bookmark.project === selectedProject;


            return (
                matchesSearch &&
                matchesProject
            );

        });


    renderBookmarks(filteredBookmarks);

}


function openBookmarkModal() {

    bookmarkModal.classList.add("active");

    bookmarkTitle.focus();

}


function closeBookmarkModalWindow() {

    bookmarkModal.classList.remove("active");

    bookmarkForm.reset();

}


newBookmarkButton.addEventListener(
    "click",
    openBookmarkModal
);


closeBookmarkModal.addEventListener(
    "click",
    closeBookmarkModalWindow
);


cancelBookmark.addEventListener(
    "click",
    closeBookmarkModalWindow
);


bookmarkModal.addEventListener(
    "click",
    (event) => {

        if (event.target === bookmarkModal) {

            closeBookmarkModalWindow();

        }

    }
);


bookmarkForm.addEventListener(
    "submit",
    (event) => {

        event.preventDefault();


        const title =
            bookmarkTitle.value.trim();


        const url =
            bookmarkUrl.value.trim();


        const description =
            bookmarkDescription.value.trim();


        const project =
            bookmarkProject.value;


        if (
            !title ||
            !url ||
            !description ||
            !project
        ) {

            return;

        }


        const newBookmark = {

            id: Date.now(),

            title,

            url,

            description,

            project,

            createdAt: Date.now(),

        };


        bookmarks.unshift(
            newBookmark
        );


        saveBookmarks();


        closeBookmarkModalWindow();


        filterBookmarks();

    }
);


bookmarksSearch.addEventListener(
    "input",
    filterBookmarks
);


bookmarksProjectFilter.addEventListener(
    "change",
    filterBookmarks
);


renderProjectOptions();

filterBookmarks();