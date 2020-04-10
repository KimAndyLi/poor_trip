import time
from datetime import datetime, timedelta
from pytz import timezone

from webapp.trip.models import City
from webapp.parser.live_prices import safe_city_prices
from webapp.parser.booking import get_all_hotels


# current_date = datetime.now(timezone("Europe/Moscow"))


def get_hotels_task():
    with open("cities.txt", "r") as f:
        data = f.read().splitlines(True)
        if data:
            f.seek(0)
            city = f.readline().strip()
            checkin = f.readline().strip()
            checkout = f.readline().strip()
            hotels = get_all_hotels(city, checkin, checkout)
            if hotels:
                with open("cities.txt", "r") as f2:
                    inner_data = f2.read().splitlines(True)
                    if inner_data:
                        with open("cities.txt", "w") as f3:
                            f3.writelines(data[3:])
                    else:
                        return "Cities has been deleted by clear TASK"
                return f"{city} - {checkin} - {checkout} completed"
            else:
                return f"{city} Parsing {city} - {checkin} - {checkout} crashed"

        else:
            return "All cities has been parsed"


def create_city_list_task():
    cities = [x.ru_name for x in City.query.all()]
    with open("cities.txt", "w") as f:
        for city in cities:
            checkin = datetime.now(timezone('Europe/Moscow')) + timedelta(days=1)
            for _ in range(5):
                checkout = checkin + timedelta(days=7)
                f.write(city + "\n")
                f.write(checkin.strftime("%d/%m/%Y") + "\n")
                f.write(checkout.strftime("%d/%m/%Y") + "\n")
                checkin = checkout
    return f"Cities.txt - {datetime.now(timezone('Europe/Moscow'))} created"


def get_live_prices_task():
    for city in City.query.all():
        safe_city_prices(city.eng_name.title())
        if not city:
            print(f"Live prices - {datetime.now(timezone('Europe/Moscow'))} - {city.ru_name} CRASHED")
        time.sleep(5)
    return f"Live prices - {datetime.now(timezone('Europe/Moscow'))} parsed"


def clear_cities_txt_task():
    with open("cities.txt", "r+") as f:
        f.truncate(0)
    return f"Cities.txt erased {datetime.now(timezone('Europe/Moscow'))}"
