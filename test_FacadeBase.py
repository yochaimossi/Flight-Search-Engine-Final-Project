import pytest
from AnonymousFacade import AnonymousFacade
from Flight import Flight
from Country import Country
from Airline_Company import Airline_Company
from datetime import datetime
from User import User


@pytest.fixture(scope='session')
def dao_connection_singleton():
    print('Setting up same DAO for all tests.')
    return AnonymousFacade()


@pytest.fixture(autouse=True)
def reset_db(dao_connection_singleton):
    dao_connection_singleton.repo.reset_test_db()
    return


def test_facade_base_get_all_flights(dao_connection_singleton):
    actual = dao_connection_singleton.get_all_flights()
    assert actual == [Flight(id=1, airline_company_id=1, origin_country_id=1, destination_country_id=2,
                        departure_time=datetime(2022, 1, 30, 16, 0, 0), landing_time=datetime(2022, 1, 30, 20, 0, 0),
                             remaining_tickets=200),
                      Flight(id=2, airline_company_id=2, origin_country_id=1, destination_country_id=2,
                        departure_time=datetime(2022, 1, 30, 16, 0, 0),
                        landing_time=datetime(2022, 1, 30, 20, 0, 0), remaining_tickets=0)]


@pytest.mark.parametrize('id_, expected', [(1, Flight(id=1, airline_company_id=1, origin_country_id=1, destination_country_id=2,
                        departure_time=datetime(2022, 1, 30, 16, 0, 0), landing_time=datetime(2022, 1, 30, 20, 0, 0),
                             remaining_tickets=200)), (2, Flight(id=2, airline_company_id=2, origin_country_id=1, destination_country_id=2,
                        departure_time=datetime(2022, 1, 30, 16, 0, 0),
                        landing_time=datetime(2022, 1, 30, 20, 0, 0), remaining_tickets=0))])
def test_facade_base_get_flight_by_id(dao_connection_singleton, id_, expected):
    actual = dao_connection_singleton.get_flight_by_id(id_)
    assert actual == [expected]


@pytest.mark.parametrize('ocountry_id, dcountry_id, date_, expected', [('f', 3, datetime(2022, 1, 30), None),
                                                                       (3, 'r', datetime(2022, 1, 30), None),
                                                                       (0, 4, datetime(2022, 1, 30), None),
                                                                       (1, 2, 4, None),
                                                                       (1, 2, datetime(2022, 1, 30), [Flight(id=1, airline_company_id=1, origin_country_id=1, destination_country_id=2,
                        departure_time=datetime(2022, 1, 30, 16, 0, 0), landing_time=datetime(2022, 1, 30, 20, 0, 0),
                             remaining_tickets=200), Flight(id=2, airline_company_id=2, origin_country_id=1, destination_country_id=2,
                        departure_time=datetime(2022, 1, 30, 16, 0, 0),
                        landing_time=datetime(2022, 1, 30, 20, 0, 0), remaining_tickets=0)]),
                                                                       (1, 1, datetime(2022, 1, 30), [])])
def test_facade_base_get_flights_by_parameters(dao_connection_singleton, ocountry_id, dcountry_id, date_, expected):
    actual = dao_connection_singleton.get_flights_by_parameters(ocountry_id, dcountry_id, date_)
    assert actual == expected


def test_facade_base_get_all_airlines(dao_connection_singleton):
    actual = dao_connection_singleton.get_all_airlines()
    assert actual == [Airline_Company(id=1, name='ELAL', country_id=1, user_id=3),
                      Airline_Company(id=2, name='Lufthansa', country_id=2, user_id=4)]


@pytest.mark.parametrize('id_, expected', [('h', None),
                                           (0, None),
                                           (3, []),
                                           (1, [Airline_Company(id=1, name='ELAL', country_id=1, user_id=3)]),
                                           (2, [Airline_Company(id=2, name='Lufthansa', country_id=2, user_id=4)])])
def test_facade_base_get_airline_by_id(dao_connection_singleton, id_, expected):
    actual = dao_connection_singleton.get_airline_by_id(id_)
    assert actual == expected


def test_facade_base_get_all_countries(dao_connection_singleton):
    actual = dao_connection_singleton.get_all_countries()
    assert actual == [Country(id=1, name='Israel'), Country(id=2, name='Germany')]


@pytest.mark.parametrize('id_, expected', [('6', None),
                                           (0, None),
                                           (3, []),
                                           (1, [Country(id=1, name='Israel')]),
                                           (2, [Country(id=2, name='Germany')])])
def test_facade_base_get_country_by_id(dao_connection_singleton, id_, expected):
    actual = dao_connection_singleton.get_country_by_id(id_)
    assert actual == expected


@pytest.mark.parametrize('user, expected', [('notuser', None),
                                            (User(username='Jon', password='123', email='Johnny@gmail.com', user_role=1), None),
                                            (User(username='Johnny', password='123', email='Johnny@gmail.com', user_role=2), None),
                                            (User(username='Johnny', password='123', email='Johnny@gmail.com', user_role=5), None),
                                            (User(username='Johnny', password='123', email='Johnny@gmail.coom', user_role=2), True)])
def test_facade_base_create_user(dao_connection_singleton, user, expected):
    actual = dao_connection_singleton.create_user(user)
    assert actual == expected


@pytest.mark.parametrize('airline_id, expected', [('not int', None),
                                                  (0, None),
                                                  (7, None),
                                                  (1, [Flight(id=1, airline_company_id=1, origin_country_id=1, destination_country_id=2,
                        departure_time=datetime(2022, 1, 30, 16, 0, 0), landing_time=datetime(2022, 1, 30, 20, 0, 0), remaining_tickets=120)])])
def test_airline_facade_get_flights_by_airline(dao_connection_singleton, airline_id, expected):
    actual = dao_connection_singleton.get_flights_by_airline_id(airline_id)
    assert actual == expected
