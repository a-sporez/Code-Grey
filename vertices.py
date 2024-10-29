import matplotlib.pyplot as plt
from matplotlib.patches import Polygon

def plot_polygon(vertices):
    """
    Plot a polygon from a list of vertices.

    Parameters:
        vertices (list of tuples): List of (x, y) coordinates for each vertex.
    """
    fig, ax = plt.subplots()
    polygon = Polygon(vertices, closed=True, edgecolor='blue', facecolor='lightblue')
    ax.add_patch(polygon)
    
    # Extract x and y coordinates for setting plot limits
    x, y = zip(*vertices)
    ax.set_xlim(min(x) - 1, max(x) + 1)
    ax.set_ylim(min(y) - 1, max(y) + 1)
    
    # Plot settings
    ax.set_aspect('equal')
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.set_title("Polygon Preview")
    
    # Show vertices
    for (i, (vx, vy)) in enumerate(vertices):
        ax.plot(vx, vy, 'ro')  # Mark vertex
        ax.text(vx, vy, f"{i}", ha="right", va="top", color="red")  # Label vertex

    plt.show()

# Example vertices for a polygon
vertices = [(0, 10), (5, -5), (-5, -5)]
plot_polygon(vertices)