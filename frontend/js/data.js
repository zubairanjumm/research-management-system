const projects = [
    {
        id: 1,
        name: "Web Development",
        symbol: "WD",
        description:
            "Learning modern web development and building practical projects.",
        resources: 18,
        notes: 7,
        progress: 80,
        status: "active",
        updated: "Updated today",
    },
    {
        id: 2,
        name: "Database Research",
        symbol: "DB",
        description:
            "Exploring relational databases, indexing, and query optimization.",
        resources: 12,
        notes: 4,
        progress: 50,
        status: "active",
        updated: "Updated yesterday",
    },
    {
        id: 3,
        name: "System Design",
        symbol: "SD",
        description:
            "Studying scalable systems, APIs, caching, and architecture.",
        resources: 24,
        notes: 11,
        progress: 65,
        status: "active",
        updated: "Updated 3 days ago",
    },
    {
        id: 4,
        name: "Operating Systems",
        symbol: "OS",
        description:
            "Notes and resources about processes, memory, and operating systems.",
        resources: 9,
        notes: 3,
        progress: 35,
        status: "active",
        updated: "Updated last week",
    },
];


const resources = [
    {
        id: 1,
        title: "Understanding Database Indexes",
        description: "Database optimization reference",
        type: "PDF",
        project: "Database Research",
        added: "Today",
        createdAt: Date.now() - 1000,
    },
    {
        id: 2,
        title: "Modern JavaScript Guide",
        description: "JavaScript language reference",
        type: "Website",
        project: "Web Development",
        added: "Yesterday",
        createdAt: Date.now() - 2000,
    },
    {
        id: 3,
        title: "System Design Fundamentals",
        description: "Introduction to scalable architecture",
        type: "PDF",
        project: "System Design",
        added: "3 days ago",
        createdAt: Date.now() - 3000,
    },
    {
        id: 4,
        title: "MDN Web Documentation",
        description: "Web development documentation",
        type: "Website",
        project: "Web Development",
        added: "Last week",
        createdAt: Date.now() - 4000,
    },
    {
        id: 5,
        title: "Designing Data-Intensive Applications",
        description: "Distributed systems and databases",
        type: "Book",
        project: "Database Research",
        added: "Last week",
        createdAt: Date.now() - 5000,
    },
];


const notes = [
    {
        id: 1,
        title: "Database Indexing",
        content:
            "Indexes improve query performance by allowing the database to find rows without scanning the entire table.",
        project: "Database Research",
        createdAt: Date.now() - 1000,
        updated: "Today",
    },
    {
        id: 2,
        title: "API Design Principles",
        content:
            "Keep APIs predictable, consistent, and easy for clients to consume.",
        project: "System Design",
        createdAt: Date.now() - 2000,
        updated: "Yesterday",
    },
    {
        id: 3,
        title: "JavaScript DOM",
        content:
            "The DOM represents the HTML document as a tree of objects that JavaScript can read and modify.",
        project: "Web Development",
        createdAt: Date.now() - 3000,
        updated: "3 days ago",
    },
];


const bookmarks = [
    {
        id: 1,
        title: "MDN Web Docs",
        url: "https://developer.mozilla.org/",
        description: "Web development documentation.",
        project: "Web Development",
        createdAt: Date.now() - 1000,
    },
    {
        id: 2,
        title: "PostgreSQL Documentation",
        url: "https://www.postgresql.org/docs/",
        description: "Official PostgreSQL documentation.",
        project: "Database Research",
        createdAt: Date.now() - 2000,
    },
    {
        id: 3,
        title: "Git Documentation",
        url: "https://git-scm.com/doc",
        description: "Official Git documentation.",
        project: "System Design",
        createdAt: Date.now() - 3000,
    },
];


function loadSavedData() {

    const savedProjects =
        localStorage.getItem("researchhub_projects");

    const savedResources =
        localStorage.getItem("researchhub_resources");

    const savedNotes =
        localStorage.getItem("researchhub_notes");

    const savedBookmarks =
        localStorage.getItem("researchhub_bookmarks");


    if (savedProjects) {

        const parsedProjects =
            JSON.parse(savedProjects);

        projects.splice(
            0,
            projects.length,
            ...parsedProjects
        );
    }


    if (savedResources) {

        const parsedResources =
            JSON.parse(savedResources);

        resources.splice(
            0,
            resources.length,
            ...parsedResources
        );
    }


    if (savedNotes) {

        const parsedNotes =
            JSON.parse(savedNotes);

        notes.splice(
            0,
            notes.length,
            ...parsedNotes
        );
    }


    if (savedBookmarks) {

        const parsedBookmarks =
            JSON.parse(savedBookmarks);

        bookmarks.splice(
            0,
            bookmarks.length,
            ...parsedBookmarks
        );
    }
}


function saveProjects() {

    localStorage.setItem(
        "researchhub_projects",
        JSON.stringify(projects)
    );
}


function saveResources() {

    localStorage.setItem(
        "researchhub_resources",
        JSON.stringify(resources)
    );
}


function saveNotes() {

    localStorage.setItem(
        "researchhub_notes",
        JSON.stringify(notes)
    );
}


function saveBookmarks() {

    localStorage.setItem(
        "researchhub_bookmarks",
        JSON.stringify(bookmarks)
    );
}


loadSavedData();