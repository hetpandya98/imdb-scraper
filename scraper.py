import requests
from bs4 import BeautifulSoup
import config
import json

class ImdbScraper:
    def __init__(self, link, token, id):
        self.titles = []
        self.links = []
        self.genre = []
        self.status = []
        self.description = []
        self.directors_list = []
        self.cast_list = []
        self.changes = []
        self.filters = ['WES ANDERSON', 'Robert Pattinson', 'Sam MeNDes', 'pATTY jenKins', 'yiFei Liu']
        self.apply_filters = True
        self.present = {}
        self.url = link
        self.bot_token = token
        self.bot_chatID = id


    def getHTMLContent(self):
        page = requests.get(self.url)
        soup = BeautifulSoup(page.content, 'html.parser')
        return soup.find_all("div", {"class":"lister-item-content"})


    def populate(self, results):
        for i in range(len(results)):
            self.titles.append(results[i].h3.a.text)
            self.links.append("https://www.imdb.com" + results[i].h3.a['href'])
            p_content = results[i].find_all("p")

            try:
                temp = p_content[0].find("span", {"class":"genre"}).text[1::]
                temp = temp[:-12]
                self.genre.append(temp)
            except:
                self.genre.append("")
            try:
                self.status.append(p_content[0].b.text)
            except:
                self.status.append("")
            
            try:
                self.description.append(p_content[1].text[5::])
            except:
                self.description.append("")

            delimeter = False
            directors = ""
            cast = ""
            try:
                for j in range(len(p_content[2].text)):
                    if p_content[2].text[j] == '\n':
                        continue
                    if p_content[2].text[j] == '|':
                        delimeter = True
                        continue
                    if delimeter:
                        cast = cast + p_content[2].text[j]
                    else:
                        directors = directors+p_content[2].text[j]
                self.directors_list.append(directors[13::])
                self.cast_list.append(cast[11::])
            except:
                self.directors_list.append("")
                self.cast_list.append("")


    def getData(self):
        movies_list = []
        for i in range(len(results)):
            movie = {}
            if self.titles[i] == "":
                movie["title"] = "Unknown"
            else:
                movie["title"] = self.titles[i]
            
            if self.links[i] == "":
                movie["link"] = "Unknown"
            else:
                movie["link"] = self.links[i]
            
            if self.genre[i] == "":
                movie["genre"] = "Unknown"
            else:
                movie["genre"] = self.genre[i]
            
            if self.status[i] == "":
                movie["status"] = "Unknown"
            else:
                movie["status"] = self.status[i]
            
            if self.description[i] == "":
                movie["description"] = "Unknown"
            else:
                movie["description"] = self.description[i]
            
            if self.directors_list[i] == "":
                movie["directors"] = "Unknown"
            else:
                movie["directors"] = self.directors_list[i]

            if self.cast_list[i] == "":
                movie["cast"] = "Unknown"
            else:
                movie["cast"] = self.cast_list[i]
            
            movies_list.append(movie)

        return json.dumps(movies_list, indent = 4)


    def writeJson(self, fileName, JsonObject):
        with open(fileName, "w") as outfile: 
	        outfile.write(JsonObject) 
        return


    def hashOldMovies(self, fileName):
        with open(fileName) as json_file:
            old_data = json.load(json_file)
            for i in range(len(old_data)):
                self.present[old_data[i]["title"]] = True


    def preprocessFilters(self):
        for i in range(len(self.filters)):
            self.filters[i] = self.filters[i].lower() 
        return


    def hasChanged(self, fileName):
        with open(fileName) as json_file:
            new_data = json.load(json_file)
            new_changes = []
            for i in range(len(new_data)):
                if new_data[i]["title"] not in self.present:
                    new_changes.append(new_data[i])
        
        for i in range(len(new_changes)):
            to_add = False
            for j in new_changes[i]:
                changes_list = new_changes[i][j].split(", ")
                for change in changes_list:
                    if change.lower() in self.filters:
                        to_add = True
            if self.apply_filters == False:
                to_add = True
            if to_add:
                self.changes.append(new_changes[i])
        return len(self.changes) != 0


    def generateMessage(self):
        msg = "New movie details just added to the IMDB page\n\n"
        for i in range(len(self.changes)):
            key_list = self.changes[i].keys()
            msg = msg + str(i+1) + ". "
            for j in key_list:
                if j == "title":
                    msg = msg + self.changes[i][j] + "\n"
                else:
                    msg = msg + j.capitalize() + ": " + self.changes[i][j] + "\n"
            msg = msg + "\n"
        return msg


    def sendTelegramMessage(self, msg):
        sendText = 'https://api.telegram.org/bot' + self.bot_token + '/sendMessage?chat_id=' + self.bot_chatID + '&parse_mode=Markdown&text=' + msg
        res = requests.get(sendText)
        return res.json()



if __name__ == "__main__":
    Scraper = ImdbScraper(config.url, config.botToken, config.botChatID)
    results = Scraper.getHTMLContent() 
    Scraper.populate(results)
    moviesJson = Scraper.getData() 
    Scraper.writeJson("new_movies.json", moviesJson)
    Scraper.hashOldMovies("old_movies.json")
    Scraper.preprocessFilters()
    if Scraper.hasChanged("new_movies.json"):
        message = Scraper.generateMessage()
        response = Scraper.sendTelegramMessage(message)
    Scraper.writeJson("old_movies.json", moviesJson)
