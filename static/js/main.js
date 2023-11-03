// alert("javascript error")



const hamburger = document.querySelector(".hamburger");
const close_btn = document.querySelector(".close-btn");
const wrapper = document.querySelector(".wrapper");

// const backdrop = document.querySelector(".backdrop");

hamburger.addEventListener("click", () => {
    // alert("hamburger");
    wrapper.classList.add("active");
});

close_btn.addEventListener("click", () => {
    wrapper.classList.remove("active");
});


// Implementing persistent dark mode using localstorage
const themeToggler = document.querySelector(".theme-toggler");
const isDarkMode = localStorage.getItem('darkMode') === 'true';

// Function to toggle the dark mode
function toggleDarkMode() {
    const body = document.body;
    body.classList.toggle('dark-theme-variables');
    themeToggler.querySelector('i:nth-child(1)').classList.toggle('active');
    themeToggler.querySelector('i:nth-child(2)').classList.toggle('active');

    // Store the user's preference in localStorage
    localStorage.setItem('darkMode', body.classList.contains('dark-theme-variables'));
}

// Initialize the theme based on the user's preference
if (isDarkMode) {
    toggleDarkMode();
}

themeToggler.onclick = toggleDarkMode;

// Add or remove a class on the body element based on dark mode preference
const body = document.body;
if (isDarkMode) {
    body.classList.add('dark-theme-variables');
} else {
    body.classList.remove('dark-theme-variables');
}


// Change theme (Non persistent dark mode implementation)
// const themeToggler = document.querySelector(".theme-toggler");
// themeToggler.onclick = ()=>{
//     // alert("hey to your friend");
//     document.body.classList.toggle('dark-theme-variables');
//     themeToggler.querySelector('i:nth-child(1)').classList.toggle('active');
//     themeToggler.querySelector('i:nth-child(2)').classList.toggle('active');
// }

