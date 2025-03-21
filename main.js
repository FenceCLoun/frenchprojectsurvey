/**
 * Main JavaScript file for Media Personality Profiler
 */

document.addEventListener('DOMContentLoaded', function() {
    // Animate elements when they come into view
    const animateOnScroll = function() {
        const elements = document.querySelectorAll('.animate-on-scroll');
        
        elements.forEach(element => {
            const elementPosition = element.getBoundingClientRect().top;
            const windowHeight = window.innerHeight;
            
            if (elementPosition < windowHeight - 50) {
                element.classList.add('animated');
            }
        });
    };
    
    // Add animate-on-scroll class to elements we want to animate
    const animatedElements = document.querySelectorAll('.card, .progress-bar, h2, h3');
    animatedElements.forEach(element => {
        element.classList.add('animate-on-scroll');
    });
    
    // Add scroll event listener
    window.addEventListener('scroll', animateOnScroll);
    
    // Initial animation check
    animateOnScroll();
    
    // Progressive loading for trait scores
    setTimeout(function() {
        document.querySelectorAll('.trait-score').forEach(function(progressBar) {
            const scoreValue = progressBar.getAttribute('data-score') || '0';
            progressBar.style.width = scoreValue + '%';
        });
    }, 500);
    
    // Tooltip initialization (if using Bootstrap tooltips)
    const tooltipTriggerList = document.querySelectorAll('[data-bs-toggle="tooltip"]');
    if (tooltipTriggerList.length > 0) {
        const tooltipList = [...tooltipTriggerList].map(tooltipTriggerEl => new bootstrap.Tooltip(tooltipTriggerEl));
    }
    
    // Share buttons functionality
    const setupShareButtons = function() {
        // Share on Twitter
        const twitterButton = document.getElementById('shareTwitter');
        if (twitterButton) {
            twitterButton.addEventListener('click', function() {
                const profileType = document.querySelector('h2')?.textContent || 'My Media Personality';
                const text = `I just discovered my media personality type: ${profileType}! Check out your own media consumption profile:`;
                const url = window.location.href;
                
                window.open(`https://twitter.com/intent/tweet?text=${encodeURIComponent(text)}&url=${encodeURIComponent(url)}`, '_blank');
            });
        }
        
        // Share on Facebook
        const facebookButton = document.getElementById('shareFacebook');
        if (facebookButton) {
            facebookButton.addEventListener('click', function() {
                const url = window.location.href;
                window.open(`https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(url)}`, '_blank');
            });
        }
        
        // Copy link
        const copyLinkButton = document.getElementById('copyLink');
        if (copyLinkButton) {
            copyLinkButton.addEventListener('click', function() {
                const url = window.location.href;
                
                // Create temporary input element
                const tempInput = document.createElement('input');
                tempInput.value = url;
                document.body.appendChild(tempInput);
                
                // Select and copy
                tempInput.select();
                document.execCommand('copy');
                
                // Remove temporary element
                document.body.removeChild(tempInput);
                
                // Notify user
                const originalText = copyLinkButton.innerHTML;
                copyLinkButton.innerHTML = '<i class="fas fa-check me-2"></i> Link Copied!';
                setTimeout(() => {
                    copyLinkButton.innerHTML = originalText;
                }, 2000);
            });
        }
    };
    
    setupShareButtons();
});
