let streaming = document.getElementById("streaming");
let liveStreaming = document.getElementById("videoStreaming");
liveStreaming.style.display = "none";

const stopButton = document.querySelector(".stpbtn");
const strtButton = document.querySelector(".strtbtn");

stopButton.addEventListener('click', ()=>{
    console.log("stopped")
    liveStreaming.style.display = "none";
    streaming.style.display = "block";
})

strtButton.addEventListener('click', ()=>{
    console.log("started");
    streaming.style.display = "none";
    liveStreaming.style.display = "flex";
})