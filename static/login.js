

document.getElementById("loginForm").addEventListener("submit", async function (event) {
    event.preventDefault();
    const email = document.getElementById("inputEmail").value;
    const password = document.getElementById("inputPassword").value;

    if (!email || !password) {
        alert("Please enter valid information");
        return;
    }

    const data = {
        email: email,
        password: password
    };


    const response = await fetch("/api/validateLogin", {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(data)
    }).then(rawResponse => {
        return rawResponse.json();  // Return the parsed JSON
    }).then(data => {
        return data  // Log the parsed JSON data
    }).catch(error => {
        console.error('Error:', error);  // This will log any error that occurs during the fetch
    });
    handleResponseError(response)
    console.log(response);
});


function handleResponseError(response) {
    const errorMessageElement = document.getElementById("errorMessage");
    if (response.error_message) {
        errorMessageElement.innerText = response.error_message;
    } else {
        errorMessageElement.innerText = "An unexpected error occurred. Please try again later.";
    }
}