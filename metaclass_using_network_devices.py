import logging

class Net_Inv_Meta(type): # Here is the Magic: the root level of Python objects is the type... type! A class is a "type" type.
    device_counter = {} #keep track of how many classes are created
    
    def __new__ (cls, name, bases, dct):
        new_class = super().__new__(cls, name, bases, dct) #__new__ allows to create new classes from the metaclass
        if name in ['Router', 'Switch', 'Firewall']:
            cls.device_counter[name] = cls.device_counter.get(name, 0) + 1
            Net_Inv_Meta.device_counter[name] = new_class
            logging.info(f"Registered {name} in Network Inventory")
        return new_class
    
    def __init__(cls, name, bases, dct): # Like any other classes __init__ is the constructor
        if 'configure_interface' not in dct or 'save_configuration' not in dct: # Validation: all the derived classes from the metaclass must have those methods implemented
            raise NotImplementedError(f"Class {name} must implement interface configuration and save configuration options") # otherwise we raise an error
        super().__init__(name, bases, dct) # the derived classes inherit built-in aspects from the metaclass using the super() function
        cls.setup_security_defaults(cls) 
        cls.vlan_management(cls)
        
    @staticmethod # static methods allows to query the method's attribute, even if they are inherited from metaclass and are not accessible by default
    def base_info(cls):
        cls.hostname = cls.__name__ # we use the name of class derived from the metaclass as the default hostname
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


class Router(metaclass=Net_Inv_Meta): # A class derived from metaclass definition
    
    @property # we use property to access value from a class's methods, if we don't use property we are pointed to the python object's id of the attribute that is like <function Net_Inv_Meta.vlan_management at 0x00000186E9731240> 
    def base_info(self):
        Net_Inv_Meta.base_info(self.__class__) # here is a trick: we can't use the super() function cause MRO doesn't allows us to access metaclass attributes... so we call the directly!
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
    


router1 = Router() # class instantiation. By MRO (Method Resolution Order) a class instance doesn't have access to the metaclass attributes. That's why we use some static methods and property feature.
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
