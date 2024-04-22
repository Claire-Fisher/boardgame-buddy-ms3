$(document).ready(function () {
  $(".alert").alert();
  $("#user-collection-btn").click(function () {
    $("#user-collection-card").removeClass("hidden");
    $("#user-wishlist-card").addClass("hidden");
  });
});
