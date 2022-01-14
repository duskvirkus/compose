from abc import ABC, abstractmethod

class Element(ABC):

    element_counter = 0
    
    @abstractmethod
    def get_shape(self):
        pass

    @abstractmethod
    def get_shape_group(self):
        pass

    @abstractmethod
    def get_to_optimize(self, set_grad=True):
        pass

    @abstractmethod
    def clamp_values(self) -> None:
        pass

    @staticmethod
    def get_next_id() -> int:
        id = Element.element_counter
        Element.element_counter += 1
        return id
