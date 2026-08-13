const projectsContainer =
    document.querySelector("#projects-container");

const projectSearch =
    document.querySelector("#project-search");

const projectFilter =
    document.querySelector("#project-filter");

const newProjectButton =
    document.querySelector("#new-project-btn");

const projectModal =
    document.querySelector("#project-modal");

const closeModalButton =
    document.querySelector("#close-modal-btn");

const cancelProjectButton =
    document.querySelector("#cancel-project-btn");

const projectForm =
    document.querySelector("#project-form");

const projectName =
    document.querySelector("#project-name");

const projectDescription =
    document.querySelector("#project-description");

const projectSymbol =
    document.querySelector("#project-symbol");



/*
|--------------------------------------------------------------------------
| Render Projects
|--------------------------------------------------------------------------
*/

function renderProjects(projectList) {

    projectsContainer.innerHTML = "";


    if (projectList.length === 0) {

        projectsContainer.innerHTML = `
            <div class="empty-state">

                <h3>No projects found</h3>

                <p>
                    Try changing your search or create a new project.
                </p>

            </div>
        `;

        return;
    }


    projectList.forEach((project) => {

        const card =
            document.createElement("article");

        card.className = "project-card";


        card.innerHTML = `

            <div class="project-card-header">

                <div class="project-symbol">
                    ${project.symbol}
                </div>


                <button
                    class="project-menu"
                    type="button"
                    data-project-id="${project.id}"
                >
                    ⋮
                </button>

            </div>


            <h2>
                ${project.name}
            </h2>


            <p>
                ${project.description}
            </p>


            <div class="project-meta">

                <span>
                    ${project.resources} resources
                </span>


                <span>
                    ${project.notes} notes
                </span>

            </div>


            <div class="project-progress">

                <div class="progress-info">

                    <span>
                        Progress
                    </span>


                    <span>
                        ${project.progress}%
                    </span>

                </div>


                <div class="progress">

                    <div
                        class="progress-bar"
                        style="width: ${project.progress}%"
                    ></div>

                </div>

            </div>


            <div class="project-card-footer">

                <span>
                    ${project.updated}
                </span>


                <a href="#">
                    Open →
                </a>

            </div>

        `;


        projectsContainer.appendChild(card);

    });

}



/*
|--------------------------------------------------------------------------
| Filter Projects
|--------------------------------------------------------------------------
*/

function filterProjects() {

    const searchTerm =
        projectSearch.value
            .trim()
            .toLowerCase();


    const selectedFilter =
        projectFilter.value;


    const filteredProjects =
        projects.filter((project) => {

            const matchesSearch =
                project.name
                    .toLowerCase()
                    .includes(searchTerm)

                ||

                project.description
                    .toLowerCase()
                    .includes(searchTerm);


            const matchesFilter =
                selectedFilter === "all"

                ||

                project.status === selectedFilter;


            return (
                matchesSearch &&
                matchesFilter
            );

        });


    renderProjects(filteredProjects);

}



/*
|--------------------------------------------------------------------------
| Open Modal
|--------------------------------------------------------------------------
*/

function openProjectModal() {

    projectModal.classList.add("active");

    projectName.focus();

}



/*
|--------------------------------------------------------------------------
| Close Modal
|--------------------------------------------------------------------------
*/

function closeProjectModal() {

    projectModal.classList.remove("active");

    projectForm.reset();

}



/*
|--------------------------------------------------------------------------
| Create Project
|--------------------------------------------------------------------------
*/

projectForm.addEventListener(
    "submit",
    (event) => {

        event.preventDefault();


        const name =
            projectName.value.trim();


        const description =
            projectDescription.value.trim();


        const symbol =
            projectSymbol.value
                .trim()
                .toUpperCase();


        if (
            !name ||
            !description ||
            !symbol
        ) {

            return;

        }


        const newProject = {

            id: Date.now(),

            name,

            symbol,

            description,

            resources: 0,

            notes: 0,

            progress: 0,

            status: "active",

            updated: "Just now",

        };


        projects.unshift(newProject);


        saveProjects();


        closeProjectModal();


        filterProjects();

    }
);



/*
|--------------------------------------------------------------------------
| Delete Project
|--------------------------------------------------------------------------
*/

function deleteProject(projectId) {

    const projectIndex =
        projects.findIndex(
            (project) =>
                project.id === projectId
        );


    if (projectIndex === -1) {

        return;

    }


    const project =
        projects[projectIndex];


    const confirmed =
        confirm(
            `Delete "${project.name}"?`
        );


    if (!confirmed) {

        return;

    }


    projects.splice(
        projectIndex,
        1
    );


    saveProjects();


    filterProjects();

}



/*
|--------------------------------------------------------------------------
| Edit Project
|--------------------------------------------------------------------------
*/

function editProject(projectId) {

    const project =
        projects.find(
            (project) =>
                project.id === projectId
        );


    if (!project) {

        return;

    }


    const newName =
        prompt(
            "Project name:",
            project.name
        );


    if (newName === null) {

        return;

    }


    const trimmedName =
        newName.trim();


    if (!trimmedName) {

        return;

    }


    const newDescription =
        prompt(
            "Project description:",
            project.description
        );


    if (newDescription === null) {

        return;

    }


    const trimmedDescription =
        newDescription.trim();


    if (!trimmedDescription) {

        return;

    }


    project.name =
        trimmedName;


    project.description =
        trimmedDescription;


    project.updated =
        "Just now";


    saveProjects();


    filterProjects();

}



/*
|--------------------------------------------------------------------------
| Project Menu
|--------------------------------------------------------------------------
*/

projectsContainer.addEventListener(
    "click",
    (event) => {

        const menuButton =
            event.target.closest(
                ".project-menu"
            );


        if (!menuButton) {

            return;

        }


        const projectId =
            Number(
                menuButton.dataset.projectId
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

            editProject(projectId);

        }


        if (
            normalizedAction === "delete"
        ) {

            deleteProject(projectId);

        }

    }
);



/*
|--------------------------------------------------------------------------
| Event Listeners
|--------------------------------------------------------------------------
*/

newProjectButton.addEventListener(
    "click",
    openProjectModal
);


closeModalButton.addEventListener(
    "click",
    closeProjectModal
);


cancelProjectButton.addEventListener(
    "click",
    closeProjectModal
);


projectModal.addEventListener(
    "click",
    (event) => {

        if (
            event.target === projectModal
        ) {

            closeProjectModal();

        }

    }
);


projectSearch.addEventListener(
    "input",
    filterProjects
);


projectFilter.addEventListener(
    "change",
    filterProjects
);



/*
|--------------------------------------------------------------------------
| Initial Render
|--------------------------------------------------------------------------
*/

filterProjects();