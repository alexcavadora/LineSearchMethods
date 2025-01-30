class LinSearch:
    def __init__(self, func, stopCrit, stepCond):
        """
        Initialize linear search algorithm
        Args:
            func: OptFunc object containing the function to optimize
            stopCrit: Stopping criterion function
            stepCond: Step condition function
        """
        self.func = func
        self.stopCrit = stopCrit
        self.stepCond = stepCond

    def solve(self, x0):
        """
        Execute linear search optimization
        Args:
            x0: Initial point to start search
        Returns:
            Optimal point found
        """
        pass

    def plot2D(self):
        """
        Creates 2D visualization of optimization process
        Shows:
            - Function contour
            - Search path
            - Start and end points
        """
        pass