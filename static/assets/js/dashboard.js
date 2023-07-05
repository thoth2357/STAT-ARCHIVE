$(document).ready(function () {
    // Hide all upload forms initially except the active one
    $(".upload-form").not(".active").hide();

    // Handle click event on upload type buttons
    $(".upload-type-btn").click(function () {
      // Remove active class from all buttons
      $(".upload-type-btn").removeClass("active");
      // Add active class to the clicked button
      $(this).addClass("active");

      // Hide all upload forms
      $(".upload-form").hide();

      // Show the corresponding form based on data-target attribute
      var targetForm = $(this).attr("data-target");
      $("#" + targetForm).show();
    });
  });