class Bounds:
    def __init__(self, xmin: float, xmax: float, ymin: float, ymax: float) -> None:
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax

    def get_bound_tuple(self) -> tuple:
        return ([self.xmin, self.xmax], [self.ymin, self.ymax])

    def get_bound_str(self) -> str:
        return f"([{self.xmin}, {self.xmax}], [{self.ymin}, {self.ymax}])"
    
    def get_bound_name(self) -> str:
        return f"{self.xmin}_{self.xmax}_{self.ymin}_{self.ymax}"
