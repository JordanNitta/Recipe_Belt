const togglePassword = document.getElementById("togglePassword")
togglePassword.addEventListener("click", toggleVisibility)

function toggleVisibility(){
    const passwordInput = document.getElementById("passwordVisibility")
    const icon = document.getElementById("icon")
    if (passwordInput.type === "password") {
        passwordInput.type = "text"
        icon.innerText = "visibility_off"
    } else {
        passwordInput.type = "password"
        icon.innerText = "visibility"
    }
}