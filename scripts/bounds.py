class Bounds:
    """ Store bounds as an object for ease of access.
    """
    def __init__(self, xmin: float, xmax: float, ymin: float, ymax: float) -> None:
        """ 
        Args:
            xmin (float): minimum longitude value in the boundary
            xmax (float): maximum longitude value in the boundary
            ymin (float): minimum latitude value in the boundary
            ymax (float): maximum latitude value in the boundary
        """

        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax

    def get_bound_tuple(self) -> tuple:
        """ Return bounds as a tuple

        Returns:
            tuple: bounds in tuple format
        """
        return ([self.xmin, self.xmax], [self.ymin, self.ymax])

    def get_bound_str(self) -> str:
        """ Return bounds as a string in '({[minx, maxx]},{[miny, maxy]})' format which pdal pipeline's reader.ept expects.

        Returns:
            str: bounds in sting format
        """

        return f"([{self.xmin}, {self.xmax}], [{self.ymin}, {self.ymax}])"
    
    def get_bound_name(self) -> str:
        """ Concatenate bound values and returns them as a string

        Returns:
            str: bounds in sting format
        """
        return f"{self.xmin}_{self.xmax}_{self.ymin}_{self.ymax}"
