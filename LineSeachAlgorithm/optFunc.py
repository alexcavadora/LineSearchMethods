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

    def ident(self, x):
        n = len(x)
        return [[1 if i == j else 0 for j in range(n)] for i in range(n)]

    def grad(self, x):
        return 2*x

    def hess(self, x):
        return 2*self.ident(x)

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