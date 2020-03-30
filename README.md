# imdb-scraper
IMDb scraper, built using Python, that sends out a telegram notification whenever new movie details pertaining to your interests are added to the IMDb page.

**Note :** The movies releasing in 2020 are being scraped in this project. You can change the URL to any other page of your interest given that the structure of that page is same as the one used here.

**Libraries used :** `BeautifulSoup` and `requests`

**How to use :** After installing the required libraries, you will need to provide your bot's token and chat ID in the `config.py` file.
If you don't have a telegram bot, you can create one by following steps mentioned [here](https://medium.com/@ManHay_Hong/how-to-create-a-telegram-bot-and-send-messages-with-python-4cf314d9fa3e).

Once that is done, you are good to go. If you want to recieve notifications regarding only certain updates, then you have to set `self.apply_filter` 
and then add all the required keywords in `self.filters`. By doing this you will only be notified for only specific updates. If you want to recieve all
the updates, then simply reset `self.apply_filter`. Run `scraper.py` file to get notifications. 

If don't want to run the file everytime, then you can create a batch file to run scraper.py and add that batch file to the statup tasks. Now whenever your system boots,
`scraper.py` will run in the background. You can also add schedulers to recieve timely updates.
