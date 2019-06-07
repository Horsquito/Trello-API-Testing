import pytest
from model.board import Board
from model.card import Card
from fixture.application import Application


@pytest.fixture(scope='module')
def app(request):
    fixture = Application()
    request.addfinalizer(fixture.destroy)
    return fixture


def test_create_valid_name_board(app):
    assert app.create_board(Board(name='Valid name board')) == (200, 'Valid name board')


def test_create_whitespase_name_board(app):
    assert app.create_board(Board(name='    ')) == (200, '    ')


def test_create_existing_name_board(app):
    assert app.create_board(Board(name='Valid name board')) == (200, 'Valid name board')


def test_create_empty_board(app):
    assert app.create_empty_board(Board(name='')) == 400


def test_edit_board(app):
    assert app.edit_board(Board(name='New board name'), app.id) == (200, 'New board name')


def test_edit_nonexistent_board(app):
    assert app.edit_nonexistent_board(Board(name='New board name'), '1234567890') == 400


def test_get_board(app):
    assert app.get_board(app.id) == (200, 'New board name')


def test_get_cards(app):
    list_id = app.get_list_id(app.id)
    app.create_card(Card(name='New card'), list_id)
    assert app.get_cards(app.id) == (200, 'New card')


def test_delete_board(app):
    assert app.delete_board(app.id) == 200
    assert app.get_board(app.id) == None


def test_delete_nonexistent_board(app):
    assert app.delete_nonexistent_board('1234567890') == 400
