from optFunc import optFuncSphere

class linSearch:
  def __init__(self, func, stopCrit=1e-5, stepCond=0.1):
    self.func = func
    self.stopCrit = stopCrit
    self.stepCond = stepCond
    self.solutions = []

  def solve(self, x0):
    x = x0
    while abs(self.func.grad(x) > self.stopCrit):
      x = x - self.stepCond * self.func.grad(x)
      self.solutions.append(x)
    return x

  def plot2D(self):
    pass

if __name__ == "__main__":
  func = optFuncSphere()
  optimizer = linSearch(func)
  x_opt = optimizer.solve(5)
  print(f"Optimo encontrado en: {x_opt}")
  optimizer.plot2D()