const imgs = document.querySelectorAll(".container img");
const dots = document.querySelectorAll(".dot i");
const leftArrow = document.querySelector(".arrow-left");
const rightArrow = document.querySelector(".arrow-right");

let currentIndex = 0;
let time = 5000; // default time for auto slideshow

const defClass = (startPos, index) => {
  for (let i = startPos; i < imgs.length; i++) {
    imgs[i].style.display = "none";
    dots[i].classList.remove("fa-dot-circle");
    dots[i].classList.add("fa-circle");
  }
  imgs[index].style.display = "block";
  dots[index].classList.add("fa-dot-circle");
};

defClass(1, 0);

leftArrow.addEventListener("click", function(){
  currentIndex <= 0 ? currentIndex = imgs.length-1 : currentIndex--;
  defClass(0, currentIndex);
});

rightArrow.addEventListener("click", function(){
  currentIndex >= imgs.length-1 ? currentIndex = 0 : currentIndex++;
  defClass(0, currentIndex);
});

const startAutoSlide = () => {
  setInterval(() => {
    currentIndex >= imgs.length-1 ? currentIndex = 0 : currentIndex++;
    defClass(0, currentIndex);
  }, time);
};

startAutoSlide(); // Start the slideshow
// let currentSlide = 0;

// function showSlide(slideIndex) {
//     const slides = document.querySelectorAll('.carousel-images img');
//     if (slideIndex >= slides.length) {
//         currentSlide = 0;
//     } else if (slideIndex < 0) {
//         currentSlide = slides.length - 1;
//     } else {
//         currentSlide = slideIndex;
//     }

//     const offset = -currentSlide * 100; // Calculate offset in percentage
//     document.querySelector('.carousel-images').style.transform = `translateX(${offset}%)`;
// }

// // Auto slide every 2 seconds
// setInterval(() => {
//     showSlide(currentSlide + 1);
// }, 5000);

// // Initial display
// showSlide(currentSlide);


