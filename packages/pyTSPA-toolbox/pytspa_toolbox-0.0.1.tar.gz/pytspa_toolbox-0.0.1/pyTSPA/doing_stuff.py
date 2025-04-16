import numpy as np
import numpy.typing as npt
import matplotlib.pyplot as plt
from matplotlib.axes import Axes

def create_data(length: int) -> npt.NDArray[np.float64]:
    """Creates some toy data with a given length

    Args:
        length (int): length of the generated data

    Returns:
        numpy.ndarray[float]: toy data
    """
    data = np.arange(length)
    data = np.exp(data,dtype=np.float64)
    return data

def plot_data(data: npt.NDArray[np.float64],fig: Axes|None = None)->None:
    """Plot the given data on a decorated figure. If the figure does not exist, it creates one.

    Args:
        data (numpy.ndarray[float]): data to plot
        fig (matplotlib.pyplot.Axes, optional): the figure axes to decorate and plot to. Defaults to None.
    """
    if fig is None:
        fig = plt.figure().gca()
    fig.plot(data,"o-")
    fig.set_xlabel("Index")
    fig.set_ylabel("Data value")
    fig.set_title("Showing our data")
    plt.show()

if __name__ == "__main__":
    print("Doing stuff submodule of our example_package")
    print("Does nothing when run, please import it in your code, for example: 'import example_package.doing_stuff'")
