/* Scroll Part */
const date = document.getElementById('date');
console.log(date);
date.innerHTML = new Date().getFullYear();


const links_container = document.querySelector('.links-container');
const links = document.querySelector('.links');
const nav_toggle = document.querySelector('.nav-toggle');

nav_toggle.addEventListener('click',()=>{
  // links_container.classList.toggle('show-links');
  const container_height = links_container.getBoundingClientRect().height;
  // console.log(container_height);
  const links_height = links.getBoundingClientRect().height;
  // console.log(links_height);
  if(container_height == 0){
    links_container.style.height = `${links_height}px`;
  }else{
    links_container.style.height = 0;
  }
});

const navbar = document.getElementById('nav');
const top_button = document.querySelector('.top-link');

window.addEventListener('scroll',()=>{
  // console.log(window.pageYOffset);
  const nav_height = navbar.getBoundingClientRect().height;
  const scroll_height = window.pageYOffset;
  if(scroll_height > nav_height){
    navbar.classList.add('fixed-nav');
  }else{
    navbar.classList.remove('fixed-nav');
  }

  if(scroll_height > 500){
    top_button.classList.add('show-link');
  }else{
    top_button.classList.remove('show-link');
  }
});

const scroll_links = document.querySelectorAll('.scroll-link');
scroll_links.forEach((link)=>{
  link.addEventListener('click',(e)=>{
    // prevent default
    e.preventDefault();
    const specific_spot_id = e.currentTarget.getAttribute('href').slice(1);
    // console.log(specific_spot_id);
    const specific_spot = document.getElementById(`${specific_spot_id}`);

    const nav_height = navbar.getBoundingClientRect().height;
    const links_container_height = links_container.getBoundingClientRect().height;
    const fixed_nav = navbar.classList.contains('fixed-nav');
    let position_spot = specific_spot.offsetTop - nav_height;
    // console.log(position_spot);

    if(!fixed_nav){
      position_spot = position_spot - nav_height;
    }
    if(nav_height > 82){
      position_spot = position_spot + links_container_height;
    }
    window.scrollTo({
      left:0,top:position_spot
    });
    links_container.style.height=0; // close the toggle
  });
});

/* Slider Part */
const slides = document.querySelectorAll('.slide');
const nextBtn = document.querySelector('.nextBtn');
const prevBtn = document.querySelector('.prevBtn');

slides.forEach((slide,index)=>{
    slide.style.left = `${index * 100}%`;
});

let counter = 0;
nextBtn.addEventListener('click',()=>{
    counter++;
    movement();
});

prevBtn.addEventListener('click',()=>{
    counter--;
    movement();
});

const movement = ()=>{
    if(counter === slides.length){
        counter = 0;
    }
    if(counter < 0){
        counter = slides.length - 1;
    }
    slides.forEach((slide) => {
        slide.style.transform = `translateX(-${counter * 100}%)`;
        slide.style.transition = "transform 0.4s ease-in-out";
    });
};
