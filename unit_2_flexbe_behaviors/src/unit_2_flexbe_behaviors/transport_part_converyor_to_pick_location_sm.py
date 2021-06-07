#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from ariac_flexbe_example_behaviors.transport__conveyor_to_pick_location_sm import transport_conveyor_to_pick_locationSM
from unit_2_flexbe_behaviors.pick_part_from_conveyor_sm import pick_part_from_conveyorSM
from unit_2_flexbe_behaviors.place_part_on_bin_sm import place_part_on_binSM
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Mon Jun 07 2021
@author: Koen Manschot
'''
class Transport_part_converyor_to_pick_locationSM(Behavior):
	'''
	transporteren part op de conveyor naar de gewenste bin. (Unit 2 compleet)
	'''


	def __init__(self):
		super(Transport_part_converyor_to_pick_locationSM, self).__init__()
		self.name = 'Transport_part_converyor_to_pick_location'

		# parameters of this behavior

		# references to used behaviors
		self.add_behavior(pick_part_from_conveyorSM, 'pick_part_from_conveyor')
		self.add_behavior(place_part_on_binSM, 'place_part_on_bin')
		self.add_behavior(transport_conveyor_to_pick_locationSM, 'transport_ conveyor_to_pick_location')

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:1139 y:392, x:205 y:353, x:351 y:350, x:512 y:351
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed', 'Not found', 'Parameter Error'])
		_state_machine.userdata.type_part = ''
		_state_machine.userdata.namespace_move = ''
		_state_machine.userdata.gripper_service = ''
		_state_machine.userdata.end_pose = ''

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:81 y:35
			OperatableStateMachine.add('transport_ conveyor_to_pick_location',
										self.use_behavior(transport_conveyor_to_pick_locationSM, 'transport_ conveyor_to_pick_location'),
										transitions={'finished': 'pick_part_from_conveyor', 'failed': 'failed'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit})

			# x:610 y:37
			OperatableStateMachine.add('place_part_on_bin',
										self.use_behavior(place_part_on_binSM, 'place_part_on_bin'),
										transitions={'finished': 'finished', 'failed': 'failed', 'Not Found': 'Not found'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit, 'Not Found': Autonomy.Inherit},
										remapping={'namespace_move': 'namespace_move', 'type_part': 'type_part', 'gripper_service': 'gripper_service', 'end_pose': 'end_pose'})

			# x:369 y:34
			OperatableStateMachine.add('pick_part_from_conveyor',
										self.use_behavior(pick_part_from_conveyorSM, 'pick_part_from_conveyor'),
										transitions={'finished': 'place_part_on_bin', 'failed': 'failed', 'Not found': 'Not found', 'parameter error': 'Parameter Error'},
										autonomy={'finished': Autonomy.Inherit, 'failed': Autonomy.Inherit, 'Not found': Autonomy.Inherit, 'parameter error': Autonomy.Inherit},
										remapping={'type_part': 'type_part', 'namespace_move': 'namespace_move', 'gripper_service': 'gripper_service', 'end_pose': 'end_pose'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
