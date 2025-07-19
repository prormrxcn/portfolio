document.addEventListener('DOMContentLoaded', function() {
    // Initialize star background animation
    initStarBackground();
    
    // Initialize circuit overlay parallax effect
    initCircuitOverlay();
    
    // Initialize page animations
    initPageAnimations();
    
    // Initialize form validations
    initFormValidations();
    
    // Initialize smooth scrolling
    initSmoothScrolling();
});

function initStarBackground() {
    const canvas = document.getElementById('stars');
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    let stars = [];
    const starCount = 200;

    // Set initial canvas size
    resizeCanvas();

    // Create stars
    for (let i = 0; i < starCount; i++) {
        stars.push({
            x: Math.random() * canvas.width,
            y: Math.random() * canvas.height,
            radius: Math.random() * 1.5,
            speed: Math.random() * 0.5,
            opacity: Math.random()
        });
    }

    function resizeCanvas() {
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
    }

    function drawStars() {
        // Clear canvas
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        
        // Draw gradient background
        const gradient = ctx.createRadialGradient(
            canvas.width / 2, canvas.height / 2, 0,
            canvas.width / 2, canvas.height / 2, canvas.width * 0.7
        );
        gradient.addColorStop(0, 'rgba(12, 20, 69, 0.8)');
        gradient.addColorStop(1, 'rgba(26, 35, 126, 0.8)');
        ctx.fillStyle = gradient;
        ctx.fillRect(0, 0, canvas.width, canvas.height);
        
        // Draw each star
        stars.forEach(star => {
            ctx.beginPath();
            ctx.arc(star.x, star.y, star.radius, 0, Math.PI * 2);
            
            // Twinkling effect
            const twinkle = Math.sin(Date.now() * 0.001 + star.x) * 0.5 + 0.5;
            ctx.fillStyle = `rgba(255, 255, 255, ${star.opacity * twinkle})`;
            ctx.fill();
            
            // Move star
            star.y += star.speed;
            
            // Reset star when it goes off screen
            if (star.y > canvas.height) {
                star.y = 0;
                star.x = Math.random() * canvas.width;
            }
        });
        
        requestAnimationFrame(drawStars);
    }

    // Handle window resize
    window.addEventListener('resize', () => {
        resizeCanvas();
    });

    // Start animation
    drawStars();
}

function initCircuitOverlay() {
    const circuitOverlay = document.querySelector('.circuit-overlay');
    if (!circuitOverlay) return;

    document.addEventListener('mousemove', (e) => {
        const moveX = (e.clientX - window.innerWidth / 2) / 30;
        const moveY = (e.clientY - window.innerHeight / 2) / 30;
        circuitOverlay.style.transform = `translate(${moveX}px, ${moveY}px)`;
    });
}

function initPageAnimations() {
    // Hero section animations
    if (document.querySelector('.hero')) {
        const heroContent = document.querySelector('.hero-content');
        if (heroContent) heroContent.classList.add('animate');

        setTimeout(() => {
            const cards = document.querySelectorAll('.project-card, .skill-card');
            cards.forEach((card, index) => {
                setTimeout(() => {
                    card.classList.add('animate');
                }, 150 * index);
            });
        }, 300);
    }

    // Project detail page animations
    if (document.querySelector('.project-detail')) {
        const elements = document.querySelectorAll('.project-detail > *');
        elements.forEach((el, index) => {
            setTimeout(() => {
                el.classList.add('animate');
            }, 150 * index);
        });
    }

    // Skill progress bars animation
    const progressBars = document.querySelectorAll('.progress-bar');
    progressBars.forEach(bar => {
        const width = bar.style.width;
        bar.style.width = '0';
        setTimeout(() => {
            bar.style.transition = 'width 1.5s ease-in-out';
            bar.style.width = width;
        }, 500);
    });
}

function initFormValidations() {
    // Regular contact form validation
    const contactForm = document.getElementById('contactForm');
    if (contactForm) {
        contactForm.addEventListener('submit', function(e) {
            if (!validateForm(contactForm, e)) {
                showFormError(contactForm, 'Please fill in all fields correctly.');
            }
        });
    }

    // API contact form validation
    const apiContactForm = document.getElementById('apiContactForm');
    if (apiContactForm) {
        apiContactForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            if (!validateForm(apiContactForm)) {
                showFormError(apiContactForm, 'Please fill in all fields correctly.');
                return;
            }

            const submitBtn = document.getElementById('apiSubmitBtn');
            submitBtn.disabled = true;
            submitBtn.textContent = 'Sending...';

            try {
                const formData = {
                    name: document.getElementById('apiName').value,
                    email: document.getElementById('apiEmail').value,
                    subject: document.getElementById('apiSubject').value,
                    message: document.getElementById('apiMessage').value
                };

                const response = await fetch('/api/contact', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(formData)
                });

                const result = await response.json();

                if (result.status === 'success') {
                    showFormSuccess(apiContactForm, result.message);
                    apiContactForm.reset();
                } else {
                    throw new Error(result.message);
                }
            } catch (error) {
                showFormError(apiContactForm, error.message || 'Failed to send message. Please try again.');
            } finally {
                submitBtn.disabled = false;
                submitBtn.textContent = 'Send Message';
            }
        });
    }
}

function validateForm(form, event = null) {
    let valid = true;
    const fields = ['name', 'email', 'subject', 'message'];
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;

    fields.forEach(field => {
        const input = form.querySelector(`[name="${field}"]`) || 
                     form.querySelector(`#${field}`) || 
                     form.querySelector(`#api${field.charAt(0).toUpperCase() + field.slice(1)}`);
        
        if (input) {
            if (!input.value.trim()) {
                valid = false;
                input.classList.add('is-invalid');
            } else {
                input.classList.remove('is-invalid');
            }

            // Special validation for email field
            if (field === 'email' && input.value && !emailRegex.test(input.value)) {
                valid = false;
                input.classList.add('is-invalid');
            }
        }
    });

    if (event && !valid) {
        event.preventDefault();
    }

    return valid;
}

function showFormError(form, message) {
    const existingAlert = form.querySelector('.alert');
    if (existingAlert) existingAlert.remove();

    const errorAlert = document.createElement('div');
    errorAlert.className = 'alert alert-danger mt-3';
    errorAlert.textContent = message;
    form.appendChild(errorAlert);

    setTimeout(() => {
        errorAlert.remove();
    }, 5000);
}

function showFormSuccess(form, message) {
    const existingAlert = form.querySelector('.alert');
    if (existingAlert) existingAlert.remove();

    const successAlert = document.createElement('div');
    successAlert.className = 'alert alert-success mt-3';
    successAlert.textContent = message;
    form.appendChild(successAlert);

    setTimeout(() => {
        successAlert.remove();
    }, 5000);
}

function initSmoothScrolling() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                window.scrollTo({
                    top: target.offsetTop - 80,
                    behavior: 'smooth'
                });
            }
        });
    });
}