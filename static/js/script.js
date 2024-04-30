$(document).ready(function () {
  $(".alert").alert();
  $(".user-filter").change(function () {
    $("#search-form").submit();
  });
});