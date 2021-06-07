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
from ariac_flexbe_states.detect_first_part_camera_ariac_state import DetectFirstPartCameraAriacState
from ariac_flexbe_states.lookup_from_table import LookupFromTableState
from ariac_flexbe_states.moveit_to_joints_dyn_ariac_state import MoveitToJointsDynAriacState
from ariac_flexbe_states.srdf_state_to_moveit_ariac_state import SrdfStateToMoveitAriac
from ariac_flexbe_states.text_to_float_state import TextToFloatState
from ariac_flexbe_states.vacuum_gripper_control_state import VacuumGripperControlState
from flexbe_states.wait_state import WaitState
# Additional imports can be added inside the following tags
# [MANUAL_IMPORT]

# [/MANUAL_IMPORT]


'''
Created on Sun Apr 25 2021
@author: docent
'''
class pick_part_from_conveyorSM(Behavior):
	'''
	pick's a part form athe conveyor
	'''


	def __init__(self):
		super(pick_part_from_conveyorSM, self).__init__()
		self.name = 'pick_part_from_conveyor'

		# parameters of this behavior

		# references to used behaviors

		# Additional initialization code can be added inside the following tags
		# [MANUAL_INIT]
		
		# [/MANUAL_INIT]

		# Behavior comments:



	def create(self):
		part_list = ['gasket_part', 'gear_part', 'piston_rod_part']
		joint_names = ['linear_arm_actuator_joint', 'shoulder_pan_joint', 'shoulder_lift_joint', 'elbow_joint', 'wrist_1_joint', 'wrist_2_joint', 'wrist_3_joint']
		pick1_group = 'robot1'
		pick2_group = 'robot2'
		# x:30 y:365, x:983 y:190, x:983 y:590, x:983 y:390
		_state_machine = OperatableStateMachine(outcomes=['finished', 'failed', 'Not found', 'parameter error'], output_keys=['type_part', 'namespace_move', 'gripper_service', 'end_pose'])
		_state_machine.userdata.conveyor_topic = []
		_state_machine.userdata.conveyor_frame = []
		_state_machine.userdata.ref_world = []
		_state_machine.userdata.robot_home1 = []
		_state_machine.userdata.robot_home2 = []
		_state_machine.userdata.robot_name = ''
		_state_machine.userdata.move_group = 'manipulator'
		_state_machine.userdata.action_topic = '/move_group'
		_state_machine.userdata.action_topic_namespace1 = '/ariac/arm1'
		_state_machine.userdata.action_topic_namespace2 = '/ariac/arm2'
		_state_machine.userdata.detect_frame = 'world'
		_state_machine.userdata.cam_topic = '/ariac/camera7_conveyor'
		_state_machine.userdata.cam_frame = 'camera7_conveyor_frame'
		_state_machine.userdata.pregrasp_pose = []
		_state_machine.userdata.namespace_move = []
		_state_machine.userdata.offset_part = 0.04
		_state_machine.userdata.rotation = 0
		_state_machine.userdata.tool_link = 'ee_link'
		_state_machine.userdata.type_part = ''
		_state_machine.userdata.end_pose = []
		_state_machine.userdata.gripper_service = ''
		_state_machine.userdata.pose_part_world = ''

		# Additional creation code can be added inside the following tags
		# [MANUAL_CREATE]
		
		# [/MANUAL_CREATE]


		with _state_machine:
			# x:262 y:24
			OperatableStateMachine.add('detect part',
										DetectFirstPartCameraAriacState(part_list=part_list, time_out=5),
										transitions={'continue': 'Config Robot 1 info', 'failed': 'failed', 'not_found': 'Wait camera'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'ref_frame': 'detect_frame', 'camera_topic': 'cam_topic', 'camera_frame': 'cam_frame', 'part': 'type_part', 'pose': 'pose_part_world'})

			# x:1579 y:424
			OperatableStateMachine.add('Compute pick',
										ComputeGraspAriacState(joint_names=joint_names),
										transitions={'continue': 'Activate gripper', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'move_group': 'move_group', 'action_topic_namespace': 'namespace_move', 'tool_link': 'tool_link', 'pose': 'pose_part_world', 'offset': 'float_value', 'rotation': 'rotation', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:485 y:24
			OperatableStateMachine.add('Config Robot 1 info',
										LookupFromTableState(parameter_name='/ariac_tables_unit2', table_name='info_parts', index_title='part', column_title='robot_home1'),
										transitions={'found': 'Config Robot 2 info', 'not_found': 'Not found'},
										autonomy={'found': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'index_value': 'type_part', 'column_value': 'robot_home1'})

			# x:635 y:25
			OperatableStateMachine.add('Config Robot 2 info',
										LookupFromTableState(parameter_name='/ariac_tables_unit2', table_name='info_parts', index_title='part', column_title='robot_home2'),
										transitions={'found': 'gripper info', 'not_found': 'Not found'},
										autonomy={'found': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'index_value': 'type_part', 'column_value': 'robot_home2'})

			# x:958 y:25
			OperatableStateMachine.add('Deactivate gripper',
										VacuumGripperControlState(enable=False),
										transitions={'continue': 'Move Robot 1 Home', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'service_name': 'gripper_service'})

			# x:1134 y:24
			OperatableStateMachine.add('Move Robot 1 Home',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'Move Robot 2 Home', 'planning_failed': 'Wait 1', 'control_failed': 'Wait 1', 'param_error': 'parameter error'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'robot_home1', 'move_group': 'move_group', 'action_topic_namespace': 'action_topic_namespace1', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:1284 y:24
			OperatableStateMachine.add('Move Robot 2 Home',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'namespace info', 'planning_failed': 'Wait 2', 'control_failed': 'Wait 2', 'param_error': 'parameter error'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'robot_home2', 'move_group': 'move_group', 'action_topic_namespace': 'action_topic_namespace2', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:1134 y:724
			OperatableStateMachine.add('Move Robot 2 end',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'finished', 'planning_failed': 'Wait 6', 'control_failed': 'Wait 6', 'param_error': 'parameter error'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'end_pose', 'move_group': 'move_group', 'action_topic_namespace': 'namespace_move', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:1571 y:624
			OperatableStateMachine.add('Move Robot to pick',
										MoveitToJointsDynAriacState(),
										transitions={'reached': 'Wait Gripper', 'planning_failed': 'wait 4', 'control_failed': 'wait 4'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off},
										remapping={'action_topic_namespace': 'namespace_move', 'move_group': 'move_group', 'action_topic': 'action_topic', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:1584 y:124
			OperatableStateMachine.add('Move to Pregrasp',
										SrdfStateToMoveitAriac(),
										transitions={'reached': 'Offset info_3', 'planning_failed': 'wait 3', 'control_failed': 'wait 3', 'param_error': 'wait 3'},
										autonomy={'reached': Autonomy.Off, 'planning_failed': Autonomy.Off, 'control_failed': Autonomy.Off, 'param_error': Autonomy.Off},
										remapping={'config_name': 'pregrasp_pose', 'move_group': 'move_group', 'action_topic_namespace': 'namespace_move', 'action_topic': 'action_topic', 'robot_name': 'robot_name', 'config_name_out': 'config_name_out', 'move_group_out': 'move_group_out', 'robot_name_out': 'robot_name_out', 'action_topic_out': 'action_topic_out', 'joint_values': 'joint_values', 'joint_names': 'joint_names'})

			# x:1585 y:224
			OperatableStateMachine.add('Offset info_3',
										LookupFromTableState(parameter_name='/ariac_tables_unit2', table_name='info_parts', index_title='part', column_title='offset_part'),
										transitions={'found': 'Text To Float', 'not_found': 'Not found'},
										autonomy={'found': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'index_value': 'type_part', 'column_value': 'offset_part'})

			# x:1593 y:324
			OperatableStateMachine.add('Text To Float',
										TextToFloatState(),
										transitions={'done': 'Compute pick'},
										autonomy={'done': Autonomy.Off},
										remapping={'text_value': 'offset_part', 'float_value': 'float_value'})

			# x:1157 y:124
			OperatableStateMachine.add('Wait 1',
										WaitState(wait_time=5),
										transitions={'done': 'Move Robot 1 Home'},
										autonomy={'done': Autonomy.Off})

			# x:1307 y:124
			OperatableStateMachine.add('Wait 2',
										WaitState(wait_time=5),
										transitions={'done': 'Move Robot 2 Home'},
										autonomy={'done': Autonomy.Off})

			# x:1157 y:624
			OperatableStateMachine.add('Wait 6',
										WaitState(wait_time=5),
										transitions={'done': 'Move Robot 2 end'},
										autonomy={'done': Autonomy.Off})

			# x:1455 y:722
			OperatableStateMachine.add('Wait Gripper',
										WaitState(wait_time=2),
										transitions={'done': 'end pose info'},
										autonomy={'done': Autonomy.Off})

			# x:303 y:112
			OperatableStateMachine.add('Wait camera',
										WaitState(wait_time=3),
										transitions={'done': 'detect part'},
										autonomy={'done': Autonomy.Off})

			# x:1285 y:724
			OperatableStateMachine.add('end pose info',
										LookupFromTableState(parameter_name='/ariac_tables_unit2', table_name='info_parts', index_title='part', column_title='end_pose'),
										transitions={'found': 'Move Robot 2 end', 'not_found': 'Not found'},
										autonomy={'found': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'index_value': 'type_part', 'column_value': 'end_pose'})

			# x:795 y:25
			OperatableStateMachine.add('gripper info',
										LookupFromTableState(parameter_name='/ariac_tables_unit2', table_name='info_parts', index_title='part', column_title='gripper_service'),
										transitions={'found': 'Deactivate gripper', 'not_found': 'Not found'},
										autonomy={'found': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'index_value': 'type_part', 'column_value': 'gripper_service'})

			# x:1435 y:24
			OperatableStateMachine.add('namespace info',
										LookupFromTableState(parameter_name='/ariac_tables_unit2', table_name='info_parts', index_title='part', column_title='robot_action_topic_namespace'),
										transitions={'found': 'pregrasp pose', 'not_found': 'Not found'},
										autonomy={'found': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'index_value': 'type_part', 'column_value': 'namespace_move'})

			# x:1585 y:24
			OperatableStateMachine.add('pregrasp pose',
										LookupFromTableState(parameter_name='/ariac_tables_unit2', table_name='info_parts', index_title='part', column_title='robot_pregrasp'),
										transitions={'found': 'Move to Pregrasp', 'not_found': 'Not found'},
										autonomy={'found': Autonomy.Off, 'not_found': Autonomy.Off},
										remapping={'index_value': 'type_part', 'column_value': 'pregrasp_pose'})

			# x:1457 y:124
			OperatableStateMachine.add('wait 3',
										WaitState(wait_time=5),
										transitions={'done': 'Move to Pregrasp'},
										autonomy={'done': Autonomy.Off})

			# x:1707 y:724
			OperatableStateMachine.add('wait 4',
										WaitState(wait_time=5),
										transitions={'done': 'Move Robot to pick'},
										autonomy={'done': Autonomy.Off})

			# x:1574 y:524
			OperatableStateMachine.add('Activate gripper',
										VacuumGripperControlState(enable=True),
										transitions={'continue': 'Move Robot to pick', 'failed': 'failed'},
										autonomy={'continue': Autonomy.Off, 'failed': Autonomy.Off},
										remapping={'service_name': 'gripper_service'})


		return _state_machine


	# Private functions can be added inside the following tags
	# [MANUAL_FUNC]
	
	# [/MANUAL_FUNC]
