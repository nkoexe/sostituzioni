const utente_template = `<div class="opzione-utente" data-email="{email}">
<input class="input-email-utente" type="text" placeholder="Email" required minlength="5" maxlength="80" autocomplete="off" value="{email}" oninput="modificato('{email}')">
<div class="container-selezione">
  <select class="selezione-ruolo-utente" name="ruolo" onchange="modificato('{email}')">
    <option {amministratore} value="amministratore">Amministratore</option>
    <option {editor} value="editor">Editor</option>
    <option {visualizzatore} value="visualizzatore" >Visualizzatore</option>
  </select>
</div>
<button class="material-symbols-rounded pulsante-elimina-utente" onclick="elimina_utente('{email}')">delete</button>
<button class="material-symbols-rounded pulsante-conferma-modifiche-utente hidden" onclick="conferma_modifiche('{email}')">check_circle</button>
</div>`

const ui_lista_utenti = document.querySelector("#lista-utenti")

utenti.forEach(utente => {
    ui_lista_utenti.innerHTML += utente_template.replaceAll("{email}", utente[0])
        .replace("{amministratore}", utente[1] == "amministratore" ? "selected" : "")
        .replace("{editor}", utente[1] == "editor" ? "selected" : "")
        .replace("{visualizzatore}", utente[1] == "visualizzatore" ? "selected" : "")
})


function modificato(email) {
    let element = document.querySelector(`[data-email="${email}"]`)
    element.querySelector(".pulsante-elimina-utente").classList.add("hidden")
    element.querySelector(".pulsante-conferma-modifiche-utente").classList.remove("hidden")
}

function conferma_modifiche(email) {
    let element = document.querySelector(`[data-email="${email}"]`)
    let new_email = element.querySelector(".input-email-utente").value
    let new_ruolo = element.querySelector(".selezione-ruolo-utente").value

    new_email = new_email.toLowerCase().replace(/\s/g, "")

    if (new_email === "") {
        notyf.error("Inserire una email valida")
        return
    }

    // nessuna modifica
    if (new_email === email && new_ruolo === utenti.find(utente => utente[0] === email)[1]) {
        element.querySelector(".pulsante-elimina-utente").classList.remove("hidden")
        element.querySelector(".pulsante-conferma-modifiche-utente").classList.add("hidden")
        return
    }

    element.querySelector(".input-email-utente").disabled = true
    element.querySelector(".selezione-ruolo-utente").disabled = true

    socket.emit("modifica utente", { email: email, new_email: new_email, ruolo: new_ruolo })
}

function elimina_utente(email) {
    socket.emit("elimina utente", email)
}

function nuovo_utente() {
    if (document.querySelector('[data-email=""]')) {
        document.querySelector(".input-email-utente").focus()
        return
    }

    ui_lista_utenti.innerHTML = utente_template.replaceAll("{email}", "")
        .replace("{amministratore}", "")
        .replace("{editor}", "")
        .replace("{visualizzatore}", "selected")
        + ui_lista_utenti.innerHTML;

    document.querySelector(".input-email-utente").focus()
}


//----------------------------------


socket.on("modifica utente successo", (data) => {
    let element = document.querySelector(`[data-email="${data.email}"]`)
    let new_element = utente_template.replaceAll("{email}", data.new_email)
        .replace("{amministratore}", data.ruolo == "amministratore" ? "selected" : "")
        .replace("{editor}", data.ruolo == "editor" ? "selected" : "")
        .replace("{visualizzatore}", data.ruolo == "visualizzatore" ? "selected" : "")

    element.outerHTML = new_element

    if (data.email == "") {
        // nuovo utente
        utenti.push([data.new_email, data.ruolo])
    } else {
        // modifica utente esistente
        let index = utenti.findIndex(utente => utente[0] === data.email)
        utenti[index][0] = data.new_email
        utenti[index][1] = data.ruolo
    }

    if (data.email == "") {
        notyf.success("Utente inserito con successo")
    } else {
        notyf.success("Utente modificato con successo")
    }
})

socket.on("modifica utente errore", (data) => {
    let element = document.querySelector(`[data-email="${data.email}"]`)
    element.querySelector(".input-email-utente").disabled = false
    element.querySelector(".selezione-ruolo-utente").disabled = false

    if (data.email == "") {
        notyf.error("Errore nell'inserimento dell'utente: " + data.error)
    } else {
        notyf.error("Errore nella modifica dell'utente: " + data.error)
    }
})

socket.on("elimina utente successo", (email) => {
    if (email == "") {
        let element = document.querySelector(`[data-email="${email}"]`)
        element.remove()
        return
    }

    let index = utenti.findIndex(utente => utente[0] === email)
    if (index == -1) return;
    utenti.splice(index, 1)

    let element = document.querySelector(`[data-email="${email}"]`)
    element.remove()

    notyf.success("Utente eliminato con successo")
})

socket.on("elimina utente errore", (data) => {
    notyf.error("Errore nell'eliminazione dell'utente: " + data.error)
})