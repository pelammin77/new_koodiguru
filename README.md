# Koofiguru

Tervetuloa Koofiguruun, Django-pohjaiseen interaktiiviseen oppimisympäristöön ohjelmoinnin opetteluun. Tämä alusta on suunniteltu tarjoamaan opiskelijoille käytännönläheinen kokemus ohjelmoinnin eri osa-alueilta.

## Projektin Rakenne ja tiedostot 


### Projektin Juuressa Olevat Tiedostot ja Hakemistot

- **code_runner/**: Hakemisto, joka sisältää koodiajon hallintaan liittyvät skriptit ja moduulit.
- **koodiguru_pilot/**: Hakemisto, joka voi sisältää KoodiGururun settings liittyviä tiedostoja tai testiversioita.
- **main_app/**: Hakemisto, joka sisältää Django-sovelluksen päämoduulit, kuten models, views, ja templates.
- **staticfiles/**: Hakemisto, jossa säilytetään staattisia tiedostoja kuten CSS, JavaScript ja kuvat.

- **.env.example**: Esimerkkitiedosto ympäristömuuttujien määrittelemiseen.
- **.gitignore**: Tiedosto, joka määrittelee git-versionhallinnan ohittamat tiedostot ja hakemistot.
- **Dockerfile**: Docker-konttia varten tarvittavat määritykset projektin juuressa.
- **Dockerfile-Code-runner**: Erillinen Dockerfile koodin ajamiseen tarkoitettua palvelua varten.
- **Dockerfile-cron**: Dockerfile ajastettujen skriptien suorittamista varten.
- **README.md**: Projektin README-tiedosto, joka sisältää projektin dokumentaation.
- **docker-compose.yml**: Docker Compose -määritystiedosto palveluiden hallintaan.
- **entrypoint.sh**: Skripti, joka suoritetaan kontin käynnistyessä.
- **manage.py**: Django-projektin hallintaskripti, joka mahdollistaa erilaisten komentojen suorittamisen.
- **rebuild_and_run.sh**: Skripti, joka auttaa uudelleenrakentamaan ja suorittamaan Docker-kontin. (ei käytetä nykyään käytetään docker-compose.yml)
- **rebuild_and_run.sh.save**: Varmuuskopio rebuild_and_run.sh-skriptistä.
- **requirements.txt**: Tiedosto, joka sisältää projektin riippuvuudet, jotka asennetaan pip-komennolla.
- **sqlite_dump.sql**: SQL-tiedosto, joka sisältää SQLite-tietokannan dumppauksen.
- **update_points.py**: Python-skripti, joka suorittaa käyttäjäpisteiden päivitystoimintoja.


### main_app/
- `admin.py` - Tiedosto, jossa määritellään admin-paneelin asetukset.
- `forms.py` - Tiedosto, joka sisältää Django-lomakkeiden määritelmiä.
- `models.py` - Tiedosto, jossa määritellään Django-tietomallit.
- `urls.py` - Tiedosto URL-reittien määrittelyyn.
- `views.py` - Tiedosto, joka sisältää näkymälogiikan.
- `templates/` - Hakemisto, joka sisältää Django-mallipohjat.
- `templatetags/` - Hakemisto mukautettuja mallitagien määrittelyille.

### main_app/models.py

Tiedosto sisältää mallit, jotka määrittävät tietokantarakenteen ja liiketoimintalogiikan.

#### Models

- **User**: Laajennettu käyttäjämalli, joka sisältää roolit, käyttöoikeudet, ja lisätiedot kuten pisteet ja käyttäjätason.
- **TutorialCategory**: Malli kategorioille, joita käytetään tutoriaalien ylläpitoon.
- **Tutorial**: Sisältää ohjeiden tiedot, kuten otsikot, kuvaukset ja kategoriat.
- **TaskCategory**: Tehtäväkategoriat, jotka luokittelevat erilaiset ohjelmointitehtävät.
- **Task**: Edustaa yksittäistä ohjelmointitehtävää, joka sisältää tiedot kuten aloituskoodit ja tehtävänannon.
- **Course**: Malli kursseille, joka sisältää kurssin tiedot ja siihen liittyvät ohjeet ja tehtävät.
- **Post**: Blogipostaukset tai uutiset, joita käyttäjät ja ylläpitäjät voivat luoda.
- **Answer**: Malli vastauksille, jotka liittyvät tehtäviin.
- **TaskTest**: Yksittäiset testit tehtäville, joiden avulla varmistetaan tehtävien oikeellisuus.
- **UserCourse**: Malli käyttäjän rekisteröimille kursseille.
- **OngoingCourse**: Malli käyttäjän keskeneräisille kursseille.
- **PerformedCourse**: Malli käyttäjän suorittamille kursseille.
- **UserTask**: Seuraa käyttäjän edistymistä tehtävissä.
- **UserAnswer**: Malli käyttäjän tehtävien vastauksille.


### main_app/urls.py

Tiedosto määrittää URL-reitit Koofiguru-sovellukseen ja linkittää ne vastaaviin näkymiin. Tässä esitellään URL-reitit ja niiden toiminnot.

#### URL Configuration

- **Base URL**:
  - `""`: Tulossa pian -sivu.
  - `"start/"`: Kotisivu.

- **User Management**:
  - `"register/"`: Rekisteröintisivu.
  - `"login/"`: Kirjautumissivu.
  - `"logout/"`: Kirjautumisesta uloskirjautumissivu.
  - `"profile/"`: Käyttäjäprofiilin sivu.
  - `"edit_profile/"`: Profiilin muokkaussivu.
  - `"purchase_premium/"`: Premium-jäsenyyden ostosivu.
  - `"password_change/"`: Salasanan vaihtosivu.
  - `"report/"`: Raportointityökalun sivu.

- **Course Management**:
  - `"courses/"`: Kurssilistaussivu.
  - `"courses/<int:course_id>/"`: Yksittäisen kurssin tiedot.
  - `"add_course_to_user/<int:course_id>/"`: Lisää kurssi käyttäjälle.
  - `"remove_course/<int:course_id>/"`: Poista kurssi käyttäjältä.

- **Tutorial and Task Management**:
  - `"tutorial/<int:tutorial_id>/"`: Yksittäisen tutoriaalin tiedot.
  - `"perform_task/<int:task_id>/"`: Suorita tehtävä.
  - `"tasks/<int:task_id>/review/"`: Tehtävän tarkastelu.
  - `"update-task-status-started/"`: Aseta tehtävän tila aloitetuksi.
  - `"update-task-status-solved/"`: Aseta tehtävän tila ratkaistuksi.

- **Blog Management**:
  - `"blogi/"`: Blogipostauslista.
  - `"blogi/<int:post_id>/"`: Yksittäisen postauksen tiedot.

- **Email and Search**:
  - `"search/"`: Haku.
  - `"send-email/"`: Lähetä sähköposti.
  - `"save_editor_theme/"`: Tallenna editorin teema.
  - `"save_code/"`: Tallenna koodi.

- **Password Reset Flow**:
  - `"password_reset/"`: Salasanan palautussivu.
  - `"password_reset/done/"`: Salasanan palautuksen onnistumissivu.
  - `"reset/<uidb64>/<token>/"`: Salasanan vaihtosivu palautuslinkistä.
  - `"password_reset/complete/"`: Salasanan palautuksen valmistumissivu.

- **Activation**:
  - `"activate/<str:token>/"`: Käyttäjätilin aktivointisivu.

### Media Files

Jos sovellus on käynnissä kehitysmoodissa (`DEBUG = True`), media-tiedostot palvellaan suoraan Django-sovelluksesta.


### main_app/views.py

Tiedosto sisältää Django-näkymät, jotka hoitavat sovelluksen eri sivujen ja toimintojen pyyntöjen käsittelyn.

#### Näkymät ja niiden toiminnot

- **coming_soon**:
  - Näyttää "Tulossa pian" -sivun.
  
- **home**:
  - Näyttää kotisivun.

- **purchase_premium**:
  - Näyttää sivun, jolla käyttäjät voivat ostaa premium-jäsenyyden.

- **register_view**:
  - Rekisteröintisivu, jossa uudet käyttäjät voivat luoda käyttäjätunnuksen.
  - Lähettää aktivointi-sähköpostin käyttäjälle rekisteröinnin jälkeen.

- **activate_account**:
  - Aktivoi käyttäjän tilin käyttäen linkkiä, joka sisältää JWT-tokenin.

- **login_view**:
  - Kirjautumissivu, jossa käyttäjät voivat kirjautua sisään.

- **logout_view**:
  - Kirjaa käyttäjän ulos ja ohjaa etusivulle.

- **profile**:
  - Näyttää käyttäjän profiilisivun, jossa on tietoja käyttäjän tasosta ja edistymisestä.

- **edit_profile**:
  - Sallii käyttäjän päivittää omat profiilitiedot.

- **report_view**:
  - Raporttinäkymä ylläpitäjille näyttämään käyttäjien tilastoja ja toimintaa.

- **contact**:
  - Yhteystietosivu, jossa käyttäjät voivat lähettää viestejä ylläpitäjille.

- **post_list** ja **post_detail**:
  - Näyttää listan blogipostauksista ja yksittäisen blogipostauksen.

- **course_list** ja **course_detail**:
  - Listaa kaikki kurssit ja näyttää yksityiskohtaiset tiedot valitusta kurssista.

- **tutorial_detail**:
  - Näyttää yksityiskohtaiset tiedot valitusta tutoriaalista.

- **perform_task** ja **review_task**:
  - Mahdollistavat tehtävän suorittamisen ja tarkastelemisen.

- **save_code** ja **save_editor_theme**:
  - Tallentaa käyttäjän kirjoittaman koodin ja valitun editorin teeman.

- **update_task_status_started** ja **update_task_status_solved**:
  - Päivittää tehtävän tilan aloitetuksi tai ratkaistuksi.

- **search**:
  - Suorittaa hakutoiminnon kursseille, tehtäville ja tutoriaaleille käyttäjän antaman hakutermin perusteella.

- **send_email**:
  - Mahdollistaa sähköpostin lähettämisen käyttäjiltä ylläpitäjille.

- **Password Reset Flow**:
  - Sarja näkymiä, jotka mahdollistavat salasanan nollauksen: `PasswordResetView`, `PasswordResetDoneView`, `PasswordResetConfirmView`, ja `PasswordResetCompleteView`.

#### Autentikointi ja Turvallisuus

Useat näkymät vaativat käyttäjän olevan kirjautunut sisään (`login_required`), ja jotkut vaativat ylläpitäjäoikeuksia (`user_passes_test`). CSRF-suojaus on otettu huomioon kaikissa lomakkeissa ja AJAX-pyynnöissä.


### Koodin suorittaminen REST API:n kautta

`views.py` sisältää toiminnallisuuden koodin suorittamiselle REST API:n kautta. Tämä mahdollistaa koodin ajamisen etäpalvelimella ja on tärkeä osa sovelluksen toiminnallisuutta, kun käyttäjät suorittavat koodia interaktiivisesti.

#### Toiminnot

- **process_code_rest_api**:
  - Suorittaa annetun koodin REST API:n kautta ja käsittelee koodin syötteet sekä potentiaaliset testikoodit, jotka liittyvät tehtävään.
  - **Parametrit**:
    - `code`: Suoritettava koodi.
    - `inputs`: Lista syötteistä, jotka toimitetaan koodille.
    - `task_id`: Tehtävän tunniste, johon koodi voi liittyä.
    - `language`: Koodin ohjelmointikieli.

  - **Toiminnallisuus**:
    - Lähettää koodin, syötteet ja testikoodin JSON-muodossa etäpalvelimelle suoritettavaksi.
    - Käsittelee vastauksen ja palauttaa tuloksen JSON-muodossa.

#### Tila

Vaikka koodin suoritus REST API:n kautta onnistuu, testikoodin suorittamisessa on vielä kehitettävää. Tämä tarkoittaa, että vaikka perus suoritus toimii, niin automaattiset testit, jotka varmistavat koodin oikeellisuuden, eivät toimi odotetulla tavalla.




### main_app/code_runner.py

`code_runner.py`-moduli mahdollistaa käyttäjän kirjoittaman koodin suorittamisen turvallisessa ympäristössä. Tämä moduuli sisältää funktioita, jotka käsittelevät koodin ajamisen, syötteiden hallinnan ja potentiaalisten virheiden käsittelyn.

#### Toiminnot

- **process_code**: Suorittaa annetun koodin ja ottaa vastaan valinnaisia syötteitä sekä tehtävän, johon koodi liittyy. Tämä funktio myös valvoo koodin suoritusajan, jotta se ei ylitä määriteltyä aikarajaa.

  - **Parametrit**:
    - `code`: Käyttäjän syöttämä koodi, joka suoritetaan.
    - `inputs`: Lista syötteistä, jotka toimitetaan koodille.
    - `task`: Valinnainen `Task`-olio, johon suoritettava koodi voi liittyä.
    
  - **Toiminnallisuus**:
    - Suorittaa Python-koodin turvallisessa ympäristössä, käyttäen `exec`-funktiota.
    - Käyttää `func_timeout`-kirjastoa aikakatkaisun hallintaan, estäen koodin suorittamisen yli määritellyn ajan (1 sekunti).
    - Ottaa huomioon mahdolliset syötteet, joita koodi saattaa pyytää suorituksen aikana.
    - Käsittelee ja palauttaa mahdolliset virheet tai normaalin suorituksen tulosteen.
  
  - **Turvallisuus**:
    - Koodi suoritetaan rajatussa ympäristössä, joka estää pääsyn kriittisiin järjestelmäresursseihin.
    - Virheet ja poikkeukset käsitellään turvallisesti ja palautetaan käyttäjälle ymmärrettävässä muodossa.
   
  
### `code_runner`-app

`code_runner` on Django-app, joka on suunniteltu suorittamaan käyttäjän syöttämää koodia. Tässä appissa on seuraavat pääkomponentit:

- **models.py** - Määrittelee tietokantamallit, jotka tallentavat koodin suorituksen tulokset ja muut tarvittavat tiedot.
- **views.py** - Käsittelylogiikka, joka ottaa vastaan koodin, suorittaa sen ja palauttaa tulokset käyttäjälle.
- **urls.py** - Määrittää URL-reitit, jotka ovat käytössä `code_runner`-sovelluksessa.
- **tests.py** - Sisältää yksikkötestit sovelluksen toiminnan varmistamiseksi.
- **execution_utils.py** - Apufunktiot koodin suorittamisen tukemiseen.


## Vaatimukset

- Python 3
- Django
- Muut riippuvuudet, jotka löytyvät `requirements.txt` -tiedostosta

### Asennus

1. Kloonaa tämä repositorio:


## Tekijä

Petri Lamminaho
- Sähköposti: [lammpe77@gmail.com](mailto:lammpe77@gmail.com)
