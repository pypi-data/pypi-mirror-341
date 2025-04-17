from dataclasses import dataclass, field
from typing import Optional, Dict, Type, Union
from numbers import Number
import xml.etree.ElementTree as ET


@dataclass
class NewareStep:
	step_name: str
	step_type: int      # Unique identifier (Neware-defined)
	step_num: Optional[int] = 0
	
	main_attributes: Optional[dict] = None
	other_attributes: Optional[dict] = None
	conditions: Optional[dict] = None

	def add_condition(self, parameter:str, value:float, comparator:str='>', condition:str='next'):
		"""
		Apply `condition` when `parameter` `comparator` `value`. E.g., go to `next` when `voltage` `>` `3.6`.
		
		Args:
			parameter (str): {'voltage', 'current', 'time'}
			value (float): Value to compare parameter against. Units are in {'voltage':volts, 'current':amps, 'temperature':celsius}.
			comparator (str, optional): {'>', '>=', '<', '<='}. Read as apply condition when 'parameter comparator \
				value'. Defaults to '>' (parameter greater than value).
			condition (str, optional): {'next', 'finish', 'protect', 'stop'}. Result of valid condition. Defaults to 'next' (go to next step)
		"""
		if not self.other_attributes is None: 
			raise ValueError(f"{self.step_name} steps cannot have additional conditions.")

		valid_parameters = ['voltage', 'current', 'time']
		if not parameter in valid_parameters: raise ValueError(f"`parameter` must be one of the following: {valid_parameters}")
		valid_comparators = ['>', '>=', '<', '<=']
		if not comparator in valid_comparators: raise ValueError(f"`comparator` must be one of the following: {valid_comparators}")
		valid_conditions = ['next', 'finish', 'protect', 'stop']
		if not condition in valid_conditions: raise ValueError(f"`condition` must be one of the following: {valid_conditions}")

		#region: set parameter
		multiplier = None
		p_type = None
		if parameter == 'voltage': 
			multiplier = 10000
			p_type = 1
		elif parameter == 'current': 
			multiplier = 1000
			p_type = 2
		elif parameter == 'time': 
			multiplier = 1000
			p_type = 3
		else:
			raise ValueError(f"`parameter` must be one of the following: {valid_parameters}")
		#endregion

		#region set comparator value
		cmp_type = None
		#region: certain parameters can only use certain comparators (not sure why)
		if parameter in ['voltage', 'current']:
			if comparator == '>=': comparator = '>'
			elif comparator == '<=': comparator = '<'
		elif parameter in ['time', ]:
			if comparator == '>': comparator = '>='
			elif comparator == '<': comparator = '<='
		#endregion
		if comparator == '>': cmp_type = 3
		elif comparator == '>=': cmp_type = 4
		elif comparator == '<': cmp_type = 5
		elif comparator == '<=': cmp_type = 6
		else: raise ValueError(f"`comparator` must be one of the following: {valid_comparators}")
		#endregion

		#region: set jump
		jump = None
		if condition == 'next': jump = 65526
		elif condition == 'finish': jump = 6535
		elif condition == 'protect': jump = 65534
		elif condition == 'stop': jump = 65533
		else:
			raise ValueError(f"`condition` must be one of the following: {valid_conditions}")
		#endregion

		if not self.conditions:
			self.conditions = {}

		self.conditions[f'Cnd{len(self.conditions)+1}'] = {
			'type':str(p_type),
			'Function':"0",						# TODO
			'CmpType': str(cmp_type),
			'Jump_Line': str(jump),
			'Value':str(int(value * multiplier)),
			'TimeGoto':"0",						# TODO
			'GlobleUserID':"2147483647",		# TODO
			'GLobleType':"1",					# TODO
			'GlobalVar':"2147483647",			# TODO
			'Aux':"0",							# TODO
		}
		
	def to_xml(self) -> ET.Element:
		"""Returns an XML ElementTree.Element object representing the given step. \n

		Returns:
			ET.Element: XML Element describing the current step.
		"""

		step_el = ET.Element(f"Step{int(self.step_num)}", Step_ID=str(int(self.step_num)), Step_Type=str(int(self.step_type)))
		if self.main_attributes or self.other_attributes:
			limit_el = ET.SubElement(
				step_el,
				"Limit",
			)
			if self.main_attributes:
				main_el = ET.SubElement(
					limit_el,
					"Main"
				)
				for tag, attr in self.main_attributes.items():
					ET.SubElement(main_el, tag, Value=str(int(attr) if isinstance(attr, Number) else attr))
			if self.other_attributes:
				other_el = ET.SubElement(
					limit_el,
					"Other"
				)
				for tag, attr in self.other_attributes.items():
					ET.SubElement(other_el, tag, Value=str(int(attr) if isinstance(attr, Number) else attr))
			elif self.conditions:
				other_el = ET.SubElement(
					limit_el,
					"Other",
					CndCount=str(len(self.conditions)),
				)
				for tag, attr in self.conditions.items():
					ET.SubElement(other_el, tag, **attr)

		return step_el


@dataclass
class CC_CHG(NewareStep):
	@classmethod
	def create(cls, current:float, cutoff_voltage:Optional[float]=None, step_duration:Optional[float]=None) -> "CC_CHG":
		"""Creates a constant current charge step (CC CHG)

		Args:
			current (float): Charge current (in amps)
			cutoff_voltage (Optional[float], optional): Optional cutoff voltage (in voltage). If not supplied, you must define `step_duration`. Defaults to None.
			step_duration (Optional[float], optional): Optioanl step duration (in seconds). If not supplied, you must define `cutoff_voltage`. Defaults to None.

		Returns:
			CC_CHG: Constant current charge step
		"""

		if cutoff_voltage is None and step_duration is None: raise ValueError("At least one of `cutoff_voltage` and `step_duration` must be defined.")

		main_attr = {'Curr':current * 1000,}
		if cutoff_voltage:
			main_attr['Stop_Volt'] = cutoff_voltage * 10000
		if step_duration:
			main_attr['Time'] = step_duration * 1000

		return cls(
			step_name="CC CHG", 
			step_type=1, 
			main_attributes=main_attr
		)

@dataclass
class CC_DCHG(NewareStep):
	@classmethod
	def create(cls, current:float, cutoff_voltage:Optional[float]=None, step_duration:Optional[float]=None) -> "CC_DCHG":
		"""Creates a constant current discharge step (CC DCHG)

		Args:
			current (float): Discharge current (in amps)
			cutoff_voltage (Optional[float], optional): Optional cutoff voltage (in voltage). If not supplied, you must define `step_duration`. Defaults to None.
			step_duration (Optional[float], optional): Optioanl step duration (in seconds). If not supplied, you must define `cutoff_voltage`. Defaults to None.

		Returns:
			CC_DCHG: Constant current discharge step
		"""

		if cutoff_voltage is None and step_duration is None: raise ValueError("At least one of `cutoff_voltage` and `step_duration` must be defined.")

		main_attr = {'Curr':current * 1000,}
		if cutoff_voltage:
			main_attr['Stop_Volt'] = cutoff_voltage * 10000
		if step_duration:
			main_attr['Time'] = step_duration * 1000

		return cls(
			step_name="CC DCHG", 
			step_type=2, 
			main_attributes=main_attr
		)
	
@dataclass
class CV_CHG(NewareStep):
	@classmethod
	def create(cls, current:float, voltage:float, cutoff_current:Optional[float]=None, step_duration:Optional[float]=None) -> "CV_CHG":
		"""Creates a constant voltage charge step (CV CHG)

		Args:
			current (float): Charge current (in amps)
			voltage (float): Charge voltage (in volts)
			cutoff_current (Optional[float], optional): Optional cutoff current (in amp). If not supplied, you must define `step_duration`. Defaults to None.
			step_duration (Optional[float], optional): Optioanl step duration (in seconds). If not supplied, you must define `cutoff_current`. Defaults to None.

		Returns:
			CV_CHG: Constant voltage charge step
		"""

		if cutoff_current is None and step_duration is None: raise ValueError("At least one of `cutoff_current` and `step_duration` must be defined.")

		main_attr = {
			'Curr':current * 1000,
			'Volt':voltage * 10000}
		if cutoff_current:
			main_attr['Stop_Curr'] = cutoff_current * 1000
		if step_duration:
			main_attr['Time'] = step_duration * 1000

		return cls(
			step_name="CV CHG", 
			step_type=3, 
			main_attributes=main_attr
		)
	
@dataclass
class CV_DCHG(NewareStep):
	@classmethod
	def create(cls, current:float, voltage:float, cutoff_current:Optional[float]=None, step_duration:Optional[float]=None) -> "CV_DCHG":
		"""Creates a constant voltage discharge step (CV DCHG)

		Args:
			current (float): Discharge current (in amps)
			voltage (float): Discharge voltage (in volts)
			cutoff_current (Optional[float], optional): Optional cutoff current (in amps). If not supplied, you must define `step_duration`. Defaults to None.
			step_duration (Optional[float], optional): Optioanl step duration (in seconds). If not supplied, you must define `cutoff_current`. Defaults to None.

		Returns:
			CV_DCHG: Constant voltage discharge step
		"""

		if cutoff_current is None and step_duration is None: raise ValueError("At least one of `cutoff_current` and `step_duration` must be defined.")

		main_attr = {
			'Curr':current * 1000,
			'Volt':voltage * 10000}
		if cutoff_current:
			main_attr['Stop_Curr'] = cutoff_current * 1000
		if step_duration:
			main_attr['Time'] = step_duration * 1000

		return cls(
			step_name="CV DCHG", 
			step_type=19, 
			main_attributes=main_attr
		)

@dataclass
class CCCV_CHG(NewareStep):
	@classmethod
	def create(cls, current:float, voltage:float, cutoff_current:Optional[float]=None, step_duration:Optional[float]=None) -> "CCCV_CHG":
		"""Creates a constant-current constant-voltage charge step (CCCV CHG)

		Args:
			current (float): Charge current (in amps)
			voltage (float): Charge voltage (in volts)
			cutoff_current (Optional[float], optional): Optional cutoff current (in amp). If not supplied, you must define `step_duration`. Defaults to None.
			step_duration (Optional[float], optional): Optioanl step duration (in seconds). If not supplied, you must define `cutoff_current`. Defaults to None.

		Returns:
			CCCV_CHG: Constant-current constant-voltage charge step
		"""

		if cutoff_current is None and step_duration is None: raise ValueError("At least one of `cutoff_current` and `step_duration` must be defined.")

		main_attr = {
			'Curr':current * 1000,
			'Volt':voltage * 10000}
		if cutoff_current:
			main_attr['Stop_Curr'] = cutoff_current * 1000
		if step_duration:
			main_attr['Time'] = step_duration * 1000

		return cls(
			step_name="CCCV CHG", 
			step_type=7, 
			main_attributes=main_attr
		)
	
@dataclass
class CCCV_DCHG(NewareStep):
	@classmethod
	def create(cls, current:float, voltage:float, cutoff_current:Optional[float]=None, step_duration:Optional[float]=None) -> "CCCV_DCHG":
		"""Creates a constant-current constant-voltage discharge step (CCCV DCHG)

		Args:
			current (float): Discharge current (in amps)
			voltage (float): Discharge voltage (in volts)
			cutoff_current (Optional[float], optional): Optional cutoff current (in amp). If not supplied, you must define `step_duration`. Defaults to None.
			step_duration (Optional[float], optional): Optioanl step duration (in seconds). If not supplied, you must define `cutoff_current`. Defaults to None.

		Returns:
			CCCV_DCHG: Constant-current constant-voltage discharge step
		"""

		if cutoff_current is None and step_duration is None: raise ValueError("At least one of `cutoff_current` and `step_duration` must be defined.")

		main_attr = {
			'Curr':current * 1000,
			'Volt':voltage * 10000}
		if cutoff_current:
			main_attr['Stop_Curr'] = cutoff_current * 1000
		if step_duration:
			main_attr['Time'] = step_duration * 1000

		return cls(
			step_name="CCCV DCHG", 
			step_type=20, 
			main_attributes=main_attr
		)
	
@dataclass
class CYCLE(NewareStep):
	@classmethod
	def create(cls, start_step:int, num_cycles:int) -> "CYCLE":
		"""Creates a cycle step (CYCLE)

		Args:
			start_step (int): Step ID where cycle starts
			num_cycles (int): Number of cycles to perform.

		Returns:
			CYCLE: Cycle step
		"""
		other_attr = {
			'Start_Step':start_step,
			'Cycle_Count':num_cycles
		}
		return cls(
			step_name="CYCLE", 
			step_type=5, 
			other_attributes=other_attr
		)

@dataclass
class REST(NewareStep):
	@classmethod
	def create(cls, step_duration:float) -> "REST":
		"""Creates a rest step (REST)

		Args:
			step_duration (float): Step duration (in seconds).

		Returns:
			REST: Rest step
		"""

		main_attr = {'Time':step_duration * 1000,}
		return cls(
			step_name="REST", 
			step_type=4, 
			main_attributes=main_attr
		)

@dataclass
class PAUSE(NewareStep):
	@classmethod
	def create(cls) -> "PAUSE":
		"""Creates a pause step (PAUSE)

		Returns:
			PAUSE: Pause step
		"""

		return cls(
			step_name="PAUSE", 
			step_type=13,
		)
	
@dataclass
class END(NewareStep):
	@classmethod
	def create(cls) -> "END":
		"""Creates a end step (END)

		Returns:
			END: End step
		"""

		return cls(
			step_name="END", 
			step_type=6,
		)
	
