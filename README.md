# MobilePlatform

Platforma Mobilna

# Ważne repozytoria

W razie problemów ze środowiskiem głowicy lub serwerem Nginx, instalacja wszystkich bibliotek i zasobów została opisana pod linkiem: 
https://github.com/Pinjesz/PiProject/tree/main

Kod odpowiedzialny za podwozie znajduje się pod linkiem:
https://github.com/Szewoj/MARMOT-grasshopper/tree/main

Aplikacja kokpitu sterowniczego powinna zostać zainstalowana na komputerze osobistym zgodnie z instrukcją pod poniższym linkiem:
https://github.com/pkacperski/mobile-platform-repo

# Podłączenie platformy
Aby móc komunikować się z komputerami platformy należy podłączyć się do nich z poziomu komputera osobistego. Poniżej znajduje się instrukcja podłączenia do komputerów Raspberry Pi:
1. Podłącz komputer Raspberry Pi do zasilania.
2. Podłącz Raspberry Pi przez Ethernet do routera.
3. Sprawdź IP podłączonego Raspberry Pi.
4. Podłącz się przez SSH za pomocą jakiegoś programu (np. puTTY)<br>
   Raspberry Pi głowicy:<br> 
   login: ```pi```<br>
   hasło: ```raspberrypi```<br>
   Raspberry Pi platformy:<br>
   login: ```pi```<br>
   hasło: ```raspberry```<br>
5. W pliku wpa-supplicant należy dodać swoją sieć Wi-Fi komendą ```sudo nano /etc/wpa_supplicant/wpa_supplicant.conf```
# Sterowanie platformą

Poniżej znajduje się instrukcja uruchomienia sterowania platformą z poziomu komputera osobistego:
1. Podłącz kontroler do komputera osobistego.
2. Włącz i podłącz się do komputerów Raspberry Pi, upewnij się że wszystkie podłączenia elektryczne są w porządku.
3. Na RPi głowicy włącz serwer Nginx komendą ```sudo nginx -c /etc/nginx/nginx.conf```
4. Na RPi głowicy włącz odbieranie i przesyłanie obrazu na RPi głowicy za pomocą komendy ```python server/MPcomms/camera_server.py```. Mogą pojawić się błędy związane z kamerą, wówczas należy sprawdzić podłączenie złącza głowicy do pinów RPi.
5. Na RPi pojazdu włącz plik w ścieżce ```MARMOT-grasshopper-main/radio-all.py``` odpowiedzialny za sterowanie.
6. Na komputerze osobistym uruchom plik ```jetson/controler.py```

Sterowanie:<br>
• lewy drązek analogowy - ruch kół lewo/prawo,<br>
• prawy drązek analogowy - pochylanie podwozia,<br>
• lewy przycisk spustowy - ruch platformy do tyłu,<br>
• prawy przycisk spustowy - ruch platformy do przodu,<br>
• przyciski kierunkowe D-Pad - ruch głowicą lewo/prawo i góra/dół,<br>
• lewy przycisk ramienia - tryb manualny ruchu głowicy,<br>
• prawy przycisk spustowy - tryb autonomiczny ruchu głowicy.<br>

By uruchomić możliwość manualnego i autonomicznego sterowania głowicą, należy na komputerze osobistym zamiast ```controler.py``` uruchomić ```kamera.py```.




Na
Następnie należy ur

# Konstrukcja i dekonstrukcja platformy
By rozdzielić Platformę Mobilną na pojazd i głowicę, należy wpierw odłączyć wszelkie połączenia elektryczne mikrokomputerów z powerbankiem oraz baterią. By odłączyć platformę łączącą od pojazdu, należy odkręcić wszystkie śrubki w dolnej części platformy, łączące czarne plastikowe uchwyty z ramą podwozia (zdjęcie niżej). Wówczas można będzie ostrożnie zdjąć łącznik i głowicę z pojazdu. 
![demontaz](demontaz1.png)

Zaleca się niezdejmowania głowicy z platformy łączącej. Konstrukcja ta zapewnia, że podczas pracy nad głowicą przewody wychodzące spod zielonej podstawki głowicy nie są przyciskane przez głowicę do powierzchni stołu. 

By zdjąć głowicę z platformy łączącej należy odkręcić śruby w górnej części uchwytów oraz śruby znajdujące się w środkowej części jednego z uchwytów (zdjęcie niżej), w taki sposób, by możliwe było wysunięcie głowicy z platformy łączącej. Należy przy tym uważać na kable znajdujące się pod zieloną podstawką głowicy. Po demontażu zaleca się umieścić głowicę na jakimś podwyższeniu tak, aby przewody wychodzące od spodu nie były przygniatane przez głowicę do stołu.
![demontaz](demontaz2.png)

