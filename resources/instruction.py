# File name: instruction.py
# Author: Jesse Malinen
# Description: API Endpoint for the Instructions Model

# imports
from flask import request
from flask_restful import Resource
from http import HTTPStatus

from models.instructions import Instruction, instruction_list


# defining the 'all instructions' class
class InstructionListResource(Resource):

    def get(self):

        data = []

        for instruction in instruction_list:
            if instruction.is_publish is True:
                data.append(instruction.data)

        return {'data': data}, HTTPStatus.OK

    def post(self):
        data = request.get_json()

        instruction = Instruction(name=data['name'],
                                  description=data['description'],
                                  steps=data['steps'],
                                  tools=data['tools'],
                                  cost=data['cost'],
                                  duration=data['duration'])

        instruction_list.append(instruction)

        return instruction.data, HTTPStatus.CREATED


# defining the class for singular instructions
class InstructionResource(Resource):
    # looking up a specific instruction
    def get(self, instruction_id):
        instruction = next((instruction for instruction in instruction_list
                            if instruction.id == instruction_id and instruction.is_publish == True), None)

        if instruction is None:
            return {'message': 'instruction not found'}, HTTPStatus.NOT_FOUND

        return instruction.data, HTTPStatus.OK

    # posting a new instruction
    def put(self, instruction_id):
        data = request.get_json()

        instruction = next((instruction for instruction in instruction_list
                            if instruction_id == instruction_id), None)

        if instruction is None:
            return {'message': 'instruction not found'}, HTTPStatus.NOT_FOUND

        instruction.name = data['name']
        instruction.description = data['description']
        instruction.steps = data['steps']
        instruction.tools = data['tools']
        instruction.cost = data['cost']
        instruction.duration = data['duration']

        return instruction.data, HTTPStatus.OK

    def delete(self, instruction_id):
        instruction = next((instruction for instruction in instruction_list
                            if instruction_id == instruction_id), None)
        # if instruction not found
        if instruction is None:
            return {'message': 'instruction not found'}, HTTPStatus.NOT_FOUND

        instruction_list.remove(instruction)

        return {}, HTTPStatus.NO_CONTENT

# class and functions for publishing/unpublishing an instruction
class InstructionPublishResource(Resource):

    def put(self, instruction_id):
        instruction = next((instruction for instruction in instruction_list
                            if instruction_id == instruction_id), None)

        if instruction is None:
            return {'message': 'instruction not found'}, HTTPStatus.NOT_FOUND

        instruction.is_publish = True

        return {}, HTTPStatus.NO_CONTENT

    def delete(self, instruction_id):
        instruction = next((instruction for instruction in instruction_list
                            if instruction_id == instruction_id), None)

        if instruction is None:
            return {'message': 'instruction not found'}, HTTPStatus.NOT_FOUND

        instruction.is_publish = False

        return {}, HTTPStatus.NO_CONTENT
