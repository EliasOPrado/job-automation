
/* 
 ---- Load more functionality ----
*/
let cardContainer = document.getElementsByClassName("minor-left-container");
let loadMoreButton = document.getElementById("load-more-button");
let allCards = document.querySelectorAll("job-list-card");


let nthChildValue = 4;
const styleElement = document.createElement("style");
document.head.appendChild(styleElement);

// Function to update the nth-child rule
function updateNthChild() {
    styleElement.textContent = `
    .job-list-card:nth-child(n+${nthChildValue}) { display: none; }
    .minor-left-container {
        overflow-y: scroll;
        height: 99vh;
        }
    `;
}

/*
 ---- Function to increase the nth-child value ----
*/ 
function increaseNthChild() {
    nthChildValue += 3; 
    updateNthChild();
}


updateNthChild();

/*
 ---- Add event listener for the button to increase the nth-child value ----
*/ 
if (loadMoreButton){
    loadMoreButton.addEventListener('click', increaseNthChild);
}

/*  
 --- delete message after N seconds ---
*/ 
setTimeout(function() {
    let delete_messages = document.getElementsByClassName("message-container");
    for (let i = 0; i < delete_messages.length; i++) {
        delete_messages[i].style.display = "none"; // Hide each element
    }
}, 3000);


/*
 ---- Modal/Pop-Up Functionality ----
*/
let modal = document.getElementById("modal");
let overlay = document.getElementById("overlay");
let modalButton = document.getElementById("open-modal");
let closeButton = document.getElementById("close-modal");

modalButton.onclick = function() {
    modal.style.display = "flex";
    overlay.style.display = "block";
};

// Close modal when clicking on the "X" button
closeButton.onclick = function() {
    modal.style.display = "none";
    overlay.style.display = "none";
};
// Close modal when clicking outside the modal
overlay.onclick = function() {
    modal.style.display = "none";
    overlay.style.display = "none";
};