
// Load more functionality
let cardContainer = document.getElementsByClassName("minor-left-container");
let loadMoreButton = document.getElementById("load-more-button");
let allCards = document.querySelectorAll("job-list-card");


let nthChildValue = 4;
const styleElement = document.createElement("style");
document.head.appendChild(styleElement);

// Function to update the nth-child rule
function updateNthChild() {
    styleElement.textContent = `
    .minor-left-container {
        overflow-y:scroll;
        height:85vh;
    }
    .job-list-card:nth-child(n+${nthChildValue}) { display: none; }
    `;
}

// Function to increase the nth-child value
function increaseNthChild() {
    nthChildValue += 3; 
    updateNthChild();
}


updateNthChild();

// Add event listener for the button to increase the nth-child value
loadMoreButton.addEventListener('click', increaseNthChild);

