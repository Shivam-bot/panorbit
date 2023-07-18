from .models import Country, City, CountryLanguage

def get_country_data(name):
    data = {}
    data_list = []
    # country_data = Country.objects.filter(name__icontains=name)
    country_data = Country.objects.filter(name__istartswith=name)
    for country in country_data:
        country_data = {'country_name': country.name}
        data_list.append(country_data)
        city_data = City.objects.filter(country_code__name__iexact=country.name)
        city_list = []
        language_list = []
        for city in city_data:
            city_dict = {'city_name': city.name, 'district': city.district, 'population': city.population}
            city_list.append(city_dict)
        country_data["city"] = city_list
        country_language = CountryLanguage.objects.filter(country_code__name__iexact=country.name)
        for language in country_language:
            language_dict = {'language': language.language, 'official': language.is_official,
                             "language_percentage": language.percentage}
            language_list.append(language_dict)
        country_data["language"] = language_list
        data_list.append(country_data)
    data['country'] = data_list
    return data

