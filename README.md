# Fake mails
The goal of this project is to develop a machine learning based mechanism for detection of fake news e-mails. <br>
The project is structured as follows: <br>

1. First part of this project is focusing on web scraping of fake emails from a database made by Czech elves (Čeští elfové). See modules *scrape.py* and *utils.py* for details.
2. Second part is a data visulization module. See *data_visualize.py* if interested.
3. Third part, that is under development right now, is a machine learning algorithm for detecting fake news emails.<br>

If you want to contribute to this project, I will be more than happy. Please write me at analyza (dot) fakenews (at) gmail (again dot) com.<br>

# Preliminary findings
Based on my results I argue that:
1. Amount of detected fake-news emails significantly grew after:
    - Removal of a statue of general Konev in Prague. https://www.reuters.com/article/us-czech-russia-monument-idUSKCN1VX2FI
    - Build of a statue of Russian Liberation Army (Vlasov army) in Řeporyje. https://english.radio.cz/reporyje-build-memorial-honouring-vlasov-troops-who-helped-liberation-prague-8113168
    - Ricin plot and expel of 2 GRU agents. https://www.nytimes.com/2020/06/05/world/europe/czech-republic-russia-ricin.html
    - Elections in the Czech Republic
    - GRU attack in Vrbětice and expel of 81 Russians agents and diplomats. https://www.nytimes.com/2021/04/17/world/europe/czech-republic-skirpal-russia-gru.html?action=click&module=In%20Other%20News&pgtype=Homepage