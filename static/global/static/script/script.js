function create_id_body(id) {
    document.body.id = id;
}

function delete_post() {
  const forms = document.querySelectorAll('.form-delete');

  for (const form of forms) {
    form.addEventListener('submit', function (e) {
      e.preventDefault();

      const confirmed = confirm('Você tem certeza que quer deletar o post PERMANENTEMENTE?');

      if (confirmed) {
        form.submit();
      }
    });
  }
}

delete_post();
