import os
import re
import requests
import urllib
import urllib.parse
from bs4 import BeautifulSoup
import urllib.request
import io


class MovieDidNotFound(Exception):
    pass


class movie():
    """ Movie class extracts and provides all the information about the movie from the web. for now the class can only get
        folders in the format of dots connecting the full name. For example The.legend.of.tarzan.2016.1080p.xSpark

        After running the script once the name of the folders will be changed so that the format of the folder names wont
        fit. For that the script creates a text file containing the original folder name and use it if the check attribute
        is 1

    Attributes:
        movie_title: str provided in order to identify the movie, should be in the format dots. eg: The.legend.of.tarzan.2016.1080p.xsparks.
        movie_name: str containing the movie name after the extraction of data from web.
        definition: str of the definition of the movie.
        year: int with the movie year.
        imdb_score: str with the imdb score of the movie
        sub_link: to be added..
        sub_path: to be added..
        id: str with the movie id from the imdb site
        soup: Beautifull soup object containing the imdb movie page
        new_name: str with the movie name year and imdb score. formatted to be shown in the folder

    """

    def __init__(self, movie_title, folder_name=''):
        self.movie_title = movie_title
        if folder_name != '':
            self.folder_name = folder_name
        else:
            self.folder_name = movie_title
        self.movie_name = ''
        self.definition = ''
        self.year = ''
        self.imdb_score = ''
        self.sub_link = ''
        self.sub_path = ''
        self.id = ''
        self.get_movie_name()
        self.get_movie_year_def()
        self.id = imdb_id_from_title(self.movie_name)
        pattern = 'http://www.imdb.com/title/{id}/?ref_=fn_al_tt_1'
        url = pattern.format(id=self.id)
        page = urllib.request.urlopen(url)
        self.soup = BeautifulSoup(page, "html.parser")
        self.get_rating()
        self.new_name = (
        self.movie_name.capitalize() + ', Movie year - ' + str(self.year) + ' Rating - ' + self.imdb_score)
        self.create_data_file()

    def get_movie_name(self):
        """ Assigning the movie name from the movie title given to movie_name arg."""
        temp_len = re.split('\.', self.movie_title)
        self.movie_name = temp_len[0]
        temp_len.remove(temp_len[0])
        for word in temp_len:
            if word.isnumeric():
                break
            else:
                self.movie_name = self.movie_name + ' ' + word

    def get_movie_year_def(self):
        """ Assigning the year and definition to the appropriate class attributes"""
        number = 0
        temp_len = re.split('\.', self.movie_title)
        for word in temp_len:
            if number == 1:
                self.definition = word
                break
            if word.isnumeric() and number == 0:
                self.year = int(word)
                number += 1

    def get_rating(self):
        "Assign the imdb rating of the movie to the imdb_score variable"
        self.imdb_score = self.soup.find("span", itemprop="ratingValue").contents[0]

    def create_data_file(self):
        """Creates a text file containing the movie information inside the movie folder. The check variable indicates that
        the program has ran once of this folder and that the info was extracted once."""
        path = os.path.join(os.getcwd(), self.folder_name)
        base_path = os.getcwd()
        os.chdir(path)
        file = open('Info.txt', 'w')
        file.write('Check: 1 \n')
        for a in dir(self):
            if not a.startswith('__') and not callable(getattr(self, a)):
                file.write(a + ':' + str(getattr(self, a)) + ' \n')
        file.close()
        os.chdir(base_path)


def text_to_dict(text_file) -> dict:
    """ return dictonary with movie attributes from info text file

    Args:
        text_file: the info.txt file
    Returns:
        temp_dict: the dictonary with the movie attributes
    """
    temp_dict = {}
    line = text_file.readline()
    while line != '':
        temp_len = re.split(":", line)
        ind = temp_len[1].find("\\")
        temp_len[1] = temp_len[1][:ind]
        dict1 = {temp_len[0]: temp_len[1]}
        temp_dict.update(dict1)
        line = text_file.readline()
    return temp_dict


def imdb_id_from_title(title):
    """ return IMDb movie id for search string

        Args::
            title (str): the movie title search string
        Returns:
            str. IMDB id, e.g., 'tt0095016'
            None. If no match was found
    """
    pattern = 'http://www.imdb.com/xml/find?json=1&nr=1&tt=on&q={movie_title}'
    url = pattern.format(movie_title=urllib.parse.quote(title))
    r = requests.get(url)
    res = r.json()
    # sections in descending order or preference
    for section in ['popular', 'exact', 'substring']:
        key = 'title_' + section
        if key in res:
            return res[key][0]['id']
    raise MovieDidNotFound("Couldnt find the movie, maybe you have folders that are not movies.")


def string_to_plus(string1: list) -> str:
    """Return the string connected by + for inserting into web urls searches

    Args:
        string1: Original list
    Returns:
        finale_string:The list items connected with +
    """
    finale_string = ''
    for word in string1:
        finale_string = finale_string + word + '+'
    return finale_string[: -1]


def imdb_id_from_title2(title: str) -> str:
    """ return IMDb movie id for search string

        Need to be updated, using imdb_id_from_title for now..
    """
    pattern = 'http://www.imdb.com/find?ref_=nv_sr_fn&q={movie_title}&s=all'
    temp_len = re.split(' ', title)
    plus_len = string_to_plus(temp_len)
    url = pattern.format(movie_title=plus_len)
    page = urllib.request.urlopen(url)
    local_soup = BeautifulSoup(page, "html.parser")
    table = local_soup.find_all('tr', class_='findResult odd')[0].a['href']
    id = re.split('./', table)[1]
    return id


def arrange_this_folder(path=os.getcwd()):
    """Given a folder path with the folders names in the format that the movie class can input, arrange the names of
    the folder in the format of (Movie_name, Year: Movie_year, Rating: imdb_rating)"""
    not_found_list = []
    folder_list = os.listdir(path)
    base_folder = path
    folder_list = remove_hidden(folder_list)
    for folder in folder_list:
        try:
            info_text = open(os.path.join(os.getcwd(), folder, "Info.txt"))
            dict1 = text_to_dict(info_text)
            if dict1['Check'] != ' 1 ':
                x = movie(folder)
                os.rename(os.path.join(base_folder, folder), x.new_name)
            if dict1['Check'] == ' 1 ':
                x = movie(dict1['movie_title'], folder)
                os.rename(os.path.join(base_folder, folder), x.new_name)
        except NotADirectoryError:
            pass
        except FileNotFoundError:
            try:
                x = movie(folder)
                os.rename(os.path.join(base_folder, folder), x.new_name)
            except MovieDidNotFound:
                not_found_list.append(folder)
                pass
            pass
    print("These movies are not in the imdb database or maybe they are not movie folders:")
    for movies in not_found_list:
        print(movies + '\n')


def remove_hidden(folder_list: list) -> list:
    """Returns a list containing folder_list items without the hidden ones"""
    folder_temp = []
    for folder in folder_list:
        if folder[0] == '.':
            folder_temp.append(folder)
    for folder in folder_temp:
        folder_list.remove(folder)
    return folder_list


def get_info_file(path=os.getcwd()):
    """Returns the info.txt file inside the path given

        Arguments:
            path: str of the folder (default is the current directory)

        Returns:
            file: text file 
    """
    return open(os.path.join(path, "Info.txt"))
