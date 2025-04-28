// static/js/conference_search.js

document.addEventListener('DOMContentLoaded', function() {
    // Add loading indicators
    const forms = document.querySelectorAll('form[data-search-form]');
    forms.forEach(form => {
        form.addEventListener('submit', function() {
            const submitBtn = this.querySelector('button[type="submit"]');
            if (submitBtn) {
                submitBtn.innerHTML = '<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Searching...';
                submitBtn.disabled = true;
            }
        });
    });
    
    // Enable tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });
    
    // Enable filters to auto-submit
    const filterForms = document.querySelectorAll('form[data-auto-submit]');
    filterForms.forEach(form => {
        const selects = form.querySelectorAll('select');
        selects.forEach(select => {
            select.addEventListener('change', function() {
                form.submit();
            });
        });
    });
    
    // Conference card click to open details modal
    const conferenceCards = document.querySelectorAll('.conference-card');
    conferenceCards.forEach(card => {
        card.addEventListener('click', function(e) {
            // Only trigger if the click wasn't on a link or button
            if (!e.target.closest('a') && !e.target.closest('button')) {
                const title = this.querySelector('.card-title').textContent;
                const description = this.querySelector('.card-text') ? 
                    this.querySelector('.card-text').textContent : 'No description available.';
                const url = this.querySelector('a').getAttribute('href');
                const source = this.querySelector('.card-footer small').textContent;
                
                // Populate and show modal (would be defined in your HTML)
                const detailModal = document.getElementById('conferenceDetailModal');
                if (detailModal) {
                    detailModal.querySelector('.modal-title').textContent = title;
                    detailModal.querySelector('.modal-body-description').textContent = description;
                    detailModal.querySelector('.modal-body-source').textContent = source;
                    detailModal.querySelector('.modal-footer a').setAttribute('href', url);
                    
                    const modalInstance = new bootstrap.Modal(detailModal);
                    modalInstance.show();
                }
            }
        });
    });
});