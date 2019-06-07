from constants.constants import URL, PAYLOAD
import requests
import logging
from model.board import Board
from model.card import Card
import json


class Application:
    logger = logging.getLogger(__name__)

    def __init__(self):
        self.id = None

    def create_board(self, board, logger=logger):
        logger.info('Start creating {}'.format(board.name))
        url = URL + '1/boards'
        querystring = {"name": board.name}
        response = requests.post(url, params=PAYLOAD, data=querystring)
        text = response.text
        text = json.loads(text)
        board_name = text['name']
        board_id = text['id']
        self.id = board_id
        info = (response.status_code, board_name)
        if response.status_code == 200:
            logger.info('Board created')
        else:
            logger.error('Something went wrong')
        return info

    def create_empty_board(self, board, logger=logger):
        logger.info('Start creating empty board')
        url = URL + '1/boards'
        querystring = {"name": board.name}
        response = requests.post(url, params=PAYLOAD, data=querystring)
        if response.status_code == 400:
            logger.info('Empty board did not create')
        else:
            logger.error('Something went wrong')
        return response.status_code

    def get_list_id(self, board_id, logger=logger):
        logger.info('Getting list id')
        url = URL + '1/boards/' + str(board_id) + '/lists'
        response = requests.get(url, params=PAYLOAD)
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
        url = URL + '1/cards?'
        querystring = {"idList": list_id, "name": card.name}
        response = requests.post(url, params=PAYLOAD, data=querystring)
        text = response.text
        text = json.loads(text)
        card_name = text['name']
        info = (response.status_code, card_name)
        if response.status_code == 200:
            logger.info('Card created')
        else:
            logger.error('Could not create card')
        return info

    def delete_board(self, board_id, logger=logger):
        logger.info('Board removal')
        url = URL + '1/boards/' + str(board_id)
        response = requests.delete(url, params=PAYLOAD)
        if response.status_code == 200:
            logger.info('Board removed successfully')
        else:
            logger.error('Failed to remove the board')
        return response.status_code

    def delete_nonexistent_board(self, board_id, logger=logger):
        logger.info('Board removal')
        url = URL + '1/boards/' + str(board_id)
        response = requests.delete(url, params=PAYLOAD)
        if response.status_code == 400:
            logger.info('Nonexistent board was not delete')
        else:
            logger.error('Something went wrong')
        return response.status_code

    def edit_board(self, board, board_id, logger=logger):
        logger.info('Edit board')
        url = URL + '1/boards/' + str(board_id)
        querystring = {"name": board.name}
        response = requests.put(url, params=PAYLOAD, data=querystring)
        text = response.text
        text = json.loads(text)
        board_name = text['name']
        info = (response.status_code, board_name)
        if response.status_code == 200:
            logger.info('Board changed')
        else:
            logger.error('Failed to change board')
        return info

    def edit_nonexistent_board(self, board, board_id, logger=logger):
        logger.info('Edit nonexistent board')
        url = URL + '1/boards/' + str(board_id)
        querystring = {"name": board.name}
        response = requests.put(url, params=PAYLOAD, data=querystring)
        if response.status_code == 400:
            logger.info('Nonexistent board was not changed')
        else:
            logger.error('Something went wrong')
        return response.status_code

    def get_board(self, board_id, logger=logger):
        logger.info('Get the board')
        url = URL + '1/boards/' + str(board_id)
        response = requests.get(url, params=PAYLOAD)
        if response.status_code == 200:
            text = response.text
            text = json.loads(text)
            board_name = text['name']
            info = (response.status_code, board_name)
            return info
            logger.info('Got the board')
        else:
            logger.error('Did not get the boards')

    def get_cards(self, board_id, logger=logger):
        logger.info('Getting the cards')
        url = URL + '1/boards/' + str(board_id) + '/cards'
        response = requests.get(url, params=PAYLOAD)
        text = response.text
        text = json.loads(text)
        card_name = text[0]['name']
        info = (response.status_code, card_name)
        if response.status_code == 200:
            logger.info('Received cards')
        else:
            logger.error('Could not get cards')
        return info

    def destroy(self):
        url = URL + "1/members/me/boards"
        response = requests.get(url, params=PAYLOAD)
        data = response.text
        boards = json.loads(data)
        for board in boards:
            board_id = board['id']
            url = URL + '1/boards/' + str(board_id)
            requests.delete(url, params=PAYLOAD)
        logging.info('All boards were deleted')
