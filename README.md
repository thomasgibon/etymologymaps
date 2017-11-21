# etymologymaps
This project aims at creating a basis for creating etymology maps (see https://www.reddit.com/r/etymologymaps/ for examples), by scraping wiktionary.org for translations and mapping them on a template svg file.

# Usage
Two functions are important here.

## `mtranslate(to_translate, wiki_lang)`
This function translates word `to_translate` (string) from language `wiki_lang` (string) to all languages available on the Wikipedia page.
The output is a text file containing the list of translation.

## `map_word(to_translate, from_language)`
This function calls `mtranslate` and maps (quite literally) the translations to the languages areas, based on the file `Simplified_Languages_of_Europe_map_base.svg`.
