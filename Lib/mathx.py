import math
import random

class MathX:
    @staticmethod
    def lerp(a, b, t):
        return a + (b - a) * t
    
    @staticmethod
    def clamp(value, min_val, max_val):
        return max(min_val, min(value, max_val))
    
    @staticmethod
    def remap(value, from_min, from_max, to_min, to_max):
        return ((value - from_min) / (from_max - from_min)) * (to_max - to_min) + to_min
    
    @staticmethod
    def random_range(min_val, max_val):
        return random.uniform(min_val, max_val)
    
    @staticmethod
    def fibonacci(n):
        a, b = 0, 1
        for _ in range(n):
            yield a
            a, b = b, a + b
    
    @staticmethod
    def is_prime(n):
        if n < 2:
            return False
        for i in range(2, int(math.sqrt(n)) + 1):
            if n % i == 0:
                return False
        return True
