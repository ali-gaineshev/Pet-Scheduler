console.log("test")

document.getElementById("loginForm").addEventListener("submit", async function (event) {
    event.preventDefault();
    const email = document.getElementById("inputEmail").value;
    const password = document.getElementById("inputPassword").value;
    if (!email || !password) {
        alert("Please enter a valid information");
    }

    const response = await fetch("/validateLogin", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ email, password })
    });
    const result = await response.json();

    console.log(result);
})