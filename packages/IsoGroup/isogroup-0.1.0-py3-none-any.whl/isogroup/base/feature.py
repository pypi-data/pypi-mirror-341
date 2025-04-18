class Feature:

    def __init__(self, rt: float, mz: float, intensity: float, **extra_dims):
        self.rt = rt
        self.mz = mz
        self.intensity = intensity
        self.__dict__.update(extra_dims)
        self.is_adduct: tuple[bool, str] = (False, "")
        self.in_cluster: bool = False
        self.mz_tol: float = 0.001
        self.rt_tol: float = 0.1

    def __eq__(self, other) -> bool:
        """
        Check if two features are equal within given tolerances.
        :param other: Feature
        :return: bool
        """
        return abs(self.rt - other.rt) < self.rt_tol and abs(
            self.mz - other.mz) < self.mz_tol

    def __hash__(self):
        return hash((self.rt, self.mz))
