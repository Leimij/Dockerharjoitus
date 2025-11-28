# Docker Client–Server File Transfer

Tässä harjoituksessa luodaan kaksi erillistä Docker-konttia: 'palvelinkontti' ja 'asiakaskontti'.
Palvelinkontti luo 1 KB kokoisen tiedoston, jakaa sen HTTP:n kautta, ja asiakaskontti hakee sen palvelimelta, sekä tallentaa tiedoston omaan voluumiinsa (servervol).

Projektin tarkoituksena on oppia:
- Docker-kuvien rakentaminen Dockerfilen avulla
- konttien välisen kommunikoinnin samassa verkossa
- tiedonsiirto palvelimen ja asiakkaan välillä
- Docker-voluumeiden käyttö pysyvän datan tallentamiseen
- automatisointi PowerShell-skripteillä

---

## Palvelinkontti (server)

Palvelin:

1. Käynnistää Flask-pohjaisen HTTP-palvelimen
2. Luo 1 KB satunnaisen tekstin sisältävän tiedoston
3. Tallentaa sen voluumiin 'servervol' hakemistoon /serverdata
4. Laskee tiedostolle SHA256-checksumin
5. Palvelee asiakkaille kaksi endpointia:

### GET /generate
- Luo uuden 1 KB tiedoston
- Laskee tiedostolle SHA256-checksumin
- Palauttaa checksumin JSON-muodossa

### GET /file
- Palauttaa viimeksi luodun tiedoston latauksena

Palvelinkontti jää käyntiin ja odottaa asiakaskontin pyyntöjä.

---

## Asiakaskontti (client)

Asiakas:

1. Kytkeytyy samaan Docker-verkkoon kuin palvelin
2. Tekee HTTP-pyynnön palvelimen /generate -endpointiin
3. Hakee checksum-arvon
4. Lataa tiedoston /file -endpointista
5. Tallentaa sen voluumiin 'clientvol' hakemistoon /clientdata
6. Asiakaskontti ajetaan kerran ja sammutetaan

Tallennettu tiedosto jää pysyvästi voluumiin.

---

## Ajaminen ja tiedoston tarkistaminen

Tämän harjoituksen ajaminen koostuu kahdesta vaiheesta:
1) palvelinkontin käynnistäminen
2) asiakaskontin käynnistäminen ja tiedoston siirtäminen

Alapuolella ohjeet.

---

### 1. Käynnistä palvelin

Avaa oikea tiedosto sijainti Powershellissä ja aja seuraava komento:

./server.ps1

Voit tarkistaa toiminnon siirtymällä ohjelman päätteeksi tulleeseen osoitteeseen.

### 2. Käynnistä asiakas

Palaa takaisin Powershelliin ja samassa ikkunassa aja seuraava komento:

./client.ps1

Ohjelma ilmoittaa, että kaikki on onnistunut

Voit tarkistaa toiminnon tekemällä seuraavat asiat:

(ajetaan kontti väliaikaisena kohteena)

docker run -it --rm -v clientvol:/clientdata python:3.12-slim sh

(Varmista, että clientdata kansio löytyy asiaskontista)

ls clientdata

(Varmista, että clientdata kansiosta löytyy randomfile, jonka sisällä on pitkä merkkijono)

cat /clientdata/randomfile.txt

(Poistu kontin sisältä)
exit

### 3. Siivoa jälkesi

Jotta tietokoneellesi ei jää pyörimään mitään turhaa tulee meidän sulkea ja poistaa kaikki ajamamme kontit

Suorita seuraavat komennot powershellissä:

docker stop $(docker ps -q)

docker rm $(docker ps -aq)

docker network rm mynetwork

docker volume rm servervol

docker volume rm clientvol
