from constants.constants import URL, KEY, TOKEN
import requests
import logging
from model.board import Board
from model.card import Card
import json


class Application:
    logger = logging.getLogger(__name__)

    def create_board(self, board, logger=logger):
        logger.info('Start creating {}'.format(board.name))
        url = URL + '1/boards' + '?' + KEY + '&' + TOKEN
        querystring = {"name": board.name}
        response = requests.post(url, data=querystring)
        if response.status_code == 200:
            logger.info('Board created')
        else:
            logger.error('Something went wrong')
        return response.status_code

    def create_empty_board(self, board, logger=logger):
        logger.info('Start creating empty board')
        url = URL + '1/boards' + '?' + KEY + '&' + TOKEN
        querystring = {"name": board.name}
        response = requests.post(url, data=querystring)
        if response.status_code == 400:
            logger.info('Empty board did not create')
        else:
            logger.error('Something went wrong')
        return response.status_code

    def get_board_id(self):
        url = URL + "1/members/me/boards?" + KEY + "&" + TOKEN
        response = requests.get(url)
        data = response.text
        data = json.loads(data)
        id = data[0]['id']
        board_id = id
        return board_id

    def get_list_id(self, board_id, logger=logger):
        logger.info('Getting list id')
        url = URL + '1/boards/' + str(board_id) + '/lists' + '?' + KEY + '&' + TOKEN
        response = requests.get(url)
        if response.status_code == 200:
            logger.info('List id received')
            list_data = response.text
            list_data = json.loads(list_data)
            id_list = list_data[0]['id']
            return id_list
        else:
            logger.error('List id not found')

    def create_card(self, card, list_id, logger=logger):
        logger.info('Creating card')
        url = URL + '1/cards?' + KEY + '&' + TOKEN
        querystring = {"idList": list_id, "name": card.name}
        response = requests.post(url, params=querystring)
        if response.status_code == 200:
            logger.info('Card created')
        else:
            logger.error('Could not create card')
        return response.status_code

    def delete_board(self, board_id, logger=logger):
        logger.info('Board removal')
        url = URL + '1/boards/' + str(board_id) + '?' + KEY + '&' + TOKEN
        response = requests.delete(url)
        if response.status_code == 200:
            logger.info('Board removed successfully')
        else:
            logger.error('Failed to remove the board')
        return response.status_code

    def delete_nonexistent_board(self, board_id, logger=logger):
        logger.info('Board removal')
        url = URL + '1/boards/' + str(board_id) + '?' + KEY + '&' + TOKEN
        response = requests.delete(url)
        if response.status_code == 400:
            logger.info('Nonexistent board was not delete')
        else:
            logger.error('Something went wrong')
        return response.status_code

    def edit_board(self, board, board_id, logger=logger):
        logger.info('Edit board')
        url = URL + '1/boards/' + str(board_id) + '?' + KEY + '&' + TOKEN
        querystring = {"name": board.name}
        response = requests.put(url, params=querystring)
        if response.status_code == 200:
            logger.info('Board changed')
        else:
            logger.error('Failed to change board')
        return response.status_code

    def edit_nonexistent_board(self, board, board_id, logger=logger):
        logger.info('Edit board')
        url = URL + '1/boards/' + str(board_id) + '?' + KEY + '&' + TOKEN
        querystring = {"name": board.name}
        response = requests.put(url, params=querystring)
        if response.status_code == 400:
            logger.info('Nonexistent board was not changed')
        else:
            logger.error('Something went wrong')
        return response.status_code

    def get_board(self, board_id, logger=logger):
        logger.info('Get the board')
        url = URL + '1/boards/' + str(board_id) + '?' + KEY + '&' + TOKEN
        response = requests.get(url)
        if response.status_code == 200:
            logger.info('Got the boards')
        else:
            logger.error('Did not get the boards')
        return response.status_code

    def get_cards(self, board_id, logger=logger):
        logger.info('Getting the cards')
        url = URL + '1/boards/' + str(board_id) + '/cards?' + KEY + '&' + TOKEN
        response = requests.get(url)
        if response.status_code == 200:
            logger.info('Received cards')
        else:
            logger.error('Could not get cards')
        return response.status_code

    def destroy(self):
        url = URL + "1/members/me/boards?" + KEY + "&" + TOKEN
        response = requests.get(url)
        data = response.text
        boards = json.loads(data)
        for board in boards:
            board_id = board['id']
            url = URL + '1/boards/' + str(board_id) + '?' + KEY + '&' + TOKEN
            requests.delete(url)
        logging.info('All boards were deleted')
