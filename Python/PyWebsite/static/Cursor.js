// Select the box element
const box = document.getElementById("myBox");

// Listen for mouse movements on the whole document
document.addEventListener("mousemove", (event) => {
    // Get the mouse coordinates
    const mouseX = event.clientX;
    const mouseY = event.clientY;

    // Move the box to the mouse position
    // Subtract half the box size to center it under the cursor
    const boxWidth = box.offsetWidth / 2;
    const boxHeight = box.offsetHeight / 2;

    box.style.left = (mouseX - boxWidth) + "px";
    box.style.top = (mouseY - boxHeight) + "px";
});
