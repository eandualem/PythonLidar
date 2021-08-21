class Bounds:
    """ Store bounds as an object for ease of access.
    """
    def __init__(self, xmin: float, xmax: float, ymin: float, ymax: float) -> None:
        """ Method used for instantiating the Bounds class

        Args:
            xmin (float): the smallest x value
            xmax (float): the largest x value
            ymin (float): the smallest y value
            ymax (float): the largest y value
        """

        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax

    def get_bound_tuple(self) -> tuple:
        """ Return bounds as a tuple

        Returns:
            tuple
        """
        return ([self.xmin, self.xmax], [self.ymin, self.ymax])

    def get_bound_str(self) -> str:
        """ Return bounds as a string

        Returns:
            str: return bounds in a '({[minx, maxx]},{[miny,maxy]})' format which pdal pipeline's reader.ept expects.
        """

        return f"([{self.xmin}, {self.xmax}], [{self.ymin}, {self.ymax}])"
    
    def get_bound_name(self) -> str:
        return f"{self.xmin}_{self.xmax}_{self.ymin}_{self.ymax}"
