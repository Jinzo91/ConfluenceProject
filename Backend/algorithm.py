import nltk
from nltk.text import TextCollection
from nltk.tokenize import word_tokenize
from bs4 import BeautifulSoup

text1 = "<p>Die Change Tracker Tabelle in der Datenbank hat im Auslieferungszustand keine Indizes. Sobald die Tabelle w&auml;chst, "
text2 = "The Georgetown experiment in 1954 involved fully automatic translation of more than sixty Russian sentences into English. The authors claimed that within three or five years, machine translation would be a solved problem.[2] However, real progress was much slower, and after the ALPAC report in 1966, which found that ten-year-long research had failed to fulfill the expectations, funding for machine translation was dramatically reduced. Little further research in machine translation was conducted until the late 1980s, when the first statistical machine translation systems were developed."
text3 = "During the 1970s, many SAP SAP SAP SAP SAPprogrammers began to write conceptual ontologies, which structured real-world information into computer-understandable data. Examples are MARGIE (Schank, 1975), SAM (Cullingford, 1978), PAM (Wilensky, 1978), TaleSpin (Meehan, 1976), QUALM (Lehnert, 1977), Politics (Carbonell, 1979), and Plot Units (Lehnert 1981). During this time, many chatterbots were written including PARRY, Racter, and Jabberwacky。"



def main():
    title = "SAP Tutorial"
    texts = title + ' ' + """<ac:layout><ac:layout-section ac:type="two_right_sidebar"><ac:layout-cell><ac:structured-macro ac:macro-id="4ed42514-81c9-40e8-a5b5-aad437c3b2cf" ac:name="details" ac:schema-version="1"><ac:parameter ac:name="hidden">true</ac:parameter><ac:parameter ac:name="label" /><ac:rich-text-body><table><tbody><tr><th>Link</th><td><img height="16px" src="http://scn.sap.com/favicon.ico" /><a href="http://scn.sap.com/docs/DOC-63551">scn.sap.com/docs/DOC-63551</a></td></tr><tr><th>Date</th><td>Jun 29, 2015</td></tr></tbody></table></ac:rich-text-body></ac:structured-macro><div class="sharelinks-link-meta-data"><ac:structured-macro ac:macro-id="d654402a-a46a-4e8d-803d-9b624cf23b50" ac:name="panel" ac:schema-version="1"><ac:rich-text-body><h3><ac:image ac:align="right"><ri:url ri:value="http://scn.sap.com/people/gowdatimma.ramu/avatar/social.png?a=21920" /></ac:image></h3><p><ac:image ac:width="16"><ri:url ri:value="http://scn.sap.com/favicon.ico" /></ac:image>&nbsp;<a href="http://scn.sap.com/docs/DOC-63551">scn.sap.com/docs/DOC-63551</a></p><blockquote><p>SAP Lumira, Server for BI Platform is the new integration of SAP Lumira with the SAP BI 4.1 Platform.    This solution enables consumption and governance of SAP Lumira content from the SAP BI 4.1 plat...</p></blockquote><p><strong><a href="http://scn.sap.com/docs/DOC-63551">Verkn&uuml;pfung &ouml;ffnen</a></strong></p></ac:rich-text-body></ac:structured-macro></div><p>&nbsp;</p></ac:layout-cell><ac:layout-cell><p>&nbsp;</p></ac:layout-cell></ac:layout-section></ac:layout>"""
    soup = BeautifulSoup(texts, 'html.parser')
    soup = soup.get_text()
    print(soup)
    soup = word_tokenize(soup)
    print(soup)
    documents = TextCollection(soup)
    nouns = [word for (word,pos) in nltk.pos_tag(documents) if pos[0] == 'N']
    print(documents)
    for i, words in enumerate(documents):
        print("Top words in document {}".format(i + 1))
        scores = {word: documents.tf_idf(word, soup) for word in words}
        print(scores)
        sorted_words = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        print(sorted_words)
        for word, score in sorted_words[:]:
            if any(word in soup for word in nouns):
                print(word)
                print("\tWord: {}, TF-IDF: {}".format(word, round(score, 5)))

    #print(text2.tags)

if __name__ == "__main__":
    main()
