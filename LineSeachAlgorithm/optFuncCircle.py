class optFunc:
  def eval(self, x: float) -> float:
    pass

  def grad(self, x: float) -> float:
    pass

  def hess(self) -> float:
    pass

  def output(self, x: float, grade: int = 2) -> float:
    if (grade == 1): 
      return self.eval(x)
    elif (grade == 2):
      return self.grad(x)
    elif (grade == 3):
      return self.hess()
    else: 
      print('Grade not supported')

class optFuncCircle(optFunc):
  def eval(self, x: float) -> float:
    return x**2

  def grad(self, x: float) -> float:
    return 2*x

  def hess(self) -> float:
    return 2.0

if __name__ == "__main__":
  f = optFunc()