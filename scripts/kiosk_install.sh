#!/bin/bash

# aggiorna e installa pacchetti necessari
apt-get update
apt-get install \
  xorg \
  lightdm \
  openbox \
  autorandr \
  sed \
  unclutter \
  chromium \
  -y

# crea gruppo
/sbin/groupadd scuolasync

# crea utente
/sbin/useradd -m scuolasync -g scuolasync -s /bin/bash

# imposta permessi
# fix per chromium che altrimenti ci sputa
# sarebbe meglio utilizzare chown e dare i permessi all'utente, ma chown non funziona subito dopo aver creato l'utente, todo trovare fix
mkdir -p /home/scuolasync/.config/chromium
chmod -R 777 /home/scuolasync/.config/chromium

# rimuovi console virtuale
cat > /etc/X11/xorg.conf << EOF
Section "ServerFlags"
    Option "DontVTSwitch" "true"
EndSection
EOF

# crea configurazione lightdm
cat > /etc/lightdm/lightdm.conf << EOF
[SeatDefaults]
autologin-user=scuolasync
user-session=openbox
EOF

# input da utente del sito web
read -p "Inserire l'url di base del sito (senza https://): " url
# input da utente per il codice di autorizzazione
read -p "Inserire il codice di autorizzazione (oppure premere invio per non utilizzarlo): " code


# creazione script di avvio openbox
mkdir -p /home/scuolasync/.config/openbox

cat > /home/scuolasync/.config/openbox/autostart << EOF
#!/bin/bash

# ---- variabili -----

# codice di autorizzazione definito nelle impostazioni del sito
code="$code"
url="https://$url/display?code=\$code"

# --------------------

# mantieni lo schermo attivo
xset s noblank
xset s off
xset -dpms

# Chiudi sessione con Ctrl-Alt-Backspace
setxkbmap -option terminate:ctrl_alt_bksp

# nascondi il cursore
unclutter -idle 0.1 -root &

while :
do
  # setup e aggiornamento display
  autorandr clone-largest

  # rimuovi flag di chromium per non far mostrare dialoghi
  sed -i 's/"exited_cleanly":false/"exited_cleanly":true/' /home/scuolasync/.config/chromium/Default/Preferences
  sed -i 's/"exit_type":"Crashed"/"exit_type":"Normal"/' /home/scuolasync/.config/chromium/Default/Preferences

  # avvia chromium in modalità kiosk a schermo intero
  chromium \\
    --no-first-run \\
    --start-maximized \\
    --noerrdialogs \\
    --disable-translate \\
    --disable-infobars \\
    --disable-suggestions-service \\
    --disable-save-password-bubble \\
    --disable-session-crashed-bubble \\
    --kiosk \$url

  # delay per il riavvio in caso di errore o chiusura manuale
  sleep 5
done &
EOF

echo "Installazione completata! Riavviare il sistema per avviare il kiosk."