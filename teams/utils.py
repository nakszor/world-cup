from datetime import datetime

from .exceptions import ImpossibleTitlesError, InvalidYearCupError, NegativeTitlesError

def data_processing(selection_info):
    titles = selection_info["titles"]
    my_dict_cup = selection_info["first_cup"]

    date_list = my_dict_cup.split("-")

    first_cup = int(date_list[0])

    if titles < 0:
        raise NegativeTitlesError
    
    current_year = datetime.now().year

    first_possible_cup = 1930

    years_since_first_cup = (current_year - first_possible_cup) // 1

    cups_since_first_cup = years_since_first_cup // 4

    last_possible_cup = first_possible_cup + 4 * cups_since_first_cup
    
    if first_cup < first_possible_cup or first_cup > last_possible_cup:
        raise InvalidYearCupError()

    cup_years = []
    for i in range(1930, current_year, 4):
        cup_years.append(i)

    if first_cup not in cup_years:
        raise InvalidYearCupError()

    max_possible_titles = cups_since_first_cup - (cup_years.index(first_cup) + 1)
   
    if titles > max_possible_titles:
        raise ImpossibleTitlesError()

    return True


