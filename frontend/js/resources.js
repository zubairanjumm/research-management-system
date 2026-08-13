const resourceTable =
    document.querySelector("#resource-table");

const resourceSearch =
    document.querySelector("#resource-search");

const resourceTypeFilter =
    document.querySelector("#resource-type-filter");

const resourceProjectFilter =
    document.querySelector("#resource-project-filter");

const resourceSort =
    document.querySelector("#resource-sort");

const resourceCount =
    document.querySelector("#resource-count");


const addResourceButton =
    document.querySelector("#add-resource-btn");

const resourceModal =
    document.querySelector("#resource-modal");

const closeResourceModal =
    document.querySelector("#close-resource-modal");

const cancelResourceButton =
    document.querySelector("#cancel-resource");

const resourceForm =
    document.querySelector("#resource-form");


const resourceTitle =
    document.querySelector("#resource-title");

const resourceDescription =
    document.querySelector("#resource-description");

const resourceType =
    document.querySelector("#resource-type");

const resourceProject =
    document.querySelector("#resource-project");


/* --------------------------------
   Render Project Options
-------------------------------- */

function renderProjectOptions() {

    resourceProjectFilter.innerHTML = `
        <option value="all">
            All Projects
        </option>
    `;


    resourceProject.innerHTML = `
        <option value="">
            Select project
        </option>
    `;


    projects.forEach((project) => {

        resourceProjectFilter.innerHTML += `
            <option value="${project.name}">
                ${project.name}
            </option>
        `;


        resourceProject.innerHTML += `
            <option value="${project.name}">
                ${project.name}
            </option>
        `;

    });

}


/* --------------------------------
   Render Resources
-------------------------------- */

function renderResources(resourceList) {

    resourceTable.innerHTML = "";


    resourceCount.textContent =
        `${resourceList.length} resource${resourceList.length === 1 ? "" : "s"}`;


    if (resourceList.length === 0) {

        resourceTable.innerHTML = `

            <div class="empty-state">

                <h3>
                    No resources found
                </h3>

                <p>
                    Try a different search or filter.
                </p>

            </div>

        `;

        return;

    }


    resourceTable.innerHTML = `

        <div class="resource-row resource-row-header">

            <div>
                Resource
            </div>

            <div>
                Type
            </div>

            <div>
                Project
            </div>

            <div>
                Added
            </div>

            <div>
            </div>

        </div>

    `;


    resourceList.forEach((resource) => {

        const row =
            document.createElement("div");


        row.className =
            "resource-row";


        const typeClass =
            resource.type.toLowerCase();


        row.innerHTML = `

            <div class="resource-title">

                <div
                    class="resource-type-icon ${typeClass}"
                >
                    ${resource.type === "Website" ? "WEB" : resource.type.toUpperCase()}
                </div>


                <div>

                    <h3>
                        ${resource.title}
                    </h3>

                    <p>
                        ${resource.description}
                    </p>

                </div>

            </div>


            <div>

                <span class="badge">
                    ${resource.type}
                </span>

            </div>


            <div>

                <span class="project-tag">
                    ${resource.project}
                </span>

            </div>


            <div class="resource-date">
                ${resource.added}
            </div>


            <button
                class="resource-menu"
                type="button"
                data-resource-id="${resource.id}"
            >
                ⋮
            </button>

        `;


        resourceTable.appendChild(row);

    });

}


/* --------------------------------
   Filter + Sort
-------------------------------- */

function filterResources() {

    const searchTerm =
        resourceSearch.value
            .trim()
            .toLowerCase();


    const selectedType =
        resourceTypeFilter.value;


    const selectedProject =
        resourceProjectFilter.value;


    const sortType =
        resourceSort.value;


    let filteredResources =
        resources.filter((resource) => {

            const matchesSearch =
                resource.title
                    .toLowerCase()
                    .includes(searchTerm)

                ||

                resource.description
                    .toLowerCase()
                    .includes(searchTerm);


            const matchesType =
                selectedType === "all"

                ||

                resource.type === selectedType;


            const matchesProject =
                selectedProject === "all"

                ||

                resource.project === selectedProject;


            return (
                matchesSearch &&
                matchesType &&
                matchesProject
            );

        });


    if (sortType === "newest") {

        filteredResources.sort(
            (a, b) =>
                b.createdAt - a.createdAt
        );

    }


    if (sortType === "oldest") {

        filteredResources.sort(
            (a, b) =>
                a.createdAt - b.createdAt
        );

    }


    if (sortType === "alphabetical") {

        filteredResources.sort(
            (a, b) =>
                a.title.localeCompare(b.title)
        );

    }


    renderResources(filteredResources);

}


/* --------------------------------
   Modal
-------------------------------- */

function openResourceModal() {

    resourceModal.classList.add("active");

    resourceTitle.focus();

}


function closeResourceModalWindow() {

    resourceModal.classList.remove("active");

    resourceForm.reset();

}


addResourceButton.addEventListener(
    "click",
    openResourceModal
);


closeResourceModal.addEventListener(
    "click",
    closeResourceModalWindow
);


cancelResourceButton.addEventListener(
    "click",
    closeResourceModalWindow
);


resourceModal.addEventListener(
    "click",
    (event) => {

        if (event.target === resourceModal) {

            closeResourceModalWindow();

        }

    }
);


/* --------------------------------
   Add Resource
-------------------------------- */

resourceForm.addEventListener(
    "submit",
    (event) => {

        event.preventDefault();


        const title =
            resourceTitle.value.trim();


        const description =
            resourceDescription.value.trim();


        const type =
            resourceType.value;


        const project =
            resourceProject.value;


        if (
            !title ||
            !description ||
            !type ||
            !project
        ) {

            return;

        }


        const newResource = {

            id: Date.now(),

            title,

            description,

            type,

            project,

            added: "Just now",

            createdAt: Date.now(),

        };


        resources.unshift(
            newResource
        );


        saveResources();


        closeResourceModalWindow();


        filterResources();

    }
);


/* --------------------------------
   Events
-------------------------------- */

resourceSearch.addEventListener(
    "input",
    filterResources
);


resourceTypeFilter.addEventListener(
    "change",
    filterResources
);


resourceProjectFilter.addEventListener(
    "change",
    filterResources
);


resourceSort.addEventListener(
    "change",
    filterResources
);


/* --------------------------------
   Initial Load
-------------------------------- */

renderProjectOptions();

filterResources();