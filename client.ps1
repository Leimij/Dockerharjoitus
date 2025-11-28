Write-Host "Pysaytetaan ja poistetaan 'clientcontainer' kontti (jos on kaynnissa)..."
docker rm -f clientcontainer 2>$null

Write-Host "Luodaan voluumi nimelta 'clientvol'..."
docker volume create clientvol 2>$null

Write-Host "Rakennetaan client-image 'myclient' Dockerfile-maarityksilla (python:3.12-slim)..."
docker build -t myclient ./client

Write-Host "Kaynnistetaan asiakas kontti 'clientcontainer', joka liitetaan mynetwork-verkkoon..."
docker run `
  --name clientcontainer `
  --network mynetwork `
  -v clientvol:/clientdata `
  myclient

Write-Host "`nAsiakasohjelma suoritettu!"
Write-Host "Tiedosto loytyy voluumista clientvol: /clientdata/randomfile.txt"
