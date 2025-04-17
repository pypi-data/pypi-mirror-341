# First  checking that the environment is web or local
import sys
# Initialize a variable to hold the mc_move function
mcmove = None

# Check if running in a WebAssembly environment (via Pyodide)
if 'pyodide' in sys.modules:
    # Import Pyodide's API
    import pyodide
    
    # Load the WebAssembly module (ensure the path is correct based on your package structure)
    wasm = pyodide.open_url('compdismatter/wasm/ising.wasm')
    
    # Get the mcmove function from the WASM module
    mcmove = wasm.exports['mcmove']
    print("Using mcmove from WebAssembly")
    
# Check if running in a native Python environment (for example, when using a shared library)
elif sys.platform != "emscripten":
    # Import the ctypes library to interact with the shared object (.so)
    import ctypes

    def get_lattice_pointer(arr):
        return arr.ravel(order='C').ctypes.data_as(ctypes.POINTER(ctypes.c_int))

    def get_float(value):
        return ctypes.c_float(value)
    # Load the shared object (.so) library
    lib = ctypes.CDLL('compdismatter/lib/ising.so')
    # Declare the function signature
    lib.mcmove.argtypes = [ctypes.POINTER(ctypes.c_int), ctypes.c_int, ctypes.c_double]
    lib.mcmove.restype = None
    # Get the mcmove function from the shared object library
    mcmove = lib.mcmove
    print("Using mcmove from native .so library")
    
else:
    print("Environment not recognized for mcmove")

# Ensure that mcmove is set
if mcmove is None:
    raise ImportError("Could not load mcmove from either WASM or native library.")

def mcmove_wrapper(lattice, N, beta):
    if 'pyodide' in sys.modules:
        # WebAssembly-specific logic: Pass array as memory or shared buffer
        # This would use pyodide or wasm-specific handling
        import js
        lattice_buffer = js.Uint8Array.new(len(lattice) * lattice.itemsize)  
        lattice_buffer.set(lattice)
        # Pass the buffer to the C function in WebAssembly (handle with pyodide or WASI interface)
        mcmove(lattice_buffer, N, beta)  # example; modify as per actual WASM interface
    else:
        # Native: Convert to ctypes pointer and call C function
        lattice_ptr = get_lattice_pointer(lattice)
        mcmove(lattice_ptr, N, beta)  # Assuming 'lib' is loaded

import numpy as np
from numpy.random import rand
import matplotlib.pyplot as plt

class IsingModel:
    def __init__(self, N, equilibration=1024, production=1024):
        """
        Initialize the Ising model simulation.
        
        Parameters:
        -----------
        N : int
            Size of the lattice (N x N)
        equilibration : int
            Number of Monte Carlo sweeps for equilibration
        production : int
            Number of Monte Carlo sweeps for calculation


        Example usage:

        # Initialize model
        model = IsingModel(N=16, nt=88, equilibration=1024, production=1024)
        
        # Run the simulation
        model.simulate()
        
        # Plot the results
        model.plot_results()    
        """
        self.N = N
        self.equilibration = equilibration
        self.production = production
        
        
        # Normalization factors
        self.n1 = 1.0/(production*N*N)
        self.n2 = 1.0/(production*production*N*N)
    
    def initialstate(self):
        """ Generate a random spin configuration for initial condition """
        np.random.seed(1234)  # For reproducibility
        state = 2*np.random.randint(2, size=(self.N, self.N),dtype=np.int32)-1
        return state
    
    def vanilla_mcmove(self, config, beta):
        """Optimized Metropolis update (minimal numpy overhead)"""
        N = self.N
        for _ in range(N * N):
            a = np.random.randint(0, N)
            b = np.random.randint(0, N)
            s = config[a, b]
            nb = (
                config[(a + 1) % N, b]
                + config[a, (b + 1) % N]
                + config[(a - 1) % N, b]
                + config[a, (b - 1) % N]
            )
            cost = 2 * s * nb
            if cost <= 0 or rand() < self.exp_cache.get(cost, np.exp(-cost * beta)):
                config[a, b] = -s
        return config

    def calcEnergy(self, config):
        """ Energy of a given configuration """
        energy = 0
        N = self.N
        for i in range(N):
            for j in range(N):
                S = config[i,j]
                nb = config[(i+1)%N, j] + config[i,(j+1)%N] + config[(i-1)%N, j] + config[i,(j-1)%N]
                energy += -nb*S
        return energy/4.
    
    def calcMag(self, config):
        """ Magnetization of a given configuration """
        return np.sum(config)
    
    def simulate(self, temperature=1.0):
        """ Run the simulation for all temperature points """
        self.exp_cache = {2*d: np.exp(-2*d/temperature) for d in range(5)}
        T = temperature
        E1 = M1 = E2 = M2 = 0
        config = self.initialstate()
        iT = 1.0/T
        iT2 = iT*iT
        
        beginning = config.copy()
        # Equilibration phase
        for i in range(self.equilibration):
            # print(i)
            # print(config)
            mcmove_wrapper(config,self.N ,iT)
            # print(config)

        self.config = config
        print(config==beginning)

        
        print("production")
        # Measurement phase
        for i in range(self.production):
            print(i)
            mcmove_wrapper(config,self.N ,iT)
            self.config = config
            
    
            # Ene = self.calcEnergy(config)
            # Mag = self.calcMag(config)
            
            # E1 += Ene
            # M1 += Mag
            # M2 += Mag*Mag
            # E2 += Ene*Ene
        
        # Calculate observables
        # self.E = self.n1 * E1
        # self.M = self.n1 * M1
        # self.C = (self.n1 * E2 - self.n2 * E1 * E1) * iT2
        # self.X = (self.n1 * M2 - self.n2 * M1 * M1) * iT
        
    
    def plot_config(self):
        """ Plot the results of the simulation """
        fig,ax = plt.subplots(figsize=(5, 5))
        ax.matshow(self.config, cmap='copper') 
        ax.axis('off')   
        plt.tight_layout()
        plt.show()