# AI Tartalomgenerátor

Ez a projekt egy Flask-alapú backend és egy frontend alkalmazásból áll, amelyek együttműködve lehetővé teszik közösségi média posztok generálását a Cohere AI segítségével.

## 📦 Telepítés

### 1. Előfeltételek

- [Docker](https://www.docker.com/) és [Docker Compose](https://docs.docker.com/compose/) telepítése
- Egy érvényes Cohere API kulcs beszerzése: [https://cohere.com](https://cohere.com)

### 2. Projekt klónozása

```bash
git clone https://github.com/felhasznalonev/projekt-nev.git
cd projekt-nev
```

### 3. .env file hozzáadása

Hozz létre egy .env fájlt a projekt gyökérkönyvtárában a következő tartalommal:

env:
COHERE_API_KEY=ide_írd_be_a_saját_api_kulcsodat


### 4. indítás docker compose -al 
A konténerek építéséhez és futtatásához használd az alábbi parancsot:

bash: 
docker-compose up --build

Ez elindítja:

a backendet a http://localhost:5000 címen,

a frontendet a http://localhost:3000 címen.

### Használat
Nyisd meg a böngésződben a http://localhost:3000 oldalt.

Add meg a bemeneteket:

Kampányüzenet (pl. egy kezdő állatotthonhoz önkéntesek toborozása hétvégére 8 órában)

Célközönség (pl. állatbarátok)

Hangnem (pl. kedves)

Emojik használata (✅ vagy ❌)

Kattints a „Generálás” gombra.

A rendszer automatikusan legenerálja a közösségi posztokat Facebookra, Instagramra, LinkedInre és X-re (Twitter).


Tesztelés curl-lal vagy PowerShellből

```
PowerShell példa:
Invoke-WebRequest -Uri "http://localhost:5000/generate" -Method POST `
-ContentType "application/json" `
-Body (@{
    message = "egy kezdő állatotthonhoz önkéntesek toborozása hétvégére 8 órában"
    audience = "állatbarátok"
    tone = "kedves"
    emojis = $true
} | ConvertTo-Json -Depth 10) | Select-Object -Expand Content

```



NÉHA ELŐFORDULHAT HOGY ELSŐRE NEM MŰKÖDIK
