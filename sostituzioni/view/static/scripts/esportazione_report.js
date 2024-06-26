const ui_pulsante_esporta_report = document.getElementById("pulsante-esporta-sostituzioni")
const ui_popup_esporta_report = document.getElementById("popup-esporta-sostituzioni")
const ui_radio_mese_esporta_report = document.getElementById("radio-filtro-mese-esporta-sostituzioni")
const ui_radio_data_esporta_report = document.getElementById("radio-filtro-data-esporta-sostituzioni")
const ui_filtro_mese_esporta_report = document.getElementById("filtro-mese-esporta-sostituzioni")
const ui_filtro_data_inizio_esporta_report = document.getElementById("filtro-data-inizio-esporta-sostituzioni")
const ui_filtro_data_fine_esporta_report = document.getElementById("filtro-data-fine-esporta-sostituzioni")
const ui_filtro_pubblicati_esporta_report = document.getElementById("filtro-pubblicati-esporta-sostituzioni")
const ui_filtro_cancellati_esporta_report = document.getElementById("filtro-cancellati-esporta-sostituzioni")
const ui_select_formato_report = document.getElementById("select-sostituzione-formato")
const ui_pulsante_scarica_report = document.getElementById("pulsante-scarica-esporta-sostituzioni")


const now = new Date()
now.setHours(0, 0, 0, 0)
ui_filtro_mese_esporta_report.value = now.getMonth()
ui_filtro_data_inizio_esporta_report.valueAsNumber = fix_date_to_input(now)
ui_filtro_data_fine_esporta_report.valueAsNumber = fix_date_to_input(now)


ui_pulsante_esporta_report.onclick = () => {
    if (ui_popup_esporta_report.style.display == "flex") {
        // animation has already started, let the dialog close
        return
    }

    ui_popup_esporta_report.style.display = "flex"
    setTimeout(() => {
        ui_popup_esporta_report.classList.add("visible")
    }, 1)
    ui_popup_esporta_report.focus()
}


ui_popup_esporta_report.onblur = (e) => {
    if (e.relatedTarget && e.relatedTarget.closest("#popup-esporta-sostituzioni")) {
        e.preventDefault()
        e.stopPropagation()
        ui_popup_esporta_report.focus()
        return
    }

    ui_popup_esporta_report.classList.remove("visible")
    setTimeout(() => {
        ui_popup_esporta_report.style.display = "none"
    }, 200)
}

ui_filtro_mese_esporta_report.onclick = () => {
    ui_radio_mese_esporta_report.checked = true
    ui_radio_data_esporta_report.checked = false
}

ui_filtro_data_inizio_esporta_report.onclick =
    ui_filtro_data_inizio_esporta_report.onchange =
    ui_filtro_data_fine_esporta_report.onclick =
    ui_filtro_data_fine_esporta_report.onchange = () => {
        ui_radio_mese_esporta_report.checked = false
        ui_radio_data_esporta_report.checked = true
    }


ui_pulsante_scarica_report.onclick = () => {
    let data_inizio
    let data_fine

    if (ui_radio_mese_esporta_report.checked) {
        const mese = parseInt(ui_filtro_mese_esporta_report.value)
        const now = new Date()
        const mese_corrente = now.getMonth() + 1
        let anno = now.getFullYear()
        if (mese > 7 && mese_corrente <= 7) {
            // Anno scolastico precedente
            anno -= 1
        } else if (mese <= 7 && mese_corrente > 7) {
            // Anno scolastico successivo
            anno += 1
        }

        data_inizio = new Date(anno, mese, 1).getTime() / 1000
        data_fine = new Date(anno, mese + 1, 0, 23, 59, 59).getTime() / 1000
    } else {
        data_inizio = fix_date_from_input(ui_filtro_data_inizio_esporta_report.valueAsNumber) / 1000
        data_fine = fix_date_from_input(ui_filtro_data_fine_esporta_report.valueAsNumber) / 1000
    }

    const non_pubblicato = ui_filtro_pubblicati_esporta_report.checked
    const cancellato = ui_filtro_cancellati_esporta_report.checked
    const formato = ui_select_formato_report.value


    socket.emit("esporta sostituzioni", {
        data_inizio,
        data_fine,
        non_pubblicato,
        cancellato,
        formato,
    })
}