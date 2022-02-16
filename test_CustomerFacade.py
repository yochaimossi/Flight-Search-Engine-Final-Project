import pytest
from Customer import Customer
from Ticket import Ticket
from AnonymousFacade import AnonymousFacade
from NoRemainingTicketsError import NoRemainingTicketsError


@pytest.fixture(scope='session')
def customer_facade_object():
    print('Setting up same DAO for all tests.')
    anonfacade = AnonymousFacade()
    return anonfacade.login('Avi', '123')


@pytest.fixture(autouse=True)
def reset_db(customer_facade_object):
    customer_facade_object.repo.reset_test_db()
    return


@pytest.mark.parametrize('customer, expected', [('not customer', None),
                                                (Customer(first_name='Jon', last_name='Doe', address='Weizmann 11',
                          phone_no='0523456007', credit_card_no='0022', user_id=2), None),
                                                (Customer(first_name='Jon', last_name='Doe', address='Weizmann 11',
                          phone_no='0523456000', credit_card_no='0000', user_id=2), None),
                                                (Customer(first_name='Johnny', last_name='Donny', address='Weizmann 111',
                          phone_no='0523456000', credit_card_no='9999', user_id=2), True)])
def test_customer_facade_update_customer(customer_facade_object, customer, expected):
    actual = customer_facade_object.update_customer(customer)
    assert actual == expected


@pytest.mark.parametrize('ticket, expected', [('not ticket', None),
                                              (Ticket(flight_id=3), None),
                                              (Ticket(flight_id=2), True)])
def test_customer_facade_remove_ticket(customer_facade_object, ticket, expected):
    actual = customer_facade_object.remove_ticket(ticket)
    assert actual == expected


def test_customer_facade_get_tickets_by_customer(customer_facade_object):
    actual = customer_facade_object.get_tickets_by_customer()
    assert actual == [Ticket(id=2, flight_id=2, customer_id=2)]


def test_customer_facade_add_ticket_raise_noremainingticketserror(customer_facade_object):
    with pytest.raises(NoRemainingTicketsError):
        customer_facade_object.add_ticket(Ticket(flight_id=2, customer_id=1))


@pytest.mark.parametrize('ticket, expected', [('not ticket', None),
                                              (Ticket(flight_id=4), None),
                                              (Ticket(flight_id=1), True)])
def test_customer_facade_add_ticket(customer_facade_object, ticket, expected):
    actual = customer_facade_object.add_ticket(ticket)
    assert actual == expected