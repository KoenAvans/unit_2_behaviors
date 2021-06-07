#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from ariac_flexbe_states.lookup_from_table import LookupFromTableState
from ariac_flexbe_states.srdf_state_to_moveit_ariac_state import SrdfStateToMoveitAriac
from ariac_flexbe_states.vacuum_gripper_control_state import VacuumGripperControlState
from flexbe_states.wait_state import WaitState
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Wed Jun 02 2021
@author: Koen Manschot
'''
class place_part_on_binSM(Behavior):
	'''
	places the part on the robot in the bin
	'''


	def __init__(self):
		super(place_part_on_binSM, self).__init__()
		self.name = 'place_part_on_bin'

		# parameters of this behavior

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		# x:1133 y:440, x:533 y:440
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed'], input_keys=['namespace_move', 'type_part', 'gripper_service', 'end_pose'])
		_state_machine.userdata.move_group = 'manipulator'
		_state_machine.userdata.action_topic = '/move_group'
		_state_machine.userdata.robot_name = ''
		_state_machine.userdata.config_name1 = 'home1'
		_state_machine.userdata.config_name2 = 'home2'
		_state_machine.userdata.action_topicname1 = '/ariac/arm1'
		_state_machine.userdata.action_topicname2 = '/ariac/arm2'
		_state_machine.userdata.namespace_move = ''
		_state_machine.userdata.type_part = ''
		_state_machine.userdata.gripper_service = ''
		_state_machine.userdata.end_pose = ''

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:185 y:24
			OperatableStateMachine.add('Lookup pregrasp',
										LookupFromTableState(parameter_name='/ariac_tables_unit2', table_name='bin_choice', index_title='bin', column_title='robot_pregrasp'),
										transitions={'found': 'Move to bin Pregrasp', 'not_found': 'failed'},
										autonomy={'found': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'index_value': 'type_part', 'column_value': 'robot_pregrasp'})

			# x:634 y:24
			OperatableStateMachine.add('Move to Home',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'Move to Home_2', 'planning_failed': 'Wait 2', 'control_failed': 'Wait 2', 'param_error': 'Wait 2'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'end_pose', 'move_group': 'move_group', 'action_topic_namespace': 'namespace_move', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:784 y:24
			OperatableStateMachine.add('Move to Home_2',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'Move to Home_4', 'planning_failed': 'Wait 3', 'control_failed': 'Wait 3', 'param_error': 'Wait 3'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'config_name1', 'move_group': 'move_group', 'action_topic_namespace': 'action_topicname1', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:934 y:24
			OperatableStateMachine.add('Move to Home_4',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'finished', 'planning_failed': 'Wait 1_2_2_2', 'control_failed': 'Wait 1_2_2_2', 'param_error': 'Wait 1_2_2_2'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'config_name2', 'move_group': 'move_group', 'action_topic_namespace': 'action_topicname2', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:334 y:24
			OperatableStateMachine.add('Move to bin Pregrasp',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'deactivate gripper', 'planning_failed': 'Wait 1', 'control_failed': 'Wait 1', 'param_error': 'Wait 1'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'robot_pregrasp', 'move_group': 'move_group', 'action_topic_namespace': 'namespace_move', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:357 y:124
			OperatableStateMachine.add('Wait 1',
										WaitState(wait_time=5),
										transitions={'done': 'Move to bin Pregrasp'},
										autonomy={'done': Autonomy.Off})

			# x:955 y:124
			OperatableStateMachine.add('Wait 1_2_2_2',
										WaitState(wait_time=5),
										transitions={'done': 'Move to Home_4'},
										autonomy={'done': Autonomy.Off})

			# x:657 y:124
			OperatableStateMachine.add('Wait 2',
										WaitState(wait_time=5),
										transitions={'done': 'Move to Home'},
										autonomy={'done': Autonomy.Off})

			# x:807 y:124
			OperatableStateMachine.add('Wait 3',
										WaitState(wait_time=5),
										transitions={'done': 'Move to Home_2'},
										autonomy={'done': Autonomy.Off})

			# x:474 y:24
			OperatableStateMachine.add('deactivate gripper',
										VacuumGripperControlState(enable=False),
										transitions={'continue': 'Move to Home', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'service_name': 'gripper_service'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
