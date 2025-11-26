// Add interactivity for filters
document.addEventListener('DOMContentLoaded', function() {
    const filters = document.querySelectorAll('.filter-select');

    filters.forEach(filter => {
        filter.addEventListener('change', function() {
            // Add visual feedback
            this.style.borderColor = '#667eea';
            setTimeout(() => {
                this.style.borderColor = '#e1e5e9';
            }, 1000);

            // Here you would typically update the charts based on filters
            console.log('Filter changed:', this.id, this.value);
        });
    });

    // Add smooth scrolling
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Add loading animation
    const statNumbers = document.querySelectorAll('.stat-number');
    statNumbers.forEach(stat => {
        const finalValue = stat.textContent;
        stat.textContent = '0';

        let current = 0;
        const target = parseInt(finalValue.replace(/,/g, ''));
        const increment = target / 50;

        const timer = setInterval(() => {
            current += increment;
            if (current >= target) {
                current = target;
                clearInterval(timer);
            }
            stat.textContent = Math.floor(current).toLocaleString();
        }, 50);
    });

    // Add hover effects to cards
    const cards = document.querySelectorAll('.stat-card');
    cards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.background = 'rgba(255, 255, 255, 1)';
        });
        card.addEventListener('mouseleave', function() {
            this.style.background = 'rgba(255, 255, 255, 0.95)';
        });
    });
});