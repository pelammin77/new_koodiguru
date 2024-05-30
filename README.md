# Koofiguru

Tervetuloa Koofiguruun, Django-pohjaiseen interaktiiviseen oppimisympäristöön ohjelmoinnin opetteluun. Tämä alusta on suunniteltu tarjoamaan opiskelijoille käytännönläheinen kokemus ohjelmoinnin eri osa-alueilta.

## Projektin Rakenne ja tiedostot 

Tässä on yleiskatsaus Koofiguru-projektin tiedostorakenteesta:

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



## Vaatimukset

- Python 3
- Django
- Muut riippuvuudet, jotka löytyvät `requirements.txt` -tiedostosta

### Asennus

1. Kloonaa tämä repositorio:


## Tekijä

Petri Lamminaho
- Sähköposti: [lammpe77@gmail.com](mailto:lammpe77@gmail.com)
