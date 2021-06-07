#!/usr/bin/env python
# -*- coding: utf-8 -*-
###########################################################
#               WARNING: Generated code!                  #
#              **************************                 #
# Manual changes may get lost if file is generated again. #
# Only code inside the [MANUAL] tags will be kept.        #
###########################################################

from flexbe_core import Behavior, Autonomy, OperatableStateMachine, ConcurrencyContainer, PriorityContainer, Logger
from ariac_flexbe_states.compute_grasp_ariac_state import ComputeGraspAriacState
from ariac_flexbe_states.moveit_to_joints_dyn_ariac_state import MoveitToJointsDynAriacState
from ariac_support_flexbe_states.get_item_from_list_state import GetItemFromListState
from flexbe_states.wait_state import WaitState
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Mon Jun 07 2021
@author: Koen Manschot
'''
class Move_to_bin_gasketSM(Behavior):
	'''
	move to bin gearpart
	'''


	def __init__(self):
		super(Move_to_bin_gasketSM, self).__init__()
		self.name = 'Move_to_bin_gasket'

		# parameters of this behavior

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		joint_names = ['linear_arm_actuator_joint', 'shoulder_pan_joint', 'shoulder_lift_joint', 'elbow_joint', 'wrist_1_joint','wrist_2_joint', 'wrist_3_joint']
		positie = ['-0.194470, -1.32807, 0.8', '0.2, 0.2, 0.2,']
		# x:905 y:393, x:419 y:425, x:230 y:415
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed', 'Not Found'], input_keys=['namespace_move', 'gripper_service'])
		_state_machine.userdata.ref_frame = 'world'
		_state_machine.userdata.frame = 'bin_2_frame'
		_state_machine.userdata.index = 0
		_state_machine.userdata.tool_link = 'ee_link'
		_state_machine.userdata.offset = ''
		_state_machine.userdata.rotation = ''
		_state_machine.userdata.move_group = 'manipulator'
		_state_machine.userdata.namespace_move = ''
		_state_machine.userdata.gripper_service = ''
		_state_machine.userdata.positie = ['-0.194470, -1.32807, 0.8', '0.2, 0.2, 0.2,']
		_state_machine.userdata.action_topic = '/move_group'

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:96 y:20
			OperatableStateMachine.add('get positie',
										GetItemFromListState(),
										transitions={'done': 'compute pick', 'invalid_index': 'Not Found'},
										autonomy={'done': Autonomy.Off, 'invalid_index': Autonomy.Off},
										remapping={'list': 'positie', 'index': 'index', 'item': 'pos_object'})

			# x:615 y:23
			OperatableStateMachine.add('move to place',
										MoveitToJointsDynAriacState(),
										transitions={'reached': 'finished', 'planning_failed': 'wait 1', 'control_failed': 'wait 1'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off},
										remapping={'action_topic_namespace': 'namespace_move', 'move_group': 'move_group', 'action_topic': 'action_topic', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:642 y:151
			OperatableStateMachine.add('wait 1',
										WaitState(wait_time=5),
										transitions={'done': 'move to place'},
										autonomy={'done': Autonomy.Off})

			# x:398 y:28
			OperatableStateMachine.add('compute pick',
										ComputeGraspAriacState(joint_names=joint_names),
										transitions={'continue': 'move to place', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'move_group': 'move_group', 'action_topic_namespace': 'namespace_move', 'tool_link': 'tool_link', 'pose': 'pos_object', 'offset': 'offset', 'rotation': 'rotation', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
