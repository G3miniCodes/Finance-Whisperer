const carousel = document.querySelector('.carousel');
const leftArrow = document.getElementById('left-arrow');
const rightArrow = document.getElementById('right-arrow');

let offset = 0;
const cardWidth = 330; // Width of each card including margin
const visibleCards = 3; // Number of visible cards
const maxOffset = -((carousel.children.length - visibleCards) * cardWidth); // Maximum offset

rightArrow.addEventListener('click', () => {
  if (offset > maxOffset) {
    offset -= cardWidth; // Move left by 1 card width
    carousel.style.transform = `translateX(${offset}px)`;
  }
});

leftArrow.addEventListener('click', () => {
  if (offset < 0) {
    offset += cardWidth; // Move right by 1 card width
    carousel.style.transform = `translateX(${offset}px)`;
  }
});

// Get all the cards
const cards = document.querySelectorAll('.card');

// Add hover effect to each card
cards.forEach((card) => {
  card.addEventListener('mouseenter', () => {
    card.classList.add('hover-card'); // Add hover class when mouse enters
  });
  card.addEventListener('mouseleave', () => {
    card.classList.remove('hover-card'); // Remove hover class when mouse leaves
  });
});
