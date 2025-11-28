Write-Host "Pysaytetaan ja poistetaan 'servercontainer' -niminen kontti (jos on kaynnissa)"
docker rm -f servercontainer 2>$null

Write-Host "Luodaan verkko nimelta mynetwork"
docker network create mynetwork 2>$null

Write-Host "Luodaan voluumi nimelta 'servervol'"
docker volume create servervol 2>$null

Write-Host "Sovellus rakentaa server-imagen 'myserver' Dockerfile -tiedoston maarityksilla (kayttaen pohjana python:3.12 slimmia)"
docker build -t myserver ./server

Write-Host "Kaynnistetaan palvelin kontti 'servercontainer'"
docker run -d `
  --name servercontainer `
  --network mynetwork `
  -p 8080:8080 `
  -v servervol:/serverdata `
  myserver

Write-Host "`nPalvelin on kaynnistetty! Odotetaan kayttajan pyyntöa..."
Write-Host "Varmista, etta palvelin toimii oikein: http://localhost:8080/generate"
