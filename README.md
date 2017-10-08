
# Movie arranger

This stack provide some usefull tools and ultimatly a funcion to arrange movie folders. For now the script support movie folders which the
words are seperated by dots. eg: The.legend.of.tarzan.2016.1080p.xSpark. Please share with me any idea regrading this project at saharsela271@gmail.com.
Enjoy

## Yet to come
* Automaticly download subs into the movie folder
* Supporting a wide variety of folder name format

## Getting Started

The easy way is to navigate to the desired folder using the terminal and opening the script there.
```
python3.5
import Movies_arranger as ma
```
after that you can access the stack functions to organize the folder.

All the functions have docstring attached to them if something isn't clear.

## Prerequisites

The script use bs4 so it should be installed before. The easy way is of course pip

```
pip3.5 install bs4
```

## How- to
After initiating the script in the folder simply run arrange_this_folder()
The other way is pass arrange_this_folder() the desired path.

### Inside a folder

```
import Movies_arranger as ma
ma.arrange_this_folder()
```

### Outside the desired folder

```
import Movies_arranger as ma
ma.arrange_this_folder(movies_folder_path)
```

You should use os.path.join to avoide any problems.
