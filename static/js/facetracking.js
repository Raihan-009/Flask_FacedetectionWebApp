const content = document.querySelector(".content");
console.log(content)
const stopButton = document.querySelector(".stpbtn");
stopButton.addEventListener('click', ()=>{
    console.log("Clicked")
    content.classList.add("active");
})