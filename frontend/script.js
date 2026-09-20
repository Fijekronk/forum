function loadPosts() {
    fetch("http://localhost:8000/posts")
        .then(response => response.json())
        .then(data => {
            renderPost(data);
        });
};

function renderPost(posts) {
    const container = document.getElementById("posts");
    container.innerHTML = "";
    posts.forEach(post => {
        const div = document.createElement("div");
        const postTitle = document.createElement("h3");
        postTitle.textContent = post.title;
        const postContent = document.createElement("p");
        postContent.textContent = post.content; 
        div.className = "post";
        div.appendChild(postTitle);
        div.appendChild(postContent);
        container.appendChild(div);
    });
};

const postContainer = document.getElementById("posts");

if(postContainer) {
    loadPosts();
}


const loginForm = document.getElementById("loginForm")
if (loginForm) {
    loginForm.addEventListener("submit", function(e) {
        e.preventDefault();
        const username = document.getElementById("username").value;
        const password = document.getElementById("password").value;

        fetch("http://localhost:8000/login", {
            method: "POST",
            headers: {"Content-Type": "Application/json"},
            body: JSON.stringify({username, password})
        })
        .then(response => {
            if(response.status==401) {
                document.getElementById("loginMessage").innerText = "Invalid password or username";
                throw new Error("Invalid credentials");
            }
            return response.json()
        })
        .then(data => {
            if (data.token) {
                localStorage.setItem("token", data.token);
                window.location.href = "index.html";
            }
        })
        .catch(error => console.log(error));
    });
}
const createForm = document.getElementById("postForm");

if (createForm) {
    createForm.addEventListener("submit", function(e) {
        e.preventDefault();

        const title = document.getElementById("postTitle").value;
        const content = document.getElementById("postContent").value;

        fetch("http://localhost:8000/posts", {
            method: "POST",
            headers: {
                "Content-Type": "Application/json",
                "Authorization": localStorage.getItem("token")
            },
            body: JSON.stringify({title: title, content: content})       
        })
        .then(response => {
            if (response.status === 401) {
                document.getElementById("createMessage").innerText = "You need to authenticate";
                throw new Error("Not Authenticated");
            }
            return response.json()
        })
        .then(data => {
            window.location.href = "index.html";
        })
        .catch(error => console.log(error));
    });
}

const registerForm = document.getElementById("registerForm");
if(registerForm) {    
    registerForm.addEventListener("submit", function(e) {
        e.preventDefault();
        const username = document.getElementById("username").value;
        const password = document.getElementById("password").value;

        fetch("http://localhost:8000/register", {
            method: "POST",
            headers: {"Content-Type": "Application/json"},
            body: JSON.stringify({username, password})
        })
        .then(response => {
            if(response.status==409) {
                document.getElementById("registerMessage").innerText = "This username already exists";
                throw new Error("Username is taken");
            }
            return response.json()
        })
        .then(data => {
            window.location.href = "login.html";
        })
        .catch(error => console.log(error));
    });
}