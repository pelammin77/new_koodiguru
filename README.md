# Koofiguru

Tervetuloa Koofiguruun, Django-pohjaiseen interaktiiviseen oppimisympäristöön ohjelmoinnin opetteluun. Tämä alusta on suunniteltu tarjoamaan opiskelijoille käytännönläheinen kokemus ohjelmoinnin eri osa-alueilta.

## Projektin Rakenne

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

## Vaatimukset

- Python 3
- Django
- Muut riippuvuudet, jotka löytyvät `requirements.txt` -tiedostosta

### Asennus

1. Kloonaa tämä repositorio:


## Tekijä

Petri Lamminaho
- Sähköposti: [lammpe77@gmail.com](mailto:lammpe77@gmail.com)
