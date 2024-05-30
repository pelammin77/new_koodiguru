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


## Vaatimukset

- Python 3
- Django
- Muut riippuvuudet, jotka löytyvät `requirements.txt` -tiedostosta

### Asennus

1. Kloonaa tämä repositorio:


## Tekijä

Petri Lamminaho
- Sähköposti: [lammpe77@gmail.com](mailto:lammpe77@gmail.com)
