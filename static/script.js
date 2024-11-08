// Send a request to Flask to add or remove a item from the favorites
function favorite(reference) {
    fetch('/favorite?reference=' + reference)
        .then(resp => resp.json()) // get response from server (app.py favorite)
        .then(data => {
            const favoriteBtn = document.getElementById(reference)
            const current_item_row = document.getElementById(reference)
            const current_path = window.location.pathname

            // Only visual
            if (current_path === "/") {
                if (data["message"] == "added") {
                    favoriteBtn.attributes["fill"].value = "green"
                } else if (data["message"] == "removed") {
                    favoriteBtn.attributes["fill"].value = "grey"
                }
            } else if (current_path == "/favorites") {
                if (data["message"] == "removed") {
                    current_item_row.style.visibility = "collapse"
                }
            }
        })
}

// Send request to flask to remove tag from the pair part tag
// flask will give a response
function remove_tag(info) {
    const tag_id = info.tag_id
    const part_id = info.part_id

    const tag_element = document.getElementById("tag_div_tag_id_" + tag_id)

    fetch('/remove_tag', {
            method: 'POST',
            headers: {
                'Accept': 'application/json',
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                tag_id: info.tag_id,
                part_id: info.part_id,
                order: "remove_tag"
            })
        })
        .then(resp => resp.json())
        .then(data => {
            console.log(data)
            tag_element.remove()
        })
}

// copy to clipboard the "reference"
function copy_reference(reference) {
    navigator.clipboard.writeText(reference.toString())
}

// popup confirmation
function confirmation_alert(tag_id, tag_name) {
    const current_alert = document.querySelectorAll('.alert')
    const part_id = document.querySelector('#part_id').value

    if (!current_alert[0]) {
      const alert_placeholder = document.querySelector('.alert_placeholder_tag_id_' + tag_id)
      const confirmation_alert = document.createElement('div')
      const current_tag_div = document.getElementById('tag_div_tag_id_' + tag_id)

      const info = {
        part_id: part_id,
        tag_id: tag_id
      }
      
      // remove_tag(info) is called here
      confirmation_alert.innerHTML = [
          '<div class="alert alert-warning d-flex align-items-center alert-dismissible fade show" role="alert">',
              `<span class="text-nowrap fs-8"><strong>Remove "${tag_name}" tag from this part?</strong></span>`,
              '<div id="btn_yes_no" data-bs-dismiss="alert" aria-label="Close" class="btn-group badge" role="group">',
                  `<button type="button" class="btn btn-success btn-sm" onclick='remove_tag({part_id:"${part_id}", tag_id:"${tag_id}"})'>Yes</button>`,
                  '<button type="button" class="btn btn-danger btn-sm">No</button>',
              '</div>',
          '</div>',
      ].join("")

      alert_placeholder.append(confirmation_alert)
    }
  }
