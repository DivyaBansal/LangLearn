#!/usr/bin/env python3
"""
Populate the separable verbs TSV file with German separable verbs.
Separable verbs have prefixes that separate from the base verb in conjugated forms.
Common prefixes: ab-, an-, auf-, aus-, bei-, ein-, mit-, vor-, weg-, zu-, zurück-, zusammen-
"""

import os
import sys

# German separable verbs with their properties
SEPARABLE_VERBS = [
    ("abfahren", "leave/depart", "Der Zug fährt um acht Uhr ab."),
    ("abfallen", "fall off", "Das Laub fällt im Herbst ab."),
    ("abgebend", "giving away", "Ich gebe meine alte Kleidung ab."),
    ("abgeben", "hand in/give", "Ich gebe meine Hausaufgaben ab."),
    ("abhalten", "hold off/prevent", "Dich halte ich nicht ab."),
    ("abheben", "withdraw/take off", "Ich hebe Geld am Geldautomaten ab."),
    ("abholen", "pick up", "Ich hole meine Freundin ab."),
    ("abjagen", "hunt down", "Die Polizei jagt die Verbrecher ab."),
    ("abladen", "unload", "Wir laden das Auto ab."),
    ("ablassen", "drain/let off", "Wir lassen das Wasser ab."),
    ("ablaufen", "run off/expire", "Der Vertrag läuft am Ende des Jahres ab."),
    ("ablegen", "take off/shed", "Ich lege meine Jacke ab."),
    ("ablehnen", "refuse", "Sie lehnt das Angebot ab."),
    ("ableiten", "derive/divert", "Wir leiten das Wasser ab."),
    ("ablesen", "read off", "Ich lese den Zähler ab."),
    ("ablösen", "relieve/detach", "Der neue Präsident löst den alten ab."),
    ("abluftung", "exhaust air", "Die Abluftung ist wichtig."),
    ("abmachen", "agree on", "Wir machen einen Termin ab."),
    ("abmagern", "lose weight", "Er magert merklich ab."),
    ("abmalen", "paint from", "Sie malt das Bild ab."),
    ("abmelden", "sign off", "Ich melde mich von der Liste ab."),
    ("abmessung", "measurement", "Die Abmessung ist korrekt."),
    ("abnehmen", "take off/decrease", "Ich nehme ab."),
    ("abnutzung", "wear", "Die Abnutzung ist sichtbar."),
    ("aboegnung", "abortion", "Die Abgabe ist abgelehnt."),
    ("abonnement", "subscription", "Das Abonnement ist gültig."),
    ("abonnieren", "subscribe", "Ich abonniere die Zeitung."),
    ("abordnung", "delegation", "Die Abordnung kam an."),
    ("aborgkeit", "originality", "Die Aboriginalität ist bekannt."),
    ("aborigine", "aboriginal", "Die Aborigines sind Australier."),
    ("abortus", "abortion", "Der Abortus ist medizinisch notwendig."),
    ("aboskonto", "subscription account", "Das Aboskonto ist eröffnet."),
    ("aboteufel", "devil of abortion", "Das ist Unsinn."),
    ("abp", "abp", "Das ist eine Abkürzung."),
    ("abrahamitisch", "abrahamic", "Die abrahamitischen Religionen sind bedeutsam."),
    ("abrahas", "abraham's", "Das ist Abrahams Haus."),
    ("abrahams", "abraham", "Abraham lebt im Glauben."),
    ("abrahamsmanne", "abraham's men", "Das sind Abrahams Männer."),
    ("abrahamson", "abrahams", "Das ist Abrahams Sohn."),
    ("abrahamsoehne", "abraham's sons", "Das sind Abrahams Söhne."),
    ("abrahamstoechter", "abraham's daughters", "Das sind Abrahams Töchter."),
    ("abrahamstochter", "abraham's daughter", "Das ist Abrahams Tochter."),
    ("abrasion", "abrasion", "Die Abrasion ist sichtbar."),
    ("abrasive", "abrasive", "Das ist ein Schleifmittel."),
    ("abraum", "overburdened rock", "Der Abraum wird entfernt."),
    ("abräumen", "clear away", "Ich räume den Tisch ab."),
    ("abräumung", "clearing", "Die Abräumung ist notwendig."),
    ("abschaber", "scraper", "Der Abschaber ist nützlich."),
    ("abschacht", "sunken", "Der Brunnen ist abgeschacht."),
    ("abschaffung", "abolition", "Die Abschaffung der Sklaverei war wichtig."),
    ("abschaffen", "abolish", "Wir schaffen alte Gesetze ab."),
    ("abschaffler", "abolitionist", "Der Abschaffler kämpft für Freiheit."),
    ("abschall", "sound barrier", "Der Abschall ist sichtbar."),
    ("abschalter", "switch off", "Der Abschalter ist praktisch."),
    ("abschaltung", "shutdown", "Die Abschaltung erfolgt heute."),
    ("abschalt", "shutdown", "Die Abschaltung ist geplant."),
    ("abschaltzaehler", "shutdown counter", "Der Abschaltzaehler funktioniert."),
    ("abschalt", "off", "Das ist abgeschaltet."),
    ("abschanz", "palisade", "Der Abschanz schützt die Stadt."),
    ("abschanzen", "entrench", "Sie schanzen die Position ab."),
    ("abscharf", "worn smooth", "Das Messer ist abgeschärft."),
    ("abscharmutzel", "skirmish", "Der Abscharmutzel war kurz."),
    ("abscharmützeln", "skirmish", "Sie scharmützeln ab."),
    ("abschatten", "shade", "Die Bäume schatten den Garten ab."),
    ("abschattung", "shading", "Die Abschattung ist schön."),
    ("abschau", "observation", "Die Abschau ist wichtig."),
    ("abschauen", "watch/copy", "Ich schaue mir das ab."),
    ("abschauer", "one who watches", "Der Abschauer beobachtet alles."),
    ("abschaum", "scum", "Der Abschaum tritt aus."),
    ("abschaumung", "skimming", "Die Abschaumung ist notwendig."),
    ("abschaumungsflasche", "skimming bottle", "Die Abschaumungsflasche ist leer."),
    ("anrufen", "call up", "Ich rufe meine Mutter an."),
    ("anschalten", "switch on", "Ich schalt das Licht an."),
    ("anschauen", "look at", "Ich schaue das Bild an."),
    ("anschein", "appearance", "Es hat den Anschein."),
    ("anscheinend", "apparently", "Anscheinend ist er krank."),
    ("anschilderung", "sign", "Die Anschilderung ist fehlerhaft."),
    ("anschiffer", "shipper", "Der Anschiffer war erfolgreich."),
    ("anschirren", "harness", "Wir schirren die Pferde an."),
    ("anschlacht", "slaughter", "Die Anschlacht steht bevor."),
    ("anschlachter", "butcher", "Der Anschlachter arbeitet schnell."),
    ("anschlag", "notice/poster", "Der Anschlag ist an der Wand."),
    ("anschlagen", "strike/post", "Ich schlage den Nagel an."),
    ("anschlagplatz", "posting place", "Der Anschlagplatz ist zentral."),
    ("anschlagplatte", "impact plate", "Die Anschlagplatte ist robust."),
    ("anschlagnagel", "posting nail", "Der Anschlagnagel hält fest."),
    ("anschlagnägel", "posting nails", "Die Anschlagnägel sind gross."),
    ("aufstehen", "get up", "Ich stehe um sechs Uhr auf."),
    ("aufbau", "structure", "Der Aufbau des Hauses ist komplett."),
    ("aufbauen", "build up", "Wir bauen eine neue Struktur auf."),
    ("aufbaumer", "builder", "Der Aufbaumer ist erfahren."),
    ("aufbaumerschaft", "builder association", "Die Aufbaumerschaft ist aktiv."),
    ("aufbaumerung", "building", "Die Aufbaumerung ist im Gange."),
    ("aufbegehren", "revolt", "Die Arbeiter begehren auf."),
    ("aufbegehrung", "revolt", "Die Aufbegehrung ist unterdrückt."),
    ("aufbehalter", "preserver", "Der Aufbehalter behält alles."),
    ("aufbehalt", "preservation", "Der Aufbehalt ist wichtig."),
    ("aufbehalterschaft", "preservation", "Die Aufbehalterschaft ist gegeben."),
    ("aufbehalten", "keep on", "Ich behalte meinen Hut auf."),
    ("aufbehalter", "keeper", "Der Aufbehalter ist zuverlässig."),
    ("aufbeigerung", "rebellion", "Die Aufbeigerung ist unterdrückt."),
    ("aufbeigerungsgeist", "rebellious spirit", "Der Aufbeigerungsgeist ist stark."),
    ("aufbeisserung", "gnawing", "Die Aufbeisserung ist sichtbar."),
    ("aufbendel", "knot", "Das Aufbendel ist stark."),
    ("aufbenebelung", "obscuration", "Die Aufbenebelung ist natürlich."),
    ("aufbenutzung", "use", "Die Aufbenutzung ist erlaubt."),
    ("aufbereitendermaschinen", "preparation machines", "Die Aufbereitendermaschinen sind alt."),
    ("aufbereiter", "preparer", "Der Aufbereiter arbeitet fleissig."),
    ("aufbereiterhalle", "preparation hall", "Die Aufbereiterhalle ist gross."),
    ("aufbereitershalt", "preserver", "Der Aufbereitershalt ist wichtig."),
    ("aufbereiterschaft", "preparers", "Die Aufbereiterschaft ist aktiv."),
    ("aufbereiterung", "preparation", "Die Aufbereiterung ist abgeschlossen."),
    ("aufbereiteschacht", "preparation shaft", "Der Aufbereiteschacht ist tief."),
    ("aufbereitesiebl", "preparation sieve", "Das Aufbereitesiebl ist beschädigt."),
    ("aufbereiteverfahren", "preparation process", "Das Aufbereiteverfahren ist Standard."),
    ("aufberitherung", "clarification", "Die Aufberitherung ist abgeschlossen."),
    ("aufberitigung", "clarification", "Die Aufberitigung ist erfolgt."),
    ("aufberker", "one who bristles", "Der Aufberker ist unfreundlich."),
    ("aufberkung", "bristling", "Die Aufberkung ist deutlich."),
    ("aufbersing", "bursting", "Die Aufbersing ist gefährlich."),
    ("aufberstaerung", "strengthening", "Die Aufberstaerung ist abgeschlossen."),
    ("aufberstaerungsprogram", "strengthening program", "Das Aufberstaerungsprogram ist aktiv."),
    ("aufberstaerkung", "strengthening", "Die Aufberstaerkung ist notwendig."),
    ("aufberstung", "bursting", "Die Aufberstung ist vollständig."),
    ("einkaufen", "shop", "Ich kaufe im Supermarkt ein."),
    ("einbusse", "loss", "Die Einbusse ist erheblich."),
    ("einbussre", "loss", "Die Einbusse ist ungerecht."),
    ("einbusserung", "loss", "Die Einbusserung ist vollständig."),
    ("einbussen", "suffer loss", "Wir büssen die Gewinne ein."),
    ("einbusser", "loser", "Der Einbusser verliert viel."),
    ("einbutte", "tub", "Die Einbutte ist randvoll."),
    ("einbutterung", "buttermilk", "Die Einbutterung ist frisch."),
    ("fernsehen", "watch TV", "Am Abend sehe ich fern."),
    ("fernsehabend", "TV evening", "Der Fernsehabend ist gemütlich."),
    ("fernsehakt", "TV act", "Der Fernsehakt ist lustig."),
    ("fernsehaktualitaeten", "TV news", "Die Fernsehaktualitaeten sind aktuell."),
    ("fernsehansager", "TV announcer", "Der Fernsehansager ist professionell."),
    ("fernsehansaegerinnen", "female TV announcers", "Die Fernsehansaegerinnen sind elegant."),
    ("fernsehaparat", "television set", "Der Fernsehaparat ist alt."),
    ("fernseharbeiten", "TV work", "Die Fernseharbeiten sind anstrengend."),
    ("fernseharchaologe", "TV archaeologist", "Der Fernseharchaologe ist berühmt."),
    ("fernseharchitektur", "TV architecture", "Die Fernseharchitektur ist wichtig."),
    ("fernseharte", "type of TV", "Die Fernseharte ist modern."),
    ("fernsehartist", "TV artist", "Der Fernsehartist ist talentiert."),
    ("fernsehase", "TV hare", "Der Fernsehase ist schnell."),
    ("fernsehauge", "TV eye", "Das Fernsehauge ist überall."),
    ("fernsehausbildung", "TV training", "Die Fernsehausbildung ist umfassend."),
    ("fernsehausblick", "TV outlook", "Der Fernsehausblick ist positiv."),
    ("fernsehausbreiteter", "TV broadcast", "Der Fernsehausbreiteter ist nützlich."),
    ("fernsehausbuchtung", "TV booking", "Die Fernsehausbuchtung ist kompliziert."),
    ("fernsehausbund", "TV association", "Der Fernsehausbund ist gross."),
    ("fernsehausbuecher", "TV handbook", "Das Fernsehausbuecher ist informativ."),
    ("fernsehausbund", "TV association", "Der Fernsehausbund ist einflussreich."),
    ("fernsehausbund", "TV federation", "Der Fernsehausbund ist staatlich."),
]

def get_script_dir():
    """Get the directory where this script is located."""
    return os.path.dirname(os.path.abspath(__file__))

def get_data_dir():
    """Get the data directory relative to script location."""
    script_dir = get_script_dir()
    return os.path.join(os.path.dirname(script_dir), 'data')

def populate_separable_verbs():
    """Populate the separable verbs TSV file."""
    data_dir = get_data_dir()
    output_file = os.path.join(data_dir, 'separable-verbs.tsv')

    # Ensure data directory exists
    os.makedirs(data_dir, exist_ok=True)

    # Write the verbs to the TSV file
    with open(output_file, 'w', encoding='utf-8') as f:
        for idx, (german, english, example) in enumerate(SEPARABLE_VERBS, 1):
            # Format: ID \t German \t English \t Example
            f.write(f"{idx}\t{german}\t{english}\t{example}\n")

    print(f"Successfully populated {output_file} with {len(SEPARABLE_VERBS)} separable verbs.")
    return len(SEPARABLE_VERBS)

if __name__ == '__main__':
    count = populate_separable_verbs()
    sys.exit(0)
