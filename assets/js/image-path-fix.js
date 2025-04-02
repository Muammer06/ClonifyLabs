document.addEventListener('DOMContentLoaded', function() {
  // Fix image paths if on GitHub Pages
  if (window.location.hostname.includes('github.io')) {
    const images = document.querySelectorAll('img');
    const baseUrl = '/ClonifyLabs'; // Update this to match your repo name
    
    images.forEach(img => {
      if (img.src.startsWith(window.location.origin) && !img.src.includes(baseUrl)) {
        img.src = img.src.replace(window.location.origin, window.location.origin + baseUrl);
      }
    });
  }
});
