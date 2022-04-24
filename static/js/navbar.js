function navbar(){
    var checkbtn = document.querySelector("#check");
    if (checkbtn.checked){
        console.log("clicked added");
        const menubar = document.querySelector(".dropdown");
        menubar.classList.add("responsive");
    }else{
        console.log("clicked removed");
        const menubar = document.querySelector(".dropdown");
        menubar.classList.remove("responsive");
    }
}