from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt


if __name__ == "__main__":
    data = np.load("traj.npy")
    fig = plt.figure()
    ax = plt.axes(projection='3d')

    T=np.linspace(0,1,data.shape[0])**2

    ax.plot3D(data[:,0], data[:,1], -data[:,2])
    '''
    for i in range(data.shape[0]):
        ax.scatter3D(data[i,0], data[i,1], -data[i,2], color=(T[i],0,1-T[i]))
    '''
    ax.scatter3D(data[0,0], data[0,1], -data[0,2], color=(1,0,0))
    ax.scatter3D(data[-1,0], data[-1,1], -data[-1,2], color=(0,0,1))
    ax.set_xlabel("north")
    ax.set_ylabel("east")
    ax.set_zlabel("altitude")

    plt.savefig("traj.png")
    plt.show()
