// TownSquare Main JavaScript File

// Utility Functions
const TownSquare = {
    // Initialize the application
    init: function() {
        this.setupEventListeners();
        this.setupTooltips();
        this.setupFormValidation();
        this.setupAutoSave();
        console.log('TownSquare initialized successfully!');
    },

    // Setup global event listeners
    setupEventListeners: function() {
        // Auto-hide alerts after 5 seconds
        document.addEventListener('DOMContentLoaded', function() {
            const alerts = document.querySelectorAll('.alert');
            alerts.forEach(alert => {
                setTimeout(() => {
                    if (alert.parentNode) {
                        alert.style.transition = 'opacity 0.5s ease';
                        alert.style.opacity = '0';
                        setTimeout(() => {
                            if (alert.parentNode) {
                                alert.remove();
                            }
                        }, 500);
                    }
                }, 5000);
            });
        });

        // Smooth scrolling for anchor links
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

        // Form submission loading states
        document.querySelectorAll('form').forEach(form => {
            form.addEventListener('submit', function() {
                const submitBtn = this.querySelector('button[type="submit"]');
                if (submitBtn) {
                    submitBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Processing...';
                    submitBtn.disabled = true;
                    submitBtn.classList.add('loading');
                }
            });
        });
    },

    // Setup Bootstrap tooltips
    setupTooltips: function() {
        const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    },

    // Setup form validation
    setupFormValidation: function() {
        // Real-time form validation
        document.querySelectorAll('.form-control, .form-select').forEach(input => {
            input.addEventListener('blur', function() {
                this.classList.remove('is-valid', 'is-invalid');
                
                if (this.checkValidity()) {
                    this.classList.add('is-valid');
                } else {
                    this.classList.add('is-invalid');
                }
            });

            input.addEventListener('input', function() {
                if (this.classList.contains('is-invalid')) {
                    this.classList.remove('is-invalid');
                }
            });
        });
    },

    // Setup auto-save functionality for forms
    setupAutoSave: function() {
        const forms = document.querySelectorAll('form[data-autosave]');
        forms.forEach(form => {
            const formData = new FormData(form);
            const formKey = form.getAttribute('data-autosave') || 'form_' + Math.random().toString(36).substr(2, 9);
            
            // Load saved data
            const savedData = localStorage.getItem(formKey);
            if (savedData) {
                try {
                    const data = JSON.parse(savedData);
                    Object.keys(data).forEach(key => {
                        const input = form.querySelector(`[name="${key}"]`);
                        if (input) {
                            input.value = data[key];
                        }
                    });
                } catch (e) {
                    console.warn('Could not load saved form data:', e);
                }
            }

            // Auto-save on input
            form.addEventListener('input', function(e) {
                if (e.target.name) {
                    const currentData = {};
                    const formData = new FormData(form);
                    for (let [key, value] of formData.entries()) {
                        currentData[key] = value;
                    }
                    localStorage.setItem(formKey, JSON.stringify(currentData));
                }
            });

            // Clear saved data on successful submission
            form.addEventListener('submit', function() {
                localStorage.removeItem(formKey);
            });
        });
    },

    // Show notification
    showNotification: function(message, type = 'info', duration = 5000) {
        const notification = document.createElement('div');
        notification.className = `alert alert-${type} alert-dismissible fade show position-fixed`;
        notification.style.cssText = `
            top: 20px;
            right: 20px;
            z-index: 9999;
            min-width: 300px;
            box-shadow: 0 0.5rem 1rem rgba(0, 0, 0, 0.15);
        `;
        
        notification.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        
        document.body.appendChild(notification);
        
        // Auto-remove after duration
        setTimeout(() => {
            if (notification.parentNode) {
                notification.remove();
            }
        }, duration);
        
        return notification;
    },

    // Confirm action
    confirmAction: function(message, callback) {
        if (confirm(message)) {
            callback();
        }
    },

    // Format date
    formatDate: function(dateString) {
        const date = new Date(dateString);
        return date.toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'short',
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        });
    },

    // Format file size
    formatFileSize: function(bytes) {
        if (bytes === 0) return '0 Bytes';
        const k = 1024;
        const sizes = ['Bytes', 'KB', 'MB', 'GB'];
        const i = Math.floor(Math.log(bytes) / Math.log(k));
        return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
    },

    // Debounce function
    debounce: function(func, wait, immediate) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                timeout = null;
                if (!immediate) func(...args);
            };
            const callNow = immediate && !timeout;
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
            if (callNow) func(...args);
        };
    },

    // Throttle function
    throttle: function(func, limit) {
        let inThrottle;
        return function() {
            const args = arguments;
            const context = this;
            if (!inThrottle) {
                func.apply(context, args);
                inThrottle = true;
                setTimeout(() => inThrottle = false, limit);
            }
        };
    },

    // Copy to clipboard
    copyToClipboard: function(text) {
        if (navigator.clipboard && window.isSecureContext) {
            navigator.clipboard.writeText(text).then(() => {
                this.showNotification('Copied to clipboard!', 'success', 2000);
            }).catch(() => {
                this.fallbackCopyToClipboard(text);
            });
        } else {
            this.fallbackCopyToClipboard(text);
        }
    },

    // Fallback copy method
    fallbackCopyToClipboard: function(text) {
        const textArea = document.createElement('textarea');
        textArea.value = text;
        textArea.style.position = 'fixed';
        textArea.style.left = '-999999px';
        textArea.style.top = '-999999px';
        document.body.appendChild(textArea);
        textArea.focus();
        textArea.select();
        
        try {
            document.execCommand('copy');
            this.showNotification('Copied to clipboard!', 'success', 2000);
        } catch (err) {
            this.showNotification('Failed to copy to clipboard', 'danger', 3000);
        }
        
        document.body.removeChild(textArea);
    },

    // Search functionality
    search: function(query, elements, options = {}) {
        const {
            searchFields = ['textContent'],
            caseSensitive = false,
            highlight = true
        } = options;

        const results = [];
        const searchTerm = caseSensitive ? query : query.toLowerCase();

        elements.forEach(element => {
            let matchFound = false;
            let elementText = '';

            searchFields.forEach(field => {
                if (element[field]) {
                    elementText += element[field] + ' ';
                }
            });

            if (!caseSensitive) {
                elementText = elementText.toLowerCase();
            }

            if (elementText.includes(searchTerm)) {
                matchFound = true;
                results.push(element);
            }

            // Highlight matches
            if (highlight && matchFound) {
                element.style.backgroundColor = 'rgba(255, 255, 0, 0.3)';
                setTimeout(() => {
                    element.style.backgroundColor = '';
                }, 2000);
            }
        });

        return results;
    },

    // Lazy loading for images
    setupLazyLoading: function() {
        const images = document.querySelectorAll('img[data-src]');
        const imageObserver = new IntersectionObserver((entries, observer) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    const img = entry.target;
                    img.src = img.dataset.src;
                    img.classList.remove('lazy');
                    imageObserver.unobserve(img);
                }
            });
        });

        images.forEach(img => imageObserver.observe(img));
    },

    // Theme switcher
    setupThemeSwitcher: function() {
        const themeToggle = document.getElementById('theme-toggle');
        if (themeToggle) {
            const currentTheme = localStorage.getItem('theme') || 'light';
            document.body.setAttribute('data-theme', currentTheme);
            
            themeToggle.addEventListener('click', () => {
                const currentTheme = document.body.getAttribute('data-theme');
                const newTheme = currentTheme === 'light' ? 'dark' : 'light';
                
                document.body.setAttribute('data-theme', newTheme);
                localStorage.setItem('theme', newTheme);
                
                this.showNotification(`Switched to ${newTheme} theme`, 'info', 2000);
            });
        }
    }
};

// Initialize when DOM is ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => TownSquare.init());
} else {
    TownSquare.init();
}

// Export for use in other scripts
if (typeof module !== 'undefined' && module.exports) {
    module.exports = TownSquare;
} else if (typeof window !== 'undefined') {
    window.TownSquare = TownSquare;
}



