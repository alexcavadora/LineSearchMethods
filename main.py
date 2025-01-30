class OptFunc:
    def __init__(self):
        """Initialize optimization function"""
        pass

    def eval(self, x):
        """
        Evaluates the function at a given point
        Returns: Function value at point
        """
    
    def ident(self, x):
        n = len(x)
        iden = []
        

    def grad(self):
        """
        Calculates gradient of the function
        Returns: Gradient vector at point
        """
        pass

    def hess(self):
        """
        Calculates Hessian matrix of the function
        Returns: Hessian matrix at point
        """
        pass

    def output(self, grade):
        """
        Calls one of the above methods based on grade
        Args:
            grade: Integer indicating which method to call
                  0 = eval()
                  1 = grad() 
                  2 = hess()
        Returns: Result from called method
        """
        pass

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