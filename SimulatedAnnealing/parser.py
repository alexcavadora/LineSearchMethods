def parser(fileContent):
  """
  Parse the file content of the dataset for the Simulated Annealing algorithm.
  Args:
    fileContent: The content of a file.
  Returns:
    {
      "n_cities": int,
      "distances": list[list[float]],
      "xy": list[list[float]]
    }
  """
  data = {
    "n_cities": 0,
    "distances": [],
    "xy": []
  }

  try:
    # First lines is always the number of cities
    data["n_cities"] = int(fileContent.split("\n")[0])

    # The matrix is cuadratic where n_cities is the number of rows and columns
    for i in range(data["n_cities"]):
      line = fileContent.split("\n")[i+1]
      data["distances"].append(list(map(float, line.split())))

    # The cities are in the next n_cities lines
    for i in range(data["n_cities"]):
      line = fileContent.split("\n")[i+data["n_cities"]+1]
      data["xy"].append(list(map(float, line.split())))
    
    return data
  except:
    print("Error parsing the file.")
    exit(1)

if __name__ == "__main__":
  with open("./dataset/rc_201.1.txt") as f:
    fileContent = f.read()

  print(parser(fileContent))
