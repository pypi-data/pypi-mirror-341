import pyTSPA.doing_stuff as doing_stuff
import numpy as np
import matplotlib.pyplot as plt

def test_create_data():
    length = 10
    data = doing_stuff.create_data(length)
    
    # Ellenőrizd, hogy a létrehozott adat a megfelelő méretű
    assert data.size == length, f"Expected data size {length}, but got {data.size}"
    
    # Ellenőrizd, hogy az adat típus helyes
    assert isinstance(data, np.ndarray), "Data should be a numpy ndarray"
    assert data.dtype == np.float64, f"Expected dtype np.float64, but got {data.dtype}"

def test_plot_data():
    data = np.arange(10)
    fig, ax = plt.subplots()
    doing_stuff.plot_data(data, ax)
    
    # Ellenőrizd, hogy a plot megjelenik
    assert ax.get_xlabel() == "Index", "X label should be 'Index'"
    assert ax.get_ylabel() == "Data value", "Y label should be 'Data value'"
    assert ax.get_title() == "Showing our data", "Title should be 'Showing our data'"

if __name__ == "__main__":
    test_create_data()
    test_plot_data()
    print("All tests passed!")
