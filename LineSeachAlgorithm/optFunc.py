class OptFunc:
    def __init__(self):
        """Initialize optimization function"""
        pass

    def eval(self):
        """
        Evaluates the function at a given point
        Returns: Function value at point
        """
        pass

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