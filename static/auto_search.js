
const input_field = document.getElementById("search")
const form = document.querySelector("form")
const result = document.getElementById("result")

input_field.addEventListener("input", submit_form);
function submit_form() {
    fetch("/result?search=" + input_field.value) 
    .then(response => {
        return response.text()
    })
    .then(html => {
        result.innerHTML = html
    })
}

form.onsubmit = function(event){
    event.preventDefault();      
    fetch("/result?search=" + input_field.value) 
    .then(response => {
        return response.text()
    })
    .then(html => {
        result.innerHTML = html
    })
}