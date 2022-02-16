import pytest
from AnonymousFacade import AnonymousFacade
from Flight import Flight
from datetime import datetime
from Airline_Company import Airline_Company
from NotLegalFlightTimesError import NotLegalFlightTimesError


@pytest.fixture(scope='session')
def airline_facade_object():
    print('Setting up same DAO for all tests.')
    anonfacade = AnonymousFacade()
    return anonfacade.login('ELAL', '123')


@pytest.fixture(autouse=True)
def reset_db(airline_facade_object):
    airline_facade_object.repo.reset_test_db()
    return


def test_airline_facade_get_airline_flights(airline_facade_object):
    actual = airline_facade_object.get_airline_flights()
    assert actual == [Flight(id=1, airline_company_id=1, origin_country_id=1, destination_country_id=2,
                             departure_time=datetime(2022, 1, 30, 16, 0, 0), landing_time=datetime(2022, 1, 30, 20, 0, 0), remaining_tickets=110)]


@pytest.mark.parametrize('flight, expected', [('not flight', None),
                                              (Flight(origin_country_id=3, destination_country_id=2,
                        departure_time=datetime(2022, 1, 30, 16, 0, 0), landing_time=datetime(2022, 1, 30, 20, 0, 0), remaining_tickets=110), None),
                                              (Flight(origin_country_id=1, destination_country_id=3,
                        departure_time=datetime(2022, 1, 30, 16, 0, 0), landing_time=datetime(2022, 1, 30, 20, 0, 0), remaining_tickets=110), None),
                                              (Flight(origin_country_id=1, destination_country_id=2,
                        departure_time=1, landing_time=datetime(2022, 1, 30, 20, 0, 0), remaining_tickets=110), None),
                                              (Flight(origin_country_id=1, destination_country_id=2,
                        departure_time=datetime(2022, 1, 30, 16, 0, 0), landing_time='not datetime', remaining_tickets=110), None),
                                              (Flight(origin_country_id=1, destination_country_id=2,
                        departure_time=datetime(2022, 1, 30, 16, 0, 0), landing_time=datetime(2022, 1, 30, 20, 0, 0), remaining_tickets=33.4), None),
                                              (Flight(origin_country_id=1, destination_country_id=2,
                        departure_time=datetime(2022, 1, 30, 16, 0, 0), landing_time=datetime(2022, 1, 30, 20, 0, 0), remaining_tickets=95), None),
                                              (Flight(origin_country_id=1, destination_country_id=2,
                        departure_time=datetime(2022, 1, 30, 17, 0, 0), landing_time=datetime(2022, 1, 30, 21, 0, 0), remaining_tickets=100), True)])
def test_airline_facade_add_flight(airline_facade_object, flight, expected):
    actual = airline_facade_object.add_flight(flight)
    assert actual == expected


def test_airline_facade_add_flight_raise_notlegalflighttimeserror(airline_facade_object):
    with pytest.raises(NotLegalFlightTimesError):
        airline_facade_object.add_flight(Flight(origin_country_id=1, destination_country_id=2,
                                                departure_time=datetime(2022, 1, 30, 17, 0, 0), landing_time=datetime(2022, 1, 30, 17, 00, 59), remaining_tickets=150))


@pytest.mark.parametrize('airline, expected', [('not airline', None),
                                               (Airline_Company(name='ELAL', country_id=1, user_id=3), None),
                                               (Airline_Company(name='LUFTHANSA', country_id=2, user_id=3), None),
                                               (Airline_Company(name='UNITED', country_id=3, user_id=3), True)])
def test_airline_facade_update_airline(airline_facade_object, airline, expected):
    actual = airline_facade_object.update_airline(airline)
    assert actual == expected


@pytest.mark.parametrize('flight, expected', [('not flight', None),
                                              (Flight(airline_company_id=3, origin_country_id=1, destination_country_id=2,
                        departure_time=datetime(2022, 1, 30, 16, 0, 0), landing_time=datetime(2022, 1, 30, 20, 0, 0), remaining_tickets=100), None),
                                              (Flight(airline_company_id=1, origin_country_id=3, destination_country_id=2,
                        departure_time=datetime(2022, 1, 30, 16, 0, 0), landing_time=datetime(2022, 1, 30, 20, 0, 0), remaining_tickets=100), None),
                                              (Flight(airline_company_id=1, origin_country_id=1, destination_country_id=3,
                        departure_time=datetime(2022, 1, 30, 16, 0, 0), landing_time=datetime(2022, 1, 30, 20, 0, 0), remaining_tickets=100), None),
                                              (Flight(airline_company_id=1, origin_country_id=1, destination_country_id=2,
                        departure_time=1, landing_time=datetime(2022, 1, 30, 20, 0, 0), remaining_tickets=100), None),
                                              (Flight(airline_company_id=1, origin_country_id=1, destination_country_id=2,
                        departure_time=datetime(2022, 1, 30, 16, 0, 0), landing_time='not datetime', remaining_tickets=100), None),
                                              (Flight(airline_company_id=1, origin_country_id=1, destination_country_id=2,
                        departure_time=datetime(2022, 1, 30, 16, 0, 0), landing_time=datetime(2022, 1, 30, 20, 0, 0), remaining_tickets=10.7), None),
                                              (Flight(airline_company_id=1, origin_country_id=1, destination_country_id=2,
                        departure_time=datetime(2022, 1, 30, 16, 0, 0), landing_time=datetime(2022, 1, 30, 20, 0, 0), remaining_tickets=-5), None),
                                              (Flight(id=3, airline_company_id=1, origin_country_id=2, destination_country_id=1,
                        departure_time=datetime(2022, 1, 29, 17, 0, 0), landing_time=datetime(2022, 1, 30, 14, 0, 0), remaining_tickets=0), None),
                                              (Flight(id=2, airline_company_id=2, origin_country_id=2, destination_country_id=1,
                        departure_time=datetime(2022, 1, 29, 17, 0, 0), landing_time=datetime(2022, 1, 30, 14, 0, 0), remaining_tickets=0), None),
                                              (Flight(id=1, airline_company_id=1, origin_country_id=2, destination_country_id=1,
                        departure_time=datetime(2022, 1, 29, 17, 0, 0), landing_time=datetime(2022, 1, 30, 14, 0, 0), remaining_tickets=0), True)])
def test_airline_facade_update_flight(airline_facade_object, flight, expected):
    actual = airline_facade_object.update_flight(flight)
    assert actual == expected


def test_airline_facade_update_flight_raise_notlegalflighttimeserror(airline_facade_object):
    with pytest.raises(NotLegalFlightTimesError):
        airline_facade_object.update_flight(Flight(id=1, airline_company_id=1, origin_country_id=1, destination_country_id=2,
                                                   departure_time=datetime(2022, 1, 30, 17, 0, 0), landing_time=datetime(2022, 1, 30, 17, 0, 59), remaining_tickets=100))


@pytest.mark.parametrize('flight_id, expected', [('not_id', None),
                                                 (0, None),
                                                 (4, None),
                                                 (2, None),
                                                 (1, True)])
def test_airline_facade_remove_flight(airline_facade_object, flight_id, expected):
    actual = airline_facade_object.remove_flight(flight_id)
    assert actual == expected
