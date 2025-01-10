document.addEventListener("DOMContentLoaded", function () {
  function getLocation() {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(showPosition, showError);
    } else {
      alert("Geolocation is not supported by this browser.");
    }
  }

  function showPosition(position) {
    document.querySelector('input[name="latitude"]').value =
      position.coords.latitude;
    document.querySelector('input[name="longitude"]').value =
      position.coords.longitude;
  }

  function showError(error) {
    switch (error.code) {
      case error.PERMISSION_DENIED:
        alert("User denied the request for Geolocation.");
        break;
      case error.POSITION_UNAVAILABLE:
        alert("Location information is unavailable.");
        break;
      case error.TIMEOUT:
        alert("The request to get user location timed out.");
        break;
      case error.UNKNOWN_ERROR:
        alert("An unknown error occurred.");
        break;
    }
  }

  // Call getLocation when the page loads
  getLocation();

  // Prevent form submission and show fake success popup
  const reportForm = document.getElementById("report-form");
  if (reportForm) {
    reportForm.addEventListener("submit", function (event) {
      event.preventDefault(); // Prevent the default form submission

      const formData = new FormData(reportForm);

      // Send data to the server
      fetch(reportForm.action, {
        method: "POST",
        body: formData,
      })
        .then((response) => {
          // Handle the response if needed
          return response.text(); // Read the response as text
        })
        .catch((error) => {
          console.error("Error:", error);
          // Handle any errors that occur during the fetch
        });

      // Simulate a delay before showing the success message
      setTimeout(() => {
        Swal.fire({
          icon: "success",
          title: "Thành công!",
          text: "Báo cáo đã được gửi thành công!",
          confirmButtonText: "OK",
        }).then(() => {
          // Delay before redirecting to the homepage
          setTimeout(() => {
            window.location.href = "/"; // Redirect to the homepage
          }, 500); // 2-second delay before redirect
        });
      }, 1000); // 2-second delay before showing the success message
    });
  } else {
    console.error('Form with ID "report-form" not found.');
  }

  var tabsFn = (function() {
    function init() {
      setHeight();
    }
    
    function setHeight() {
      var $tabPane = $('.tab-pane'),
          tabsHeight = $('.nav-tabs').height();
      
      $tabPane.css({
        height: tabsHeight
      });
    }
      
    $(init);
  })();

  $(document).ready(function() {
    $('.nav-tabs a').click(function(e) {
      e.preventDefault();
      $(this).tab('show');
    });
  });
});
