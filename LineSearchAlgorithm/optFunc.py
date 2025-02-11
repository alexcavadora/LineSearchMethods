from lib.optFunc import optFunc 

class optFuncSphere(optFunc):
  def eval(self, x):
    return sum(xi ** 2 for xi in x)

  def ident(self, x):
    n = len(x)
    return [[1 if i == j else 0 for j in range(n)] for i in range(n)]

  def grad(self, x):
    return 2*x

  def hess(self, x):
    return 2*self.ident(x)