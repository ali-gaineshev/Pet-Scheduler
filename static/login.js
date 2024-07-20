console.log("test")

document.getElementById("loginForm").addEventListener("submit", async function (event) {
    event.preventDefault();
    const email = document.getElementById("inputEmail").value;
    const password = document.getElementById("inputPassword").value;
    if (!email || !password) {
        alert("Please enter a valid information");
    }

    const response = await fetch("/api/validateLogin", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify({ email, password })
    });
    const result = await response.json();
    if(result.ok === undefined || result.body === undefined){
        window.location.replace()
    }
      result.ok === false  || result.body.message === undefined || result.body.message === "error" || result.body.error_message !== undefined
    ) {
        alert(result.body.error_message);
    }
    console.log(result);
})