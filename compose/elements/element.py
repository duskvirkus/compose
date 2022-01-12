from abc import ABC, abstractmethod

class Element(ABC):

    element_counter = 0
    
    @abstractmethod
    def get_shape(self):
        pass

    @abstractmethod
    def get_shape_group(self):
        pass

    @staticmethod
    def get_next_id() -> int:
        id = Element.element_counter
        Element.element_counter += 1
        return id
