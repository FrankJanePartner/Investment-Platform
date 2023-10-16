document.addEventListener('DOMContentLoaded', function() {
    // Retrieve the plan list element
    var planList = document.getElementById('plan-list');
  
    // Attach click event listener to each plan item
    var planItems = planList.getElementsByTagName('li');
    for (var i = 0; i < planItems.length; i++) {
      planItems[i].addEventListener('click', function() {
        // Toggle the active class on the clicked plan item
        this.classList.toggle('active');
      });
    }
  });