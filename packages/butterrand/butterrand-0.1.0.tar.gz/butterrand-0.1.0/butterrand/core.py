import math
import hashlib

class ButterflyRandom:
    def __init__(self, seed, r=3.99, epsilon=1e-6, phi=None, mode='logistic', noise_function='sin'):
        self.original_seed = self._normalize_seed(seed)
        self.x = self.original_seed
        self.r = r
        self.epsilon = epsilon
        self.phi = phi if phi is not None else math.pi / 4
        self.mode = mode
        self.noise_fn = getattr(math, noise_function, math.sin)

    def _normalize_seed(self, seed):
        if isinstance(seed, str):
            hashed = hashlib.sha256(seed.encode()).hexdigest()
            seed_float = int(hashed[:8], 16) / 0xFFFFFFFF
        else:
            seed_float = float(seed) % 1
        return seed_float if seed_float != 0 else 1e-8

    def reset(self):
        self.x = self.original_seed

    def _chaotic_step(self):
        if self.mode == 'logistic':
            self.x = self.r * self.x * (1 - self.x)
        elif self.mode == 'sine':
            self.x = self.r * math.sin(math.pi * self.x)
        else:
            raise ValueError("Unsupported mode. Use 'logistic' or 'sine'.")

        chaos = self.x + self.epsilon * self.noise_fn(math.pi * self.x + self.phi)
        return chaos % 1

    def next_float(self):
        return self._chaotic_step()

    def next_int(self, min_val=0, max_val=100):
        return min_val + int(self.next_float() * (max_val - min_val))

    def generate_sequence(self, count, as_int=False, min_val=0, max_val=100):
        return [
            self.next_int(min_val, max_val) if as_int else self.next_float()
            for _ in range(count)
        ]
