$(document).ready(function () {
    $(".alert").alert();
    $("#user-collection-btn").click(function () {
        $("#user-collection-card").removeClass("hidden");
        $("#user-wishlist-card").addClass("hidden");
    });
    $("#user-wishlist-btn").click(function () {
      $("#user-collection-card").addClass("hidden");
      $("#user-wishlist-card").removeClass("hidden");
    });
});
