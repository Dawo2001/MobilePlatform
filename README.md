# Platforma Mobilna

Kod do sterowania głowicą oraz pojazdem Platformy Mobilnej.

English version below.

# Informacje ogólne
Owo repozytorium zawiera dwa foldery przeznaczone do umieszczenia w dwóch różnych komputerach.<br><br>
Folder ```jetson``` obsługuje poruszanie platformą z poziomu komputera osobistego bądź, po skonfigurowaniu, komputera Nvidia Jetson Nano. Folder należy przenieść do odpowiedniego komputera i z jego poziomu uruchamiać opisywane niżej skrypty.<br><br>
Folder ```server``` posiada pliki, które na moment zakończenia pracy nad moją pracą dyplomową (wrzesień 2024), znajdują się na komputerze Raspberry Pi podłączonym do głowicy Platformy Mobilnej, w folderze również nazwanym ```server```.<br><br>
Znajdujące się w tym repozytorium skrypty, z dodatkiem skryptów znajdujących się już na komputerach Platformy, pozwalają na poruszanie Platformą zdalnie za pomocą kontrolera oraz obsługę algorytmu śledzenia znaczników. W celu uzyskania dodatkowych funkcjonalności poniżej zamieściłem łącza do pozostałych repozytoriów, z których korzystałem, a które mogą być także przydatne w dalszej pracy.<br>                                                                                                                                                                                                                                            
Repozytorium z inicjalizacją i sterowaniem głowicą: [https://github.com/Pinjesz/PiProject/tree/main](https://github.com/Pinjesz/PiProject.git)

Repozytorium z kodem odpowiedzialnym za podwozie: [https://github.com/Szewoj/MARMOT-grasshopper/tree/main](https://github.com/Szewoj/MARMOT-grasshopper.git)

Repozytorium z aplikacją kokpitu sterowniczego: [https://github.com/pkacperski/mobile-platform-repo](https://github.com/pkacperski/mobile-platform-repo.git)

# Dependencies
Na komputerze osobistym należy zainstalować:<br>
• Python
```sudo apt install python3```<br>
• OpenCV
```$ sudo apt-get install python3-opencv```<br>
Na komputerach Platformy Mobilnej środowisko powinno być już przygotowane do dalszej pracy. Jeśli nie - należy zainstalować potrzebne biblioteki zgodnie z instrukcjami we wspomnianych wcześniej repozytoriach.



# Elementy platformy

Dokładny opis Platformy Mobilnej, wraz ze wszystkimi elementami, połączeniami i działaniem można znaleźć w mojej pracy dyplomowej pt. "Integracja zrealizowanej głowicy pan-tilt z nową platformą mobilną".

Platforma Mobilna składa się z:<br>
• głowicy, która posiada silniki krokowe i kamery, działa na Raspberry Pi głowicy, zasilana jest z dołączonej do platformy baterii i powerbanka,<br>
• pojazdu, który posiada serwomechanizmy i silniki krokowe, działa na Raspberry Pi pojazdu, zasilany jest z powerbanka i umieszczonej w ramie pojazdu baterii.<br>

Do uruchomienia platformy niezbędny jest komputer osobisty i dostęp do Wi-Fi. Do dyspozycji jest również komputer Nvidia Jetson Nano, na którym według założeń projektu będą umieszczane wszelkie złożone algorytmy sterowania i autonomii platformy.






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
Do sterowania platformą wymagany jest kontroler do gier. Musi być on tak skonfigurowany, by mógł być wykryty przez klasę XboxController (więcej informacji w https://github.com/bzier/TensorKart/blob/master/utils.py).

Poniżej znajduje się instrukcja uruchomienia sterowania platformą z poziomu komputera osobistego:
1. Podłącz kontroler do komputera osobistego.
2. Włącz i podłącz się do komputerów Raspberry Pi, upewnij się że wszystkie podłączenia elektryczne są w porządku.
3. Na RPi głowicy włącz serwer Nginx komendą ```sudo nginx -c /etc/nginx/nginx.conf```
4. Na RPi głowicy włącz odbieranie i przesyłanie obrazu na RPi głowicy za pomocą komendy ```python server/MPcomms/camera_server.py```. Mogą pojawić się błędy związane z kamerą, wówczas należy sprawdzić podłączenie złącza głowicy do pinów RPi.
5. Na RPi pojazdu włącz plik w ścieżce ```MARMOT-grasshopper-main/radio-all.py``` odpowiedzialny za sterowanie.
6. Na komputerze osobistym uruchom plik ```jetson/controler.py```

Sterowanie:<br>
• lewy drążek analogowy - ruch kół lewo/prawo,<br>
• prawy drążek analogowy - pochylanie podwozia,<br>
• lewy przycisk spustowy - ruch platformy do tyłu,<br>
• prawy przycisk spustowy - ruch platformy do przodu,<br>
• przyciski kierunkowe D-Pad - ruch głowicą lewo/prawo i góra/dół,<br>
• lewy przycisk ramienia - tryb manualny ruchu głowicy,<br>
• prawy przycisk spustowy - tryb autonomiczny ruchu głowicy.<br>

By uruchomić możliwość manualnego i autonomicznego sterowania głowicą, należy na komputerze osobistym zamiast ```controler.py``` uruchomić ```kamera.py```. Wówczas po odczekaniu do komputera osobistego zostanie przesyłany obraz z kamer platformy i po zmianie trybu sterowania na autonomiczny możliwe będzie śledzenie tarczki pomiarowej przez głowicę.





# Konstrukcja i dekonstrukcja platformy
By rozdzielić Platformę Mobilną na pojazd i głowicę, należy wpierw odłączyć wszelkie połączenia elektryczne mikrokomputerów z powerbankiem oraz baterią. By odłączyć platformę łączącą od pojazdu, należy odkręcić wszystkie śrubki w dolnej części platformy, łączące czarne plastikowe uchwyty z ramą podwozia (zdjęcie niżej). Wówczas można będzie ostrożnie zdjąć łącznik i głowicę z pojazdu. 

![demontaz](demontaz1.png)

Zaleca się niezdejmowania głowicy z platformy łączącej. Konstrukcja ta zapewnia, że podczas pracy nad głowicą przewody wychodzące spod zielonej podstawki głowicy nie są przyciskane przez głowicę do powierzchni stołu. 

By zdjąć głowicę z platformy łączącej należy odkręcić śruby w górnej części uchwytów oraz śruby znajdujące się w środkowej części jednego z uchwytów (zdjęcie niżej), w taki sposób, by możliwe było wysunięcie głowicy z platformy łączącej. Należy przy tym uważać na kable znajdujące się pod zieloną podstawką głowicy. Po demontażu zaleca się umieścić głowicę na jakimś podwyższeniu tak, aby przewody wychodzące od spodu nie były przygniatane przez głowicę do stołu.

![demontaz](demontaz2.png)



<br><br><br><br><br>












# Mobile Platform
Code for controlling the head and the vehicle of the Mobile Platform.



# General Information

This repository contains two folders intended for placement on two different computers.

The ```jetson``` folder manages platform movement from a personal computer or, once configured, an Nvidia Jetson Nano. This folder should be transferred to the appropriate computer, from which the scripts described below should be run.

The ```server``` folder contains files which, as of the completion of my thesis work (September 2024), are located on the Raspberry Pi computer connected to the head of the Mobile Platform, in a folder also named ```server```.

The scripts in this repository, together with scripts already on the Platform’s computers, enable remote control of the Platform using a controller and support for a marker-tracking algorithm. For additional functionalities, I have included links below to other repositories I used, which may also be helpful for future work.


Repository for initialization and head control: [https://github.com/Pinjesz/PiProject/tree/main](https://github.com/Pinjesz/PiProject.git)

Repository with code responsible for the chassis: [https://github.com/Szewoj/MARMOT-grasshopper/tree/main](https://github.com/Szewoj/MARMOT-grasshopper.git)

Repository with the control cockpit application: [https://github.com/pkacperski/mobile-platform-repo](https://github.com/pkacperski/mobile-platform-repo.git)






# Dependencies
On a personal computer, you need to install:<br> 
• Python ```sudo apt install python3```<br> 
• OpenCV ```$ sudo apt-get install python3-opencv```<br> 
On the Mobile Platform computers, the environment should already be prepared for further work. If not, you need to install the required libraries according to the instructions in the previously mentioned repositories.





# Components of the Platform
A detailed description of the Mobile Platform can be found in my thesis titled "Integration of the Developed Pan-Tilt Head with the New Mobile Platform."

The Mobile Platform consists of:<br> 
• a head that has stepper motors and cameras, operates on the head's Raspberry Pi, and is powered by the battery and power bank attached to the platform,<br> 
• a vehicle that has servomechanisms and stepper motors, operates on the vehicle's Raspberry Pi, and is powered by a power bank and a battery mounted in the vehicle's frame.<br>

To operate the platform, a personal computer and access to Wi-Fi are essential. There is also an Nvidia Jetson Nano computer available, where, according to the project assumptions, all complex control and autonomy algorithms for the platform will be placed.





# Connecting the Platform
To communicate with the platform computers, you need to connect to them from a personal computer. Below are the instructions for connecting to Raspberry Pi computers:<br>

1. Connect the Raspberry Pi computer to power.<br>
2. Connect the Raspberry Pi to the router via Ethernet.<br>
3. Check the IP address of the connected Raspberry Pi.<br>
4. Connect via SSH using a program (e.g., puTTY)<br>head's Raspberry Pi:<br> login: ```pi```<br> password: ```raspberrypi```<br> vehicle's Raspberry Pi:<br> login: ```pi```<br> password: ```raspberry```<br>
6. In the file wpa-supplicant, add your Wi-Fi network with the command ```sudo nano /etc/wpa_supplicant/wpa_supplicant.conf```.<br>

# Controlling the Platform
To control the platform, a game controller is required. It must be configured so that it can be detected by the XboxController class (more information at https://github.com/bzier/TensorKart/blob/master/utils.py).

Below are the instructions to start controlling the platform from a personal computer:

1. Connect the controller to the personal computer.
2. Turn on and connect to the Raspberry Pi computers, ensuring that all electrical connections are secure.
3. On the head's RPi, start the Nginx server with the command ```sudo nginx -c /etc/nginx/nginx.conf```.
4. On the head's RPi, start receiving and transmitting the image on the head's RPi using the command ```python server/MPcomms/camera_server.py```. If there are any camera-related errors, check the connection of the head's connector to the RPi pins.
5. On the vehicle's RPi, run the file located at ```MARMOT-grasshopper-main/radio-all.py``` responsible for vehicle's control.
6. On the personal computer, run the file ```jetson/controler.py```.<br>
Controls:<br>
• left analog stick - wheel movement left/right,<br>
• right analog stick - chassis tilting,<br>
• left trigger - move the platform backward,<br>
• right trigger - move the platform forward,<br>
• D-Pad directional buttons - move the head left/right and up/down,<br>
• left shoulder button - manual mode for head movement,<br>
• right trigger - autonomous mode for head movement.<br>

To enable manual and autonomous control of the head, instead of ```controler.py```, run ```kamera.py``` on the personal computer. After waiting, the image from the platform's camera will be sent to the personal computer, and by switching to autonomous control mode, the head will be able to track the measurement target.






# Construction and Deconstruction of the Platform
To separate the Mobile Platform into the vehicle and the head, you must first disconnect all electrical connections between the microcontrollers, the power bank, and the battery. To detach the connecting platform from the vehicle, remove all screws at the bottom of the platform that connect the black plastic holders to the chassis frame (see the picture below). This will allow you to carefully remove the connector and the head from the vehicle.


It is recommended not to remove the head from the connecting platform. This design ensures that while working on the head, the wires coming from under the green base of the head are not pressed down against the table surface by the head.

![demontaz](demontaz1.png)

To remove the head from the connecting platform, unscrew the screws at the top of the holders and the screws located in the middle section of one of the holders (see the picture below) so that the head can be slid out of the connecting platform. Care must be taken with the cables located under the green base of the head. After disassembly, it is recommended to place the head on a raised surface to prevent the wires coming from underneath from being crushed against the table by the head.

![demontaz](demontaz2.png)
