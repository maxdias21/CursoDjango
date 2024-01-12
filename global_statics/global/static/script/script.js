function create_id_body(id) {
    document.body.id = id;
}

function delete_post() {
  const forms = document.querySelectorAll('.form-delete');

  for (const form of forms) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();

      const confirmed = confirm('Clique em "ok" para deletar seu post PERMANENTEMENTE');

      if (confirmed) {
        form.submit();
      }
    });
  }
}

delete_post();

/* Set the width of the sidebar to 250px and the left margin of the page content to 250px */
function openNav() {
  document.getElementById("mySidebar").style.width = "250px";
  document.getElementById("main").style.marginLeft = "250px";
}

/* Set the width of the sidebar to 0 and the left margin of the page content to 0 */
function closeNav() {
  document.getElementById("mySidebar").style.width = "0px";
  document.getElementById("main").style.marginLeft = "0";
}
