document.addEventListener('DOMContentLoaded', function() {
  document.querySelectorAll('.enter__tab').forEach(function(stepBtn) {
    stepBtn.addEventListener('click', function(event) {
      
      const path = event.currentTarget.dataset.path;

      document.querySelectorAll('.enter__inputs').forEach(function(stepContent) {
        stepContent.classList.remove('tab-content-active');

        document.querySelector(`[data-target="${path}"]`).classList.add('tab-content-active');
        document.querySelector(`[data-path="${path}"]`).classList.add('tab-button-active');
      });

      document.querySelectorAll('.enter__tab').forEach(function(stepContent) {
        stepContent.classList.remove('tab-button-active');

        document.querySelector(`[data-path="${path}"]`).classList.add('tab-button-active');
      });
    });   
  });
});