import logging

class Net_Inv_Meta(type):
    device_counter = {}
    
    def __new__ (cls, name, bases, dct):
        new_class = super().__new__(cls, name, bases, dct)
        if name in ['Router', 'Switch', 'Firewall']:
            cls.device_counter[name] = cls.device_counter.get(name, 0) + 1
            Net_Inv_Meta.device_counter[name] = new_class
            logging.info(f"Registered {name} in Network Inventory")
        return new_class
    
    def __init__(cls, name, bases, dct):
        if 'configure_interface' not in dct or 'save_configuration' not in dct:
            raise NotImplementedError(f"Class {name} must implement interface configuration and save configuration options")
        super().__init__(name, bases, dct)
        cls.setup_security_defaults(cls)
        cls.vlan_management(cls)
        
    @staticmethod
    def base_info(cls):
        cls.hostname = cls.__name__
        cls.interfaces = ['24', '48']
        
    @staticmethod
    def setup_security_defaults(cls):
        cls.password = 'Admin'
        cls.default_native_vlan = 'VLAN1'
        cls.vpn_enabled = False
        cls.log_changes = lambda message: logging.info(f"Configuration change in {cls.__name__}: {message}")
    
    @staticmethod
    def vlan_management(cls):
        cls.native_vlan = 'VLAN90'
        cls.log_changes = lambda message: logging.info(f"Configuration change in {cls.__name__}: {message}")
        
        
    def connect(cls):
        print(f"{cls.__name__} connecting using default method.")

    def disconnect(cls):
        print(f"{cls.__name__} disconnecting using default method.")

    def update_firmware(cls):
        print(f"{cls.__name__} updating firmware using default method.")    


class Router(metaclass=Net_Inv_Meta):
    
    @property
    def base_info(self):
        Net_Inv_Meta.base_info(self.__class__)
        return(f"Device {self.hostname} has {self.interfaces[1]} interfaces")
    
    def configure_interface(self):
        self.log_changes("Interfaces configured")
        return "Interfaces configured"

    def save_configuration(self):
        self.log_changes("Configuration saved")
        return 'Configuration saved'
    
    def connect(self):
        Net_Inv_Meta.connect(self.__class__)
        print(f"{self.__class__.__name__} establishing a VPN connection.")
            
    def update_firmware(self):
        Net_Inv_Meta.update_firmware(self.__class__)
                        
            
class Switch(metaclass=Net_Inv_Meta):
    
    @property
    def base_info(self):
        Net_Inv_Meta.base_info(self.__class__)
        return(f"Device {self.hostname} has {self.interfaces[0]} interfaces")
    
    def configure_interface(self):
        self.log_changes("Interfaces configured")
        return "Interfaces configured"

    def save_configuration(self):
        self.log_changes("Configuration saved")
        return 'Configuration saved'
        
    def connect(self):
        Net_Inv_Meta.connect(self.__class__)
        print(f"{self.__class__.__name__} establishing a VPN connection.")
    
    @property    
    def change_native_vlan(self):
        Net_Inv_Meta.setup_security_defaults(self.__class__)
        print(f"Default Native VLAN is {self.default_native_vlan}")
        Net_Inv_Meta.vlan_management(self.__class__)
        return (f"Native VLAN has changed to {self.native_vlan}") 
    
class Firewall(metaclass=Net_Inv_Meta):
    
    @property
    def base_info(self):
        Net_Inv_Meta.base_info(self.__class__)
        return(f"Device {self.hostname} has {self.interfaces[0]} interfaces")
    
    def configure_interface(self):
        self.log_changes("Interfaces configured")
        return "Interfaces configured"

    def save_configuration(self):
        self.log_changes("Configuration saved")
        return 'Configuration saved'
        
    def connect(self):
        Net_Inv_Meta.setup_security_defaults(self.__class__)
        print(f"VPN Enabled is {self.vpn_enabled}")
        print(f"{self.__class__.__name__} enabling and establishing a VPN connection.")
    


router1 = Router()
switch1 = Switch()
firewall1 = Firewall()

print('\n')

router1.connect()
router1.update_firmware()
print(router1.base_info)

print('\n')

print(switch1.base_info)
switch1.connect()
print(switch1.change_native_vlan)

print('\n')

firewall1.connect()

print('\n')
print(Net_Inv_Meta.device_counter)