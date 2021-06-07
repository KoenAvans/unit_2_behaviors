#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from ariac_flexbe_states.set_conveyorbelt_power_state import SetConveyorbeltPowerState
from flexbe_states.subscriber_state import SubscriberState
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Mon May 31 2021
@author: Koen manschot
'''
class transport_conveyor_to_pick_locationSM(Behavior):
	'''
	vervoeren van transportband naar oppak locatie
	'''


	def __init__(self):
		super(transport_conveyor_to_pick_locationSM, self).__init__()
		self.name = 'transport_ conveyor_to_pick_location'

		# parameters of this behavior

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:833 y:40, x:130 y:365
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'])
		_state_machine.userdata.start_conveyorbelt = 99
		_state_machine.userdata.stop_converyorbelt = 0

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:223 y:24
			OperatableStateMachine.add('Start conveyorbelt',
										SetConveyorbeltPowerState(),
										transitions={'continue': 'wait for part', 'fail': 'failed'},
										autonomy={'continue': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'power': 'start_conveyorbelt'})

			# x:623 y:24
			OperatableStateMachine.add('Stop converyorbelt',
										SetConveyorbeltPowerState(),
										transitions={'continue': 'finished', 'fail': 'failed'},
										autonomy={'continue': Autonomy.Off, 'fail': Autonomy.Off},
										remapping={'power': 'stop_converyorbelt'})

			# x:451 y:24
			OperatableStateMachine.add('wait for part',
										SubscriberState(topic="/ariac/break_beam_1_change", blocking=True, clear=True),
										transitions={'received': 'Stop converyorbelt', 'unavailable': 'failed'},
										autonomy={'received': Autonomy.Off, 'unavailable': Autonomy.Off},
										remapping={'message': 'message'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
