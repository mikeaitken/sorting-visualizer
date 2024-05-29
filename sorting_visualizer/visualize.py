import matplotlib.pyplot as plt
import matplotlib.animation as animation

def visualize_sorting(arr, sort_algorithm, title, interval):
    """Function to visualize the sorting process."""
    generator = sort_algorithm(arr)
    
    fig, ax = plt.subplots()
    ax.set_title(title)
    bar_rects = ax.bar(range(len(arr)), arr, align="edge")
    ax.set_xlim(0, len(arr))
    ax.set_ylim(0, int(1.1 * max(arr)))
    
    iteration = [0]
    
    def update_fig(data, rects, iteration):
        arr, swaps = data
        for rect, val in zip(rects, arr):
            rect.set_height(val)
            rect.set_color('b')
        for swap in swaps:
            if len(swap) > 1:
                if swap[0] < len(rects) and swap[1] < len(rects):
                    rects[swap[0]].set_color('r')
                    rects[swap[1]].set_color('r')
            elif len(swap) == 1:
                if swap[0] < len(rects):
                    rects[swap[0]].set_color('r')
        iteration[0] += 1
    
    anim = animation.FuncAnimation(fig, func=update_fig, fargs=(bar_rects, iteration), frames=generator, interval=interval, repeat=False, cache_frame_data=False)
    return fig, anim
