# downloadBGTfromPDOK
Dit Python-script downloadt BGT-gegevens van PDOK voor een specifiek gebied. Het script is eenvoudig aan te passen voor verschillende polygonen en gegevensformaten (citygml, gml, json).

Functies
Dynamische featurelijst: Haalt automatisch de meest actuele lijst van beschikbare gegevens op.
Gegevensformaten: Ondersteunt citygml, gml, en json.
Volledig downloadproces: Creëer een downloadverzoek, controleer de status, en download het bestand.
Vereisten
Python 3.x
requests library (pip install requests)
Gebruik
Script kopiëren en aanpassen: Stel de coördinaten en het gegevensformaat in.

Script uitvoeren:
python bgt_downloader.py
Het gedownloade bestand wordt opgeslagen op C:/temp/downloaded_file.zip. Pas deze locatie aan indien nodig.

Aanpassen
Featuretypes: Voeg extra features toe of verwijder deze in het script.

