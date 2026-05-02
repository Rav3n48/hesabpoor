document.addEventListener("DOMContentLoaded", () => {
  const iconSelectors = [
    "nav a i",
  ];

  const allIcons = document.querySelectorAll(iconSelectors.join(", "));

  const rubberBandKeyframes = [
    { transform: "scale3d(1, 1, 1)", offset: 0 },
    { transform: "scale3d(1.25, 0.75, 1)", offset: 0.3 },
    { transform: "scale3d(0.75, 1.25, 1)", offset: 0.4 },
    { transform: "scale3d(1.15, 0.85, 1)", offset: 0.5 },
    { transform: "scale3d(0.95, 1.05, 1)", offset: 0.65 },
    { transform: "scale3d(1.05, 0.95, 1)", offset: 0.75 },
    { transform: "scale3d(1, 1, 1)", offset: 1 },
  ];

  const animationOptions = {
    duration: 800,
    easing: "ease-in-out",
    fill: "forwards",
  };

  allIcons.forEach((icon) => {
    icon.style.cursor = "pointer";
    icon.style.transition = "none";

    icon.addEventListener("mouseenter", function () {
      if (
        this.getAnimations().length === 0 ||
        this.getAnimations()[0].playState === "finished"
      ) {
        this.animate(rubberBandKeyframes, animationOptions);
      }
    });
  });
});
new SlimSelect({
  select: '#mySelect'
})
