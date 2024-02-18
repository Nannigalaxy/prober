
function get_and_update_status(url_param, class_id) {

    url = "/probe_status?url=" + url_param;

    axios.get(url, { timeout: 10000 })
        .then(function (response) {
            parent = document.getElementById(class_id);
            span = parent.firstChild
            p_text = parent.lastChild
            if (response.data != '200') {
                span.className = 'downstatus'
                p_text.innerText = "Error: " + response.data + "\nProbed: " + url_param;
            }
            else {
                span.className = 'upstatus'
                p_text.innerText = "Probed: " + url_param;
            }
            p_text.classList.add("helper")
        })
        .catch(function (error) {
            console.log(error);
        });
}

function probe_and_update(target_data, status_check) {
    for (const [key, value] of Object.entries(target_data)) {
        for (const [index, entity] of Object.entries(target_data[key])) {
            for (const [entity_key, entity_value] of Object.entries(entity)) {
                if (entity_key in status_check) {
                    get_and_update_status(entity_value, entity_value);

                }
            }
        }
    }
}