// This script is used to add click event listeners to all links in the table
// and save the checkbox state to local storage
// Make sure the table is loaded before adding event listeners
// Adds a persistent checkbox state to the table
// Add class "visitor" to the table in the parent document

var mytable = window.parent.document.getElementsByClassName("visitor")[0];
// Add click event listeners to all links in the table
for (var i = 0; i < mytable.rows.length; i++) {
  // Use querySelectorAll to find all the links in the current row
  var links = mytable.rows[i].querySelectorAll("a");
  for (var j = 0; j < links.length; j++) {
    // Check if the current link has an href attribute
    if (links[j].hasAttribute("href")) {
      links[j].addEventListener("click", function () {
        // Get the checkbox in the same row as the clicked link
        var checkbox = this.parentNode.parentNode.querySelector(
          "input[type='checkbox']"
        );
        // Check if checkbox exists in the current row
        if (checkbox != null) {
          checkbox.checked = true;
          var id = checkbox.getAttribute("data-id");
          // Save the checkbox state to local storage
          localStorage.setItem("checkbox" + id, checkbox.checked);
        }
      });
    }
  }
}

// Retrieve the checkbox state from local storage and set the checkboxes
window.addEventListener("load", function () {
  var checkboxes = mytable.querySelectorAll("input[type='checkbox']");

  for (var i = 0; i < checkboxes.length; i++) {
    var id = checkboxes[i].getAttribute("data-id");
    checkboxes[i].checked = localStorage.getItem("checkbox" + id) === "true";
  }
});
