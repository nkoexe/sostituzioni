"""
Gestione della configurazione del sistema tramite il file configurazione.json
"""

import os
import subprocess
from shutil import which
from pathlib import Path
from json import load, dump
import logging

from beartype._decor.decormain import beartype
from beartype.typing import List, Dict, Any, Iterator

import sostituzioni.control.logging
from sostituzioni.lib.searchablelist import SearchableList

logger = logging.getLogger(__name__)


ROOT_PATH = Path(__file__).parent.parent
CONFIG_FILE = ROOT_PATH / "database" / "configurazione.json"
CONFIG_TEMPLATE = ROOT_PATH / "database" / "configurazione.json.template"


@beartype
def parsepath(pathstring: str) -> Path:
    pathstring = pathstring.replace("%ROOT%", str(ROOT_PATH))

    return Path(pathstring)


class Sezione:
    """
    Gruppo di opzioni.
    """

    @beartype
    def __init__(self, id: str, dati: Dict):
        self.id = id
        self.titolo: str = dati.get("titolo", "")
        self.descrizione: str = dati.get("descrizione", "")

    def __repr__(self):
        return "Sezione" + self.id

    def aggiorna(self, template):
        self.titolo = template.titolo
        self.descrizione = template.descrizione


class Opzione:
    """
    Singola opzione per la configurazione del sistema.
    """

    TESTO = "testo"
    NUMERO = "numero"
    NUMERO_UNITA = "numero_unita"
    BOOLEANO = "booleano"
    COLORE = "colore"
    SELEZIONE = "selezione"
    PERCORSO = "percorso"
    LISTA = "lista"

    @beartype
    def __init__(
        self,
        id: str | None = None,
        dati: Dict = {},
        parent: object | None = None,
        index: int | None = None,
    ):
        self.parent = parent

        # Opzione regolare
        if id is not None:
            titolo = dati.get("titolo", "")
            descrizione = dati.get("descrizione", "")
            sezione = dati.get("sezione", "")
            disabilitato = dati.get("disabilitato", False)
            nascosto = dati.get("nascosto", False)
            tipo = dati.get("tipo", "")

        # Questa è una sotto-opzione
        elif parent is not None:
            id = parent.id + "_" + str(index)
            titolo = ""
            descrizione = ""
            sezione = parent.sezione
            disabilitato = dati.get("disabilitato", False)
            nascosto = dati.get("nascosto", False)
            tipo = parent.tipo_valori

        else:
            raise ValueError("Fornire id o parent")

        self.id = id
        self.titolo: str = titolo
        self.descrizione: str = descrizione
        self.sezione: str = sezione
        self.disabilitato: bool = disabilitato
        self.nascosto: bool = nascosto
        self.tipo: str = tipo

        match self.tipo:
            case self.TESTO:
                self.lunghezza_massima: int | None = dati.get("lunghezza_massima", None)
                self.default: str = dati.get("default", "")
                self.valore: str = dati.get("valore", "")

            case self.NUMERO:
                self.intervallo: List[int | None] = dati.get("intervallo", [None, None])
                self.default: int | float = dati.get("default", 0)
                self.valore: int | float = dati.get("valore", 0)

            case self.NUMERO_UNITA:
                self.intervallo: List[int | None] = dati.get("intervallo", [None, None])
                self.scelte_unita: List[str] = dati.get("scelte_unita", [""])
                self.unita_default: int = dati.get("unita_default", 0)
                self.unita: int = dati.get("unita", 0)
                self.default: int | float = dati.get("default", 0)
                self.valore: int | float = dati.get("valore", 0)

            case self.BOOLEANO:
                self.default: bool = dati.get("default", False)
                self.valore: bool = dati.get("valore", False)

            case self.COLORE:
                self.default: str = dati.get("default", "")
                self.valore: str = dati.get("valore", "")

            case self.SELEZIONE:
                self.scelte: List[str] = dati.get("scelte", [""])
                self.default: int = dati.get("default", 0)
                self.valore: int = dati.get("valore", 0)

            case self.PERCORSO:
                self.scelte_radice: List[str] = dati.get("scelte_radice", [""])
                self.radice: int = dati.get("radice", 0)
                self.default: str = dati.get("default", "")
                self.valore: str = dati.get("valore", "")

                self.path = parsepath(self.scelte_radice[self.radice]) / parsepath(
                    self.valore
                )

            case self.LISTA:
                self.tipo_valori: str = dati.get("tipo_valori", "")
                self.default: list = []
                self.valore: list = []

                for index in range(len(dati.get("default", []))):
                    dati_lista = dati.get("default")[index]
                    self.default.append(
                        Opzione(parent=self, dati=dati_lista, index=index)
                    )

                for index in range(len(dati.get("valore", []))):
                    dati_lista = dati.get("valore")[index]
                    self.valore.append(
                        Opzione(parent=self, dati=dati_lista, index=index)
                    )

            case _:
                logger.error(
                    f"Nel caricamento della configurazione, opzione con id {self.id} non ha un tipo valido ({self.tipo})"
                )

    def aggiorna(self, template):
        self.titolo = template.titolo
        self.descrizione = template.descrizione
        self.sezione = template.sezione
        self.disabilitato = template.disabilitato
        self.nascosto = template.nascosto
        self.tipo = template.tipo
        self.default = template.default

        match self.tipo:
            case self.TESTO:
                self.lunghezza_massima = template.lunghezza_massima

            case self.NUMERO:
                self.intervallo = template.intervallo

            case self.NUMERO_UNITA:
                self.intervallo = template.intervallo
                self.scelte_unita = template.scelte_unita
                self.unita_default = template.unita_default
                self.unita = template.unita

            case self.SELEZIONE:
                self.scelte = template.scelte

            case self.PERCORSO:
                self.scelte_radice = template.scelte_radice
                self.radice = template.radice

            case self.LISTA:
                self.tipo_valori = template.tipo_valori

    def __eq__(self, value: object) -> bool:
        return self.valore == value

    def __ne__(self, value: object) -> bool:
        return self.valore != value

    def __lt__(self, value: object) -> bool:
        return self.valore < value

    def __le__(self, value: object) -> bool:
        return self.valore <= value

    def __gt__(self, value: object) -> bool:
        return self.valore > value

    def __ge__(self, value: object) -> bool:
        return self.valore >= value

    def __mul__(self, value: object) -> int | float:
        return self.valore * value

    def __rmul__(self, value: object) -> int | float:
        return value * self.valore

    def __add__(self, value: object) -> int | float:
        return self.valore + value

    def __radd__(self, value: object) -> int | float:
        return value + self.valore

    def __sub__(self, value: object) -> int | float:
        return self.valore - value

    def __rsub__(self, value: object) -> int | float:
        return value - self.valore

    def __truediv__(self, value: object) -> int | float:
        return self.valore / value

    def __rtruediv__(self, value: object) -> int | float:
        return value / self.valore

    def __floordiv__(self, value: object) -> int:
        return self.valore // value

    def __rfloordiv__(self, value: object) -> int:
        return value // self.valore

    def __mod__(self, value: object) -> int:
        return self.valore % value

    def __rmod__(self, value: object) -> int:
        return value % self.valore

    def __pow__(self, value: object) -> int | float:
        return self.valore**value

    def __rpow__(self, value: object) -> int | float:
        return value**self.valore

    def __str__(self) -> str:
        return str(self.valore)

    def __repr__(self) -> str:
        return str(self.valore)

    def __bool__(self) -> bool:
        return bool(self.valore)

    def __int__(self) -> int:
        return int(self.valore)

    def __float__(self) -> float:
        return float(self.valore)

    def __len__(self) -> int:
        return len(self.valore)

    def __iter__(self) -> Iterator[str]:
        return iter(self.valore)

    def __contains__(self, item: str) -> bool:
        return item in self.valore

    def __getitem__(self, item: int) -> str:
        return self.valore[item]

    @beartype
    def set(self, dati: Any, force: bool = False, index: int | None = None):
        logger.debug(f"Setter {self.id}: {dati} {index if index else ''}")

        if not force and (self.disabilitato):
            logger.debug("Setter disabilitato, impossibile aggiornare l'opzione.")
            return False

        match self.tipo:
            case self.TESTO:
                if not isinstance(dati, str):
                    raise TypeError(
                        f"Dati non validi, fornire stringa, non {type(dati)}"
                    )

                if (self.lunghezza_massima is not None) and (
                    len(dati) > self.lunghezza_massima
                ):
                    logger.debug(
                        f"Setter {self.id}, valore {dati} sfora la lunghezza massima di {self.lunghezza_massima}"
                    )
                    return False

                self.valore = dati
                return True

            case self.NUMERO:
                if not isinstance(dati, (int, float)):
                    raise TypeError(
                        f"Dati non validi, fornire int o float, non {type(dati)}"
                    )

                if (
                    (self.intervallo[0] is not None)
                    and not (self.intervallo[0] <= dati)
                ) or (
                    (self.intervallo[1] is not None)
                    and not (dati <= self.intervallo[1])
                ):
                    logger.error(
                        f"Valore {dati} sfora l'intervallo di {self.intervallo}"
                    )
                    return False

                self.valore = dati
                return True

            case self.NUMERO_UNITA:
                if not isinstance(dati, (list, tuple)) or len(dati) != 2:
                    raise ValueError(
                        f"Dati {dati} non validi, per numero con unità fornire (valore, index_unita)"
                    )
                if not isinstance(dati[0], (int, float)):
                    raise TypeError(
                        "Valore del numero deve essere di tipo int o float, non "
                        + str(type(dati[0]))
                    )
                if not isinstance(dati[1], int):
                    raise TypeError(
                        "L'indice dell'unità deve essere di tipo int, non "
                        + str(type(dati[1]))
                    )
                if not 0 <= dati[1] < len(self.scelte_unita):
                    raise ValueError(
                        f"L'indice dell'unità {dati[1]} non è valido, deve essere compreso tra 0 e {len(self.scelte_unita) - 1}"
                    )

                if (
                    (self.intervallo[0] is not None)
                    and not (self.intervallo[0] <= dati[0])
                ) and (
                    (self.intervallo[1] is not None)
                    and not (dati[0] <= self.intervallo[1])
                ):
                    logger.warning(
                        f"Valore {dati[0]} sfora l'intervallo di {self.intervallo}"
                    )
                    return False

                self.valore = dati[0]
                self.unita = dati[1]
                return True

            case self.BOOLEANO:
                if not isinstance(dati, bool):
                    raise TypeError(
                        "Valore deve essere di tipo bool, non " + str(type(dati))
                    )

                self.valore = dati
                return True

            case self.COLORE:
                pass

            case self.SELEZIONE:
                if not isinstance(dati, int):
                    raise TypeError(
                        "Valore deve essere di tipo int, non " + str(type(dati))
                    )
                if not 0 <= dati < len(self.scelte):
                    raise ValueError(
                        f"Valore {dati} non valido, deve essere compreso tra 0 e {len(self.scelte) - 1}"
                    )

                self.valore = dati
                return True

            case self.PERCORSO:
                if not isinstance(dati, (list, tuple)) or len(dati) != 2:
                    raise ValueError(
                        "Dati non validi, per percorso fornire (index_radice, percorso)"
                    )
                if not isinstance(dati[0], int):
                    raise TypeError(
                        "L'indice della radice deve essere di tipo int, non "
                        + str(type(dati[0]))
                    )
                if not isinstance(dati[1], (str, Path)):
                    raise TypeError(
                        "Il percorso deve essere di tipo str o Path, non "
                        + str(type(dati[1]))
                    )
                if not 0 <= dati[0] < len(self.scelte_radice):
                    raise ValueError(
                        f"L'indice della radice {dati[0]} non è valido, deve essere compreso tra 0 e {len(self.scelte_radice) - 1}"
                    )

                if isinstance(dati[1], Path):
                    dati[1] = dati[1].as_posix()

                self.radice = dati[0]
                self.valore = dati[1]

                self.path = parsepath(self.scelte_radice[self.radice]) / parsepath(
                    self.valore
                )

                return True

            case self.LISTA:
                # Modifica un solo elemento della lista
                if index is not None:
                    opzione = Opzione(parent=self)
                    opzione.set(dati)
                    self.valore[index] = opzione
                    return True

                # Modifica tutte le opzioni della lista
                if not isinstance(dati, list):
                    raise TypeError("Dati non validi, per lista fornire un array")

                self.valore = []
                for dato in dati:
                    opzione = Opzione(parent=self)
                    opzione.set(dato)
                    self.valore.append(opzione)

                return True

    def esporta(self):

        dati = {
            "titolo": self.titolo,
            "descrizione": self.descrizione,
            "sezione": self.sezione,
            "disabilitato": self.disabilitato,
            "nascosto": self.nascosto,
            "tipo": self.tipo,
        }

        match self.tipo:
            case self.TESTO:
                dati["lunghezza_massima"] = self.lunghezza_massima
                dati["default"] = self.default
                dati["valore"] = self.valore

            case self.NUMERO:
                dati["intervallo"] = self.intervallo
                dati["default"] = self.default
                dati["valore"] = self.valore

            case self.NUMERO_UNITA:
                dati["intervallo"] = self.intervallo
                dati["scelte_unita"] = self.scelte_unita
                dati["unita_default"] = self.unita_default
                dati["unita"] = self.unita
                dati["default"] = self.default
                dati["valore"] = self.valore

            case self.BOOLEANO:
                dati["default"] = self.default
                dati["valore"] = self.valore

            case self.COLORE:
                dati["default"] = self.default
                dati["valore"] = self.valore

            case self.SELEZIONE:
                dati["scelte"] = self.scelte
                dati["default"] = self.default
                dati["valore"] = self.valore

            case self.PERCORSO:
                dati["radice"] = self.radice
                dati["scelte_radice"] = self.scelte_radice
                dati["default"] = str(self.default)
                dati["valore"] = str(self.valore)

            case self.LISTA:
                dati["tipo_valori"] = self.tipo_valori
                dati["default"] = [
                    {"valore": opzione.valore} for opzione in self.default
                ]

                valori = []
                for opzione in self.valore:
                    match self.tipo_valori:
                        case self.TESTO:
                            dato = {"valore": opzione.valore}
                        case self.NUMERO:
                            dato = {"valore": opzione.valore}
                        case self.PERCORSO:
                            dato = {"valore": opzione.valore}
                        case _:
                            raise ValueError(
                                f"Tipo {self.tipo_valori} non ancora supportato."
                            )
                    valori.append(dato)

                dati["valore"] = valori

        return dati


class Configurazione:
    @beartype
    def __init__(self):
        self.shell_commands = {}

        if which("git") is None:
            logger.error("Git non trovato.")

        if os.name == "nt":
            self.shell_commands["update"] = ["git", "pull"]
            self.shell_commands["reboot"] = [
                "kill",
                "-9",
                str(os.getpid()),
                "&&",
                "python",
                "-m",
                "sostituzioni",
            ]
            self.shell_commands["get_version"] = [
                "git",
                "rev-parse",
                # "--short",
                "HEAD",
            ]
            self.shell_commands["check_update"] = [
                "git",
                "ls-remote",
                "origin",
                "main",
            ]
        else:
            if which("systemctl") is None:
                logger.error("Systemctl non trovato.")

            self.shell_commands["update"] = ["git", "pull"]
            self.shell_commands["reboot"] = [
                "systemctl",
                "restart",
                "sostituzioni.service",
            ]
            self.shell_commands["get_version"] = [
                "git",
                "rev-parse",
                # "--short",
                "HEAD",
            ]
            self.shell_commands["check_update"] = [
                "git",
                "ls-remote",
                "origin",
                "main",
            ]

    def load(self, file: Path = CONFIG_FILE):
        with open(file, encoding="utf-8") as configfile:
            logger.debug("Caricamento file di configurazione..")
            self.data = load(configfile)
            # logger.debug(f"Raw data: {self.data}")

        # Todo: controllare validità file

        self.sezioni = SearchableList()
        self.opzioni = SearchableList()

        for sectionid, sectiondata in self.data.get("sezioni").items():
            sezione = Sezione(sectionid, sectiondata)
            self.sezioni.append(sezione)

        for optionid, optiondata in self.data.get("opzioni").items():
            opzione = Opzione(optionid, optiondata)
            self.opzioni.append(opzione)

        # Tutti i dati sono caricati in oggetti, self.data non verrà aggiornato quindi eliminarlo per sicurezza
        del self.data

        # Aggiorna il percorso base di sistema e quello del file di configurazione
        self.set("rootpath", [0, str(ROOT_PATH)], force=True)
        self.set("configpath", [0, str(file)], force=True)

        # Carica il dato di versione del sistema
        v = (
            subprocess.check_output(self.shell_commands["get_version"])
            .decode("utf-8")
            .strip()
        )
        self.set("version", v, force=True)

    def applica_aggiornamenti(self):
        configurazione_template = Configurazione()
        configurazione_template.load(CONFIG_TEMPLATE)

        for sezione_template in configurazione_template.sezioni:
            if sezione_template.id in self.sezioni.keys():
                self.sezioni.get(sezione_template.id).aggiorna(sezione_template)
            else:
                self.sezioni.append(sezione_template)

        for opzione_template in configurazione_template.opzioni:
            if opzione_template.id in self.opzioni.keys():
                self.opzioni.get(opzione_template.id).aggiorna(opzione_template)
            else:
                self.opzioni.append(opzione_template)

        del configurazione_template

    def __repr__(self):
        return "Configurazione Sistema"

    @beartype
    def get(self, id_opzione: str) -> Opzione | None:
        """
        Recupera un oggetto Opzione in base al suo ID.
        Restituisce None se l'ID non è trovato.

        :param id_opzione: Stringa che rappresenta l'ID dell'opzione interessata.

        :return: Il metodo get restituisce un'istanza della classe Opzione
                 se l'id_opzione è trovato nel dizionario self.opzioni.
                 Se l'id_opzione non viene trovato, restituisce None.
        """
        if self.opzioni.get(id_opzione) is None:
            logger.warning(f"Getter: id {id_opzione} non trovato.")
            return None

        return self.opzioni.get(id_opzione)

    @beartype
    def set(self, id_opzione: str, dati: Any, force: bool = False) -> bool:
        """
        Imposta il valore di un'opzione.

        :param id_opzione: Stringa che rappresenta l'ID dell'opzione interessata.
        :param dati: Il valore o i valori che verranno inseriti. A dipendere dal tipo
                     dell'opzione, questo parametro può essere un testo, un numero,
                     un booleano, o una lista di valori se l'opzione è composta.

        :param force: Forza l'aggiornamento di un'impostazione, anche se essa è disabilitata.

        :return: Success. Se l'id_opzione non è riconosciuto, restituisce False.
                 In caso contrario, chiama il metodo set dell'oggetto opzioni[id_opzione]
                 con il parametro dati e restituisce il risultato.
        """

        match id_opzione.split("_"):
            case [id_parent, index] if index.isdigit():
                return self.opzioni.get(id_parent).set(dati, index=int(index))

        if id_opzione not in self.opzioni.keys():
            logger.warning(f"Setter: id {id_opzione} non riconosciuto.")
            return False

        return self.opzioni.get(id_opzione).set(dati, force)

    @beartype
    def aggiorna(self, configurazione: Dict, salva=True) -> bool:
        """
        Questa funzione aggiorna le impostazioni di configurazione utilizzando un dizionario 'configurazione' che
        contiene coppie chiave-valore, dove ogni chiave rappresenta l'id di un'opzione e il valore (singolo o multiplo)
        corrispondente rappresenta il nuovo valore per quell'opzione.

        :param configurazione: Dizionario contenente i dati di configurazione da aggiornare.

        :param salva: Un flag booleano che determina se la configurazione aggiornata deve essere esportata su file.
                      (valore predefinito: True)
        :type salva: bool
        """

        for key, dati in configurazione.items():
            ok = self.set(key, dati)

            if not ok:
                return False

        if salva:
            self.esporta()

        return True

    @beartype
    def esporta(self, file: str | Path = CONFIG_FILE):
        """
        La funzione esporta esporta i dati di configurazione in un file nel formato JSON.

        :param file: Il parametro file rappresenta il percorso del file in cui i dati verranno esportati.
        :type file: str | Path
        """

        dati = {
            "sezioni": {
                s.id: {"titolo": s.titolo, "descrizione": s.descrizione}
                for s in self.sezioni
            },
            "opzioni": {o.id: o.esporta() for o in self.opzioni},
        }

        with open(file, "w", encoding="utf-8") as f:
            dump(dati, f, ensure_ascii=False, indent=2)


configurazione = Configurazione()

if "SOSTITUZIONI_SETUP" not in os.environ:
    configurazione.load()
    configurazione.applica_aggiornamenti()
