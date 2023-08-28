import urllib.request, json


url = "https://api.themoviedb.org/3/discover/movie?sort_by=popularity.desc&api_key=f99dbb8745b326c616475a6b60bad2a0"

resposta = urllib.request.urlopen(url)

dados = resposta.read()

jsondata = json.loads(dados)

print(jsondata['results'])
