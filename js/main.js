// alert("javascript error")

const hamburger = document.querySelector(".hamburger");
const close_btn = document.querySelector(".close-btn");
const wrapper = document.querySelector(".wrapper");
const themeToggler = document.querySelector(".theme-toggler");
// const backdrop = document.querySelector(".backdrop");

hamburger.addEventListener("click", () => {
    // alert("hamburger");
    wrapper.classList.add("active");
});

close_btn.addEventListener("click", () => {
    wrapper.classList.remove("active");
});

// Change theme
themeToggler.onclick = ()=>{
    // alert("hey to your friend");
    document.body.classList.toggle('dark-theme-variables');
    themeToggler.querySelector('i:nth-child(1)').classList.toggle('active');
    themeToggler.querySelector('i:nth-child(2)').classList.toggle('active');
}